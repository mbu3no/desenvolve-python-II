"""Módulo ``estilo``: exibe texto usando o recurso de estilo do ``rich``.

A classe ``rich.style.Style`` e a marcação de console do ``rich`` permitem
aplicar cores, negrito, itálico, sublinhado e fundo ao texto. Aqui o texto
fornecido é impresso com diferentes combinações de estilo.

Funções disponíveis:

==  ====================  =================================================
id  função                descrição
==  ====================  =================================================
1   colorido              imprime em negrito com cor de frente e de fundo
2   arco_iris             imprime cada caractere com uma cor diferente
==  ====================  =================================================
"""

from rich.console import Console
from rich.style import Style
from rich.text import Text

from personalizador._comum import obter_texto

console = Console()


def colorido(texto: str, isArquivo: bool = False) -> None:
    """Imprime o texto em negrito branco sobre fundo azul, sublinhado.

    Demonstra a construção explícita de um ``rich.style.Style``.

    :param texto: A string a imprimir ou o caminho de um arquivo de texto.
    :param isArquivo: Quando ``True``, ``texto`` é o caminho de um arquivo.
    """
    conteudo = obter_texto(texto, isArquivo)

    estilo = Style(color="white", bgcolor="blue", bold=True, underline=True)
    console.print(conteudo, style=estilo)


def arco_iris(texto: str, isArquivo: bool = False) -> None:
    """Imprime o texto colorindo cada caractere com uma cor do arco-íris.

    As cores se repetem em ciclo ao longo dos caracteres, criando um efeito
    de gradiente colorido.

    :param texto: A string a imprimir ou o caminho de um arquivo de texto.
    :param isArquivo: Quando ``True``, ``texto`` é o caminho de um arquivo.
    """
    conteudo = obter_texto(texto, isArquivo)

    cores = ["red", "orange1", "yellow", "green", "cyan", "blue", "magenta"]
    resultado = Text()
    for indice, caractere in enumerate(conteudo):
        resultado.append(caractere, style=Style(color=cores[indice % len(cores)], bold=True))
    console.print(resultado)
