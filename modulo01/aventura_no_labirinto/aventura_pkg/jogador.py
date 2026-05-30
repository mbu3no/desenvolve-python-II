"""Módulo ``jogador``: estado, movimentação e pontuação do jogador.

A movimentação usa a biblioteca externa **pynput** para ler o teclado em
tempo real (setas ou teclas W/A/S/D). A pontuação aumenta ao coletar itens
espalhados pelo labirinto.

Funções principais:

* :func:`iniciar_jogador` — cria o jogador na posição inicial, zerando pontos.
* :func:`mover` — aplica um movimento (lógica pura, com ``match``/``case``).
* :func:`pontuar` — coleta o item da célula atual, somando pontos.
* :func:`jogar` — laço principal que lê o teclado (pynput) até vitória,
  derrota ou saída.
"""

from pynput import keyboard

from aventura_pkg.labirinto import MOVIMENTOS, PAREDE


def iniciar_jogador(nome: str, labirinto: dict) -> dict:
    """Cria o dicionário de estado do jogador na posição inicial.

    :param nome: Nome do(a) jogador(a), usado nas mensagens da tela.
    :param labirinto: O labirinto onde o jogador será posicionado.
    :returns: Dicionário ``{"nome", "pos", "pontos", "movimentos", "itens"}``.
    """
    return {
        "nome": nome,
        "pos": list(labirinto["inicio"]),
        "pontos": 0,
        "movimentos": 0,
        "itens": 0,
    }


def mover(jogador: dict, labirinto: dict, direcao: str) -> bool:
    """Move o jogador em uma direção, se não houver parede no caminho.

    O deslocamento correspondente a cada direção é obtido com um
    ``match``/``case``.

    :param jogador: Estado do jogador (alterado no local).
    :param labirinto: O labirinto atual.
    :param direcao: ``"cima"``, ``"baixo"``, ``"esquerda"`` ou ``"direita"``.
    :returns: ``True`` se o jogador se moveu; ``False`` se bateu numa parede
        ou a direção é inválida.
    """
    match direcao:
        case "cima" | "baixo" | "esquerda" | "direita":
            dl, dc = MOVIMENTOS[direcao]
        case _:
            return False

    nova_l = jogador["pos"][0] + dl
    nova_c = jogador["pos"][1] + dc
    grade = labirinto["grade"]

    if not (0 <= nova_l < len(grade) and 0 <= nova_c < len(grade[0])):
        return False
    if grade[nova_l][nova_c] == PAREDE:
        return False

    jogador["pos"] = [nova_l, nova_c]
    jogador["movimentos"] += 1
    return True


def pontuar(jogador: dict, labirinto: dict) -> int:
    """Coleta o item da posição atual do jogador, se houver, somando pontos.

    :param jogador: Estado do jogador (alterado no local).
    :param labirinto: O labirinto atual (o item coletado é removido dele).
    :returns: A quantidade de pontos ganhos nesta jogada (0 se não havia item).
    """
    pos = tuple(jogador["pos"])
    if pos in labirinto["itens"]:
        ganho = labirinto["itens"].pop(pos)
        jogador["pontos"] += ganho
        jogador["itens"] += 1
        return ganho
    return 0


def _tecla_para_direcao(tecla) -> str | None:
    """Traduz uma tecla do pynput para o nome de uma direção (ou ``None``).

    Reconhece as setas e as teclas W/A/S/D usando ``match``/``case``.

    :param tecla: O evento de tecla recebido do listener do pynput.
    :returns: O nome da direção, ou ``None`` se a tecla não for de movimento.
    """
    match tecla:
        case keyboard.Key.up:
            return "cima"
        case keyboard.Key.down:
            return "baixo"
        case keyboard.Key.left:
            return "esquerda"
        case keyboard.Key.right:
            return "direita"

    caractere = getattr(tecla, "char", None)
    if caractere is None:
        return None
    match caractere.lower():
        case "w":
            return "cima"
        case "s":
            return "baixo"
        case "a":
            return "esquerda"
        case "d":
            return "direita"
        case _:
            return None


def jogar(labirinto: dict, jogador: dict, desenhar, max_movimentos: int | None = None) -> str:
    """Executa o laço principal do jogo lendo o teclado com pynput.

    A cada tecla de movimento válida o jogador anda, pontua e a tela é
    redesenhada. O laço termina ao alcançar a saída (vitória), ao esgotar o
    limite de movimentos (derrota) ou ao pressionar ESC (saída).

    :param labirinto: O labirinto sendo jogado.
    :param jogador: O estado do jogador.
    :param desenhar: Função sem argumentos que redesenha a tela do jogo.
    :param max_movimentos: Limite opcional de movimentos antes da derrota.
    :returns: ``"vitoria"``, ``"derrota"`` ou ``"saiu"``.
    """
    desenhar()
    estado = {"fim": "saiu"}

    def ao_pressionar(tecla):
        """Trata cada tecla pressionada durante a partida."""
        if tecla == keyboard.Key.esc:
            estado["fim"] = "saiu"
            return False

        direcao = _tecla_para_direcao(tecla)
        if direcao is None:
            return None

        if mover(jogador, labirinto, direcao):
            pontuar(jogador, labirinto)
            desenhar()
            if tuple(jogador["pos"]) == labirinto["saida"]:
                estado["fim"] = "vitoria"
                return False
            if max_movimentos is not None and jogador["movimentos"] >= max_movimentos:
                estado["fim"] = "derrota"
                return False
        return None

    with keyboard.Listener(on_press=ao_pressionar) as ouvinte:
        ouvinte.join()

    return estado["fim"]
