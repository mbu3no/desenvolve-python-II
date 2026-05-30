"""Módulo ``labirinto``: criação, exibição e resolução do labirinto.

O labirinto é **gerado aleatoriamente** (nunca lido de uma string fixa no
código) por um algoritmo de *recursive backtracker* (escavação recursiva).
Cada labirinto recebe itens colecionáveis espalhados pelos corredores e
possui uma entrada e uma saída.

Representação interna
---------------------
O labirinto é um dicionário::

    {
        "grade":  list[list[str]],   # matriz de caracteres ('#' parede, ' ' livre)
        "inicio": (linha, coluna),   # posição de entrada
        "saida":  (linha, coluna),   # posição de saída
        "itens":  dict[(l, c) -> int]  # posição -> pontos do item
    }

As posições são sempre tuplas ``(linha, coluna)``.

Funções principais:

* :func:`criar_labirinto` — gera um novo labirinto aleatório.
* :func:`imprimir_labirinto` — desenha o labirinto (com o jogador) usando rich.
* :func:`resolver_labirinto` — **função recursiva** que devolve a lista de
  comandos que leva da entrada à saída.
"""

import random

from rich.text import Text

#: Caractere que representa uma parede na grade.
PAREDE = "#"
#: Caractere que representa um corredor livre na grade.
LIVRE = " "

#: Mapeia o nome de cada movimento para o deslocamento ``(linha, coluna)``.
MOVIMENTOS = {
    "cima": (-1, 0),
    "baixo": (1, 0),
    "esquerda": (0, -1),
    "direita": (0, 1),
}

#: Tamanho (em células) de cada nível de dificuldade.
DIFICULDADES = {
    1: (6, 6),    # fácil
    2: (10, 10),  # médio
    3: (16, 16),  # difícil
}


def criar_labirinto(dificuldade: int = 1, qtd_itens: int = 5) -> dict:
    """Gera e devolve um novo labirinto aleatório.

    A estrutura é escavada por um algoritmo recursivo (*recursive
    backtracker*): partindo da célula inicial, o algoritmo visita vizinhos
    ainda não visitados em ordem aleatória, derrubando a parede entre eles.

    :param dificuldade: Nível ``1`` (fácil), ``2`` (médio) ou ``3`` (difícil);
        define o tamanho do labirinto.
    :param qtd_itens: Quantidade de itens colecionáveis a espalhar.
    :returns: O dicionário que representa o labirinto (ver módulo).
    :raises ValueError: Se ``dificuldade`` não for 1, 2 ou 3.
    """
    if dificuldade not in DIFICULDADES:
        raise ValueError("Dificuldade deve ser 1, 2 ou 3.")

    cels_l, cels_c = DIFICULDADES[dificuldade]
    altura = 2 * cels_l + 1
    largura = 2 * cels_c + 1

    # Começa tudo parede; o escavador abre os corredores.
    grade = [[PAREDE for _ in range(largura)] for _ in range(altura)]
    _escavar(grade, 1, 1, set())

    inicio = (1, 1)
    saida = (altura - 2, largura - 2)
    grade[saida[0]][saida[1]] = LIVRE

    itens = _espalhar_itens(grade, inicio, saida, qtd_itens)

    return {"grade": grade, "inicio": inicio, "saida": saida, "itens": itens}


def _escavar(grade: list, linha: int, coluna: int, visitados: set) -> None:
    """Escava recursivamente os corredores do labirinto (backtracker).

    Esta é uma função **recursiva**: ela se chama para cada vizinho não
    visitado, abrindo a parede intermediária a cada passo.

    :param grade: A matriz de caracteres sendo escavada (modificada no local).
    :param linha: Linha da célula atual.
    :param coluna: Coluna da célula atual.
    :param visitados: Conjunto de células já visitadas.
    """
    visitados.add((linha, coluna))
    grade[linha][coluna] = LIVRE

    direcoes = list(MOVIMENTOS.values())
    random.shuffle(direcoes)
    for dl, dc in direcoes:
        nova_l, nova_c = linha + 2 * dl, coluna + 2 * dc
        if 0 < nova_l < len(grade) - 1 and 0 < nova_c < len(grade[0]) - 1:
            if (nova_l, nova_c) not in visitados:
                # Derruba a parede entre a célula atual e a vizinha.
                grade[linha + dl][coluna + dc] = LIVRE
                _escavar(grade, nova_l, nova_c, visitados)


def _espalhar_itens(grade: list, inicio: tuple, saida: tuple, quantidade: int) -> dict:
    """Sorteia posições livres para colocar itens colecionáveis.

    :param grade: A grade já escavada.
    :param inicio: Posição inicial (não recebe item).
    :param saida: Posição de saída (não recebe item).
    :param quantidade: Número de itens desejado.
    :returns: Dicionário ``(linha, coluna) -> pontos`` com os itens.
    """
    livres = [
        (l, c)
        for l in range(len(grade))
        for c in range(len(grade[0]))
        if grade[l][c] == LIVRE and (l, c) not in (inicio, saida)
    ]
    random.shuffle(livres)
    return {pos: 10 for pos in livres[:quantidade]}


def imprimir_labirinto(labirinto: dict, jogador: dict, cor: str = "cyan") -> Text:
    """Monta o desenho do labirinto (com o jogador e os itens) para o rich.

    :param labirinto: O labirinto a desenhar.
    :param jogador: Dicionário do jogador (usa a chave ``"pos"``).
    :param cor: Cor principal usada nas paredes.
    :returns: Um objeto ``rich.text.Text`` pronto para ``console.print``.
    """
    pos_jogador = tuple(jogador["pos"])
    texto = Text()
    for l, linha in enumerate(labirinto["grade"]):
        for c, celula in enumerate(linha):
            if (l, c) == pos_jogador:
                texto.append("@", style="bold yellow")
            elif (l, c) == labirinto["saida"]:
                texto.append("⚑", style="bold green")
            elif (l, c) in labirinto["itens"]:
                texto.append("●", style="bold magenta")
            elif celula == PAREDE:
                texto.append("█", style=cor)
            else:
                texto.append(" ")
        texto.append("\n")
    return texto


def resolver_labirinto(labirinto: dict) -> list:
    """Devolve a lista de comandos que resolve o labirinto (entrada → saída).

    Implementa uma **busca em profundidade recursiva**. O retorno é a
    sequência de movimentos (ex.: ``["baixo", "direita", ...]``) que o
    jogador deve executar para chegar à saída.

    :param labirinto: O labirinto a resolver.
    :returns: Lista de nomes de movimentos; vazia se não houver solução.
    """
    grade = labirinto["grade"]
    saida = labirinto["saida"]
    visitados: set = set()
    caminho: list = []

    def _busca(pos: tuple) -> bool:
        """Visita recursivamente as células até alcançar a saída."""
        if pos == saida:
            return True
        visitados.add(pos)
        for nome, (dl, dc) in MOVIMENTOS.items():
            vizinho = (pos[0] + dl, pos[1] + dc)
            if vizinho in visitados:
                continue
            if 0 <= vizinho[0] < len(grade) and 0 <= vizinho[1] < len(grade[0]):
                if grade[vizinho[0]][vizinho[1]] == LIVRE:
                    caminho.append(nome)
                    if _busca(vizinho):
                        return True
                    caminho.pop()
        return False

    _busca(labirinto["inicio"])
    return caminho
