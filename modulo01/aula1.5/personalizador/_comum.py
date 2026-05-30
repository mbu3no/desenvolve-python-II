"""Funções utilitárias internas compartilhadas pelos módulos do pacote.

Este módulo não faz parte da interface pública; ele apenas evita a
duplicação da lógica de "obter o texto a ser exibido" em cada módulo.
"""


def obter_texto(texto: str, isArquivo: bool = False) -> str:
    """Retorna o conteúdo a ser exibido pelas funções do pacote.

    :param texto: A string a imprimir ou o caminho de um arquivo de texto.
    :param isArquivo: Quando ``True``, ``texto`` é tratado como o caminho de
        um arquivo e o conteúdo desse arquivo é lido e retornado. Quando
        ``False`` (padrão), a própria string ``texto`` é retornada.
    :returns: O texto pronto para ser formatado e impresso.
    :raises FileNotFoundError: Se ``isArquivo`` for ``True`` e o arquivo não
        existir.
    """
    if isArquivo:
        with open(texto, "r", encoding="utf-8") as arquivo:
            return arquivo.read()
    return texto
