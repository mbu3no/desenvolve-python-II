"""Módulo ``progresso``: exibe texto usando o recurso de progresso do ``rich``.

O subpacote ``rich.progress`` fornece barras de progresso e spinners
animados. Aqui o texto é "processado" caractere a caractere (ou linha a
linha) enquanto uma barra/spinner é animada, e ao final o texto completo é
impresso.

Funções disponíveis:

==  ====================  =================================================
id  função                descrição
==  ====================  =================================================
1   barra                 anima uma barra de progresso e imprime o texto
2   girando               anima um spinner enquanto "carrega" o texto
==  ====================  =================================================
"""

import time

from rich.console import Console
from rich.progress import (
    Progress,
    SpinnerColumn,
    BarColumn,
    TextColumn,
    TimeElapsedColumn,
)

from personalizador._comum import obter_texto

console = Console()


def barra(texto: str, isArquivo: bool = False) -> None:
    """Anima uma barra de progresso revelando o texto caractere a caractere.

    A barra avança um passo por caractere do texto; ao terminar, o texto
    completo é impresso.

    :param texto: A string a imprimir ou o caminho de um arquivo de texto.
    :param isArquivo: Quando ``True``, ``texto`` é o caminho de um arquivo.
    """
    conteudo = obter_texto(texto, isArquivo)

    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console,
    ) as progresso:
        tarefa = progresso.add_task("Processando...", total=len(conteudo) or 1)
        for _ in conteudo or " ":
            time.sleep(0.01)
            progresso.advance(tarefa)

    console.print(conteudo)


def girando(texto: str, isArquivo: bool = False) -> None:
    """Anima um spinner por um curto período e então imprime o texto.

    Simula um carregamento exibindo um spinner com a mensagem "Carregando"
    durante alguns instantes antes de mostrar o conteúdo.

    :param texto: A string a imprimir ou o caminho de um arquivo de texto.
    :param isArquivo: Quando ``True``, ``texto`` é o caminho de um arquivo.
    """
    conteudo = obter_texto(texto, isArquivo)

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold green]{task.description}"),
        transient=True,
        console=console,
    ) as progresso:
        tarefa = progresso.add_task("Carregando o texto...", total=None)
        for _ in range(30):
            time.sleep(0.03)
            progresso.advance(tarefa)

    console.print(f"[bold green][OK][/bold green] {conteudo}")
