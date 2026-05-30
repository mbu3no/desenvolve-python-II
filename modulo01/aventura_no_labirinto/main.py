"""Aventura no Labirinto — controle principal e interface de linha de comando.

Este arquivo amarra os três módulos do pacote :mod:`aventura_pkg`:
gera o labirinto, controla o menu (com ``match``/``case``), executa o laço
do jogo lendo o teclado (pynput) e mostra as telas finais (rich).

Uso típico (com o ambiente virtual ativado)::

    python main.py --name Ana
    python main.py --name Bia --color magenta --dificuldade 3
    python main.py --name Léo --disable-sound --max-movimentos 80

Veja todas as opções com ``python main.py --help``.
"""

import sys
import time
import argparse

# Garante acentos/blocos unicode no terminal do Windows (evita cp1252).
try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

from rich.console import Console

from aventura_pkg import labirinto as lab
from aventura_pkg import jogador as jog
from aventura_pkg import utils

#: Caminho do arquivo de instruções, ao lado deste script.
ARQUIVO_INSTRUCOES = "instrucoes.txt"

console = Console()


def criar_parser() -> argparse.ArgumentParser:
    """Cria o parser da linha de comando com todas as opções do jogo.

    Define cinco elementos, sendo ``--name`` obrigatório.

    :returns: O ``argparse.ArgumentParser`` configurado.
    """
    parser = argparse.ArgumentParser(
        prog="main.py",
        description="🗺️  Aventura no Labirinto — explore, colete itens e ache a saída!",
        epilog="Dica: use as setas ou W/A/S/D para se mover. Divirta-se!",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--name",
        required=True,
        help="(obrigatório) Nome do(a) jogador(a).",
    )
    parser.add_argument(
        "--color",
        default="cyan",
        help="Cor principal do jogo (nome de cor do rich). Padrão: cyan.",
    )
    parser.add_argument(
        "--dificuldade",
        type=int,
        choices=[1, 2, 3],
        default=1,
        help="Tamanho do labirinto: 1=fácil, 2=médio, 3=difícil. Padrão: 1.",
    )
    parser.add_argument(
        "--max-movimentos",
        type=int,
        default=None,
        help="Limite de movimentos antes da derrota (sem limite por padrão).",
    )
    parser.add_argument(
        "--disable-sound",
        action="store_true",
        help="Desativa o som de abertura do jogo.",
    )
    return parser


def desenhar_jogo(labirinto: dict, jogador: dict, cor: str) -> None:
    """Limpa a tela e redesenha o labirinto com a barra de status.

    :param labirinto: O labirinto atual.
    :param jogador: O estado do jogador.
    :param cor: Cor principal do jogo.
    """
    console.clear()
    utils.imprimir_banner(console, cor)
    console.print(lab.imprimir_labirinto(labirinto, jogador, cor))
    console.print(
        f"[bold]{jogador['nome']}[/bold]   "
        f"Pontos: [yellow]{jogador['pontos']}[/yellow]   "
        f"Movimentos: {jogador['movimentos']}   "
        f"Itens restantes: {len(labirinto['itens'])}"
    )
    console.print("[dim]Mova-se com as setas ou W/A/S/D. ESC para sair.[/dim]")


def jogar_partida(args) -> None:
    """Cria um labirinto, executa a partida e mostra a tela final.

    :param args: Os argumentos já analisados da linha de comando.
    """
    labirinto = lab.criar_labirinto(args.dificuldade)
    jogador = jog.iniciar_jogador(args.name, labirinto)

    resultado = jog.jogar(
        labirinto,
        jogador,
        desenhar=lambda: desenhar_jogo(labirinto, jogador, args.color),
        max_movimentos=args.max_movimentos,
    )

    console.clear()
    match resultado:
        case "vitoria":
            utils.tela_vitoria(console, jogador, args.color)
        case "derrota":
            utils.tela_derrota(console, jogador)
        case _:
            console.print(f"[dim]Até a próxima, {jogador['nome']}![/dim]")


def assistir_solucao(args) -> None:
    """Resolve o labirinto pela busca recursiva e anima a solução na tela.

    :param args: Os argumentos já analisados da linha de comando.
    """
    labirinto = lab.criar_labirinto(args.dificuldade)
    jogador = jog.iniciar_jogador(args.name, labirinto)
    comandos = lab.resolver_labirinto(labirinto)

    desenhar_jogo(labirinto, jogador, args.color)
    time.sleep(0.6)
    for comando in comandos:
        jog.mover(jogador, labirinto, comando)
        jog.pontuar(jogador, labirinto)
        desenhar_jogo(labirinto, jogador, args.color)
        time.sleep(0.12)

    console.clear()
    utils.tela_vitoria(console, jogador, args.color)
    console.print(f"[dim]Solução com {len(comandos)} movimentos.[/dim]")


def menu_principal(args) -> None:
    """Mostra o menu repetidamente e despacha a opção escolhida (match-case).

    :param args: Os argumentos já analisados da linha de comando.
    """
    while True:
        console.clear()
        utils.imprimir_banner(console, args.color)
        utils.imprimir_menu(console, args.name, args.color)
        escolha = console.input("[bold]Escolha uma opção: [/bold]").strip()

        match escolha:
            case "1" | "instrucoes" | "instruções":
                console.clear()
                utils.imprime_instrucoes(console, ARQUIVO_INSTRUCOES, args.color)
                console.input("\n[dim]Pressione ENTER para voltar ao menu...[/dim]")
            case "2" | "jogar":
                jogar_partida(args)
                console.input("\n[dim]Pressione ENTER para voltar ao menu...[/dim]")
            case "3" | "assistir":
                assistir_solucao(args)
                console.input("\n[dim]Pressione ENTER para voltar ao menu...[/dim]")
            case "4" | "sair":
                console.print(f"[bold]Tchau, {args.name}![/bold] 👋")
                break
            case _:
                console.print("[red]Opção inválida. Tente novamente.[/red]")
                time.sleep(1)


def main() -> None:
    """Ponto de entrada: lê a CLI, toca o som de abertura e abre o menu."""
    args = criar_parser().parse_args()
    utils.tocar_som_abertura(args.disable_sound)
    try:
        menu_principal(args)
    except KeyboardInterrupt:
        console.print("\n[dim]Jogo encerrado.[/dim]")


if __name__ == "__main__":
    main()
