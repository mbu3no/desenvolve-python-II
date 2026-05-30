"""Módulo ``painel``: exibe texto usando o recurso de painel do ``rich``.

O ``rich.panel.Panel`` desenha uma moldura ao redor do conteúdo, com título,
subtítulo, cor de borda e estilos configuráveis. É ideal para destacar
mensagens no terminal.

Funções disponíveis:

==  ====================  =================================================
id  função                descrição
==  ====================  =================================================
1   simples               painel com borda arredondada e título
2   destacado             painel colorido e centralizado, com subtítulo
==  ====================  =================================================
"""

from rich.console import Console
from rich.panel import Panel
from rich.box import ROUNDED, DOUBLE

from personalizador._comum import obter_texto

console = Console()


def simples(texto: str, isArquivo: bool = False) -> None:
    """Exibe o texto dentro de um painel simples de bordas arredondadas.

    :param texto: A string a imprimir ou o caminho de um arquivo de texto.
    :param isArquivo: Quando ``True``, ``texto`` é o caminho de um arquivo.
    """
    conteudo = obter_texto(texto, isArquivo)

    painel = Panel(conteudo, title="Painel", box=ROUNDED, border_style="cyan")
    console.print(painel)


def destacado(texto: str, isArquivo: bool = False) -> None:
    """Exibe o texto em um painel chamativo, com borda dupla e centralizado.

    O conteúdo é centralizado, exibido em magenta e cercado por uma borda
    dupla amarela, com título e subtítulo.

    :param texto: A string a imprimir ou o caminho de um arquivo de texto.
    :param isArquivo: Quando ``True``, ``texto`` é o caminho de um arquivo.
    """
    conteudo = obter_texto(texto, isArquivo)

    painel = Panel(
        f"[bold magenta]{conteudo}[/bold magenta]",
        title="[bold yellow]:: DESTAQUE ::[/bold yellow]",
        subtitle="[dim]personalizador.painel.destacado[/dim]",
        box=DOUBLE,
        border_style="yellow",
        padding=(1, 4),
    )
    console.print(painel, justify="center")
