"""Módulo ``utils``: funções utilitárias de apresentação (rich) e som.

Concentra a parte "visual" do jogo para manter o ``main.py`` enxuto:
impressão do menu, das instruções (lidas de um arquivo), das telas de
vitória/derrota e uma animação **recursiva** de comemoração. Também oferece
um som de abertura opcional (via ``winsound``, no Windows).

Funções principais:

* :func:`imprime_instrucoes` — lê um arquivo de texto e o imprime formatado.
* :func:`imprimir_menu` — desenha o menu principal do jogo.
* :func:`tela_vitoria` / :func:`tela_derrota` — telas finais.
* :func:`animacao_vitoria` — animação **recursiva** de comemoração.
* :func:`tocar_som_abertura` — toca um jingle de abertura (opcional).
"""

import time
import threading

from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.text import Text


def imprimir_banner(console: Console, cor: str = "cyan") -> None:
    """Imprime o título/banner do jogo em um painel destacado.

    :param console: O console rich usado para imprimir.
    :param cor: Cor principal do banner.
    """
    titulo = Text("AVENTURA NO LABIRINTO", style=f"bold {cor}", justify="center")
    console.print(Panel(titulo, border_style=cor, subtitle="módulo 1 • trabalho prático I"))


def imprimir_menu(console: Console, nome: str, cor: str = "cyan") -> None:
    """Desenha o menu principal do jogo.

    :param console: O console rich usado para imprimir.
    :param nome: Nome do(a) jogador(a), exibido na saudação.
    :param cor: Cor principal usada na borda do menu.
    """
    opcoes = Text()
    opcoes.append("  [1] ", style="bold yellow")
    opcoes.append("Instruções\n")
    opcoes.append("  [2] ", style="bold yellow")
    opcoes.append("Jogar\n")
    opcoes.append("  [3] ", style="bold yellow")
    opcoes.append("Assistir a solução automática\n")
    opcoes.append("  [4] ", style="bold yellow")
    opcoes.append("Sair")

    console.print(
        Panel(opcoes, title=f"Olá, [bold]{nome}[/bold]! O que deseja?", border_style=cor)
    )


def imprime_instrucoes(console: Console, caminho_arquivo: str, cor: str = "cyan") -> None:
    """Lê as instruções de um arquivo de texto e as imprime formatadas.

    :param console: O console rich usado para imprimir.
    :param caminho_arquivo: Caminho do arquivo de texto com as instruções.
    :param cor: Cor principal usada na borda do painel.
    """
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read()
    except FileNotFoundError:
        conteudo = "[red]Arquivo de instruções não encontrado.[/red]"

    console.print(Panel(conteudo, title="Como jogar", border_style=cor, padding=(1, 2)))


def tela_vitoria(console: Console, jogador: dict, cor: str = "green") -> None:
    """Mostra a tela de vitória com a pontuação final e uma animação.

    :param console: O console rich usado para imprimir.
    :param jogador: O estado final do jogador (nome, pontos, etc.).
    :param cor: Cor principal da tela.
    """
    animacao_vitoria(console)
    resumo = Text(justify="center")
    resumo.append(f"Parabéns, {jogador['nome']}! 🏆\n\n", style=f"bold {cor}")
    resumo.append(f"Itens coletados: {jogador['itens']}\n")
    resumo.append(f"Movimentos: {jogador['movimentos']}\n")
    resumo.append(f"Pontuação final: {jogador['pontos']}", style="bold yellow")
    console.print(Panel(Align.center(resumo), title="VITÓRIA!", border_style=cor, padding=(1, 4)))


def tela_derrota(console: Console, jogador: dict, cor: str = "red") -> None:
    """Mostra a tela de derrota (limite de movimentos esgotado).

    :param console: O console rich usado para imprimir.
    :param jogador: O estado final do jogador.
    :param cor: Cor principal da tela.
    """
    resumo = Text(justify="center")
    resumo.append(f"Que pena, {jogador['nome']}...\n\n", style=f"bold {cor}")
    resumo.append("Você ficou sem movimentos antes de achar a saída.\n")
    resumo.append(f"Pontuação: {jogador['pontos']}", style="bold yellow")
    console.print(Panel(Align.center(resumo), title="DERROTA", border_style=cor, padding=(1, 4)))


def animacao_vitoria(console: Console, nivel: int = 1, maximo: int = 6) -> None:
    """Desenha **recursivamente** uma árvore de estrelas que cresce na tela.

    Cada chamada imprime uma linha de estrelas e chama a si mesma para o
    próximo nível, até atingir ``maximo`` — caracterizando a recursão.

    :param console: O console rich usado para imprimir.
    :param nivel: Nível atual da animação (linha sendo desenhada).
    :param maximo: Nível máximo (condição de parada da recursão).
    """
    if nivel > maximo:
        return
    espacos = " " * (maximo - nivel)
    estrelas = "✦ " * nivel
    console.print(f"{espacos}{estrelas}", style="bold yellow", justify="center")
    time.sleep(0.12)
    animacao_vitoria(console, nivel + 1, maximo)


def tocar_som_abertura(desligado: bool = False) -> None:
    """Toca um pequeno jingle de abertura em uma thread separada (Windows).

    Usa o módulo ``winsound`` da biblioteca padrão. Em outros sistemas, ou
    quando ``desligado`` é ``True``, a função simplesmente não faz nada.

    :param desligado: Se ``True``, não toca som algum (ver opção
        ``--disable-sound`` da CLI).
    """
    if desligado:
        return
    try:
        import winsound
    except ImportError:
        return

    def _tocar():
        """Reproduz a sequência de notas do jingle."""
        for frequencia, duracao in [(523, 150), (659, 150), (784, 150), (1047, 300)]:
            winsound.Beep(frequencia, duracao)

    threading.Thread(target=_tocar, daemon=True).start()
