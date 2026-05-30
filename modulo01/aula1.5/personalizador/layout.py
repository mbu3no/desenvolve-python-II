"""Módulo ``layout``: exibe texto usando o recurso de layout do ``rich``.

O ``rich.layout.Layout`` permite dividir a tela do terminal em regiões
independentes. Aqui usamos esse recurso para apresentar o texto fornecido
distribuído em colunas ou linhas, cada região com sua própria moldura.

Funções disponíveis:

==  ====================  =================================================
id  função                descrição
==  ====================  =================================================
1   colunas               divide a tela em duas colunas lado a lado
2   linhas                divide a tela em três linhas (topo/meio/rodapé)
==  ====================  =================================================
"""

from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel

from personalizador._comum import obter_texto

console = Console()


def colunas(texto: str, isArquivo: bool = False) -> None:
    """Exibe o texto dividido em duas colunas lado a lado.

    A primeira coluna mostra o texto e a segunda mostra algumas
    estatísticas simples (quantidade de caracteres e de linhas), cada uma
    dentro de um painel próprio.

    :param texto: A string a imprimir ou o caminho de um arquivo de texto.
    :param isArquivo: Quando ``True``, ``texto`` é o caminho de um arquivo.
    """
    conteudo = obter_texto(texto, isArquivo)

    layout = Layout()
    layout.split_row(
        Layout(Panel(conteudo, title="Texto"), name="esquerda"),
        Layout(
            Panel(
                f"Caracteres: {len(conteudo)}\nLinhas: {len(conteudo.splitlines()) or 1}",
                title="Informações",
            ),
            name="direita",
        ),
    )
    console.print(layout)


def linhas(texto: str, isArquivo: bool = False) -> None:
    """Exibe o texto em três regiões empilhadas: topo, meio e rodapé.

    O topo e o rodapé recebem rótulos fixos e o texto fornecido é exibido na
    região central, evidenciando a divisão vertical da tela.

    :param texto: A string a imprimir ou o caminho de um arquivo de texto.
    :param isArquivo: Quando ``True``, ``texto`` é o caminho de um arquivo.
    """
    conteudo = obter_texto(texto, isArquivo)

    layout = Layout()
    layout.split_column(
        Layout(Panel("[bold]:: TOPO ::[/bold]"), name="topo", size=3),
        Layout(Panel(conteudo, title="Conteúdo"), name="meio"),
        Layout(Panel("[dim]:: RODAPÉ ::[/dim]"), name="rodape", size=3),
    )
    console.print(layout)
