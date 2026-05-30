"""Interface de linha de comando do pacote ``personalizador``.

Permite imprimir um texto (ou o conteúdo de um arquivo) formatado com os
recursos da biblioteca ``rich``, escolhendo o módulo e a função desejados
por nome ou por id.

Exemplos de uso (com o ambiente virtual ativado)::

    python main.py "Olá, mundo!"
    python main.py "Olá" -m painel -f destacado
    python main.py "Olá" -m 4 -f 2
    python main.py texto.txt -a -m estilo -f arco_iris

Para ver a ajuda completa::

    python main.py -h
"""

import argparse

from personalizador import layout, painel, progresso, estilo

# Registro dos módulos: cada um com um id, o módulo importado e suas funções.
# As funções também recebem um id (1 e 2) para permitir a escolha por número.
MODULOS = {
    "layout": {
        "id": "1",
        "modulo": layout,
        "funcoes": {
            "colunas": {"id": "1", "func": layout.colunas},
            "linhas": {"id": "2", "func": layout.linhas},
        },
    },
    "painel": {
        "id": "2",
        "modulo": painel,
        "funcoes": {
            "simples": {"id": "1", "func": painel.simples},
            "destacado": {"id": "2", "func": painel.destacado},
        },
    },
    "progresso": {
        "id": "3",
        "modulo": progresso,
        "funcoes": {
            "barra": {"id": "1", "func": progresso.barra},
            "girando": {"id": "2", "func": progresso.girando},
        },
    },
    "estilo": {
        "id": "4",
        "modulo": estilo,
        "funcoes": {
            "colorido": {"id": "1", "func": estilo.colorido},
            "arco_iris": {"id": "2", "func": estilo.arco_iris},
        },
    },
}


def resolver_modulo(escolha: str) -> str:
    """Converte o valor de ``-m`` (nome ou id) no nome do módulo.

    :param escolha: O nome do módulo (ex.: ``"painel"``) ou seu id (ex.: ``"2"``).
    :returns: O nome canônico do módulo.
    :raises SystemExit: Se a escolha não corresponder a nenhum módulo.
    """
    for nome, dados in MODULOS.items():
        if escolha == nome or escolha == dados["id"]:
            return nome
    validos = ", ".join(f"{d['id']}={n}" for n, d in MODULOS.items())
    raise SystemExit(f"Módulo inválido: {escolha!r}. Opções: {validos}.")


def resolver_funcao(nome_modulo: str, escolha: str):
    """Converte o valor de ``-f`` (nome ou id) na função a ser executada.

    :param nome_modulo: O nome canônico do módulo já resolvido.
    :param escolha: O nome da função ou seu id (``"1"`` ou ``"2"``).
    :returns: A função do módulo correspondente à escolha.
    :raises SystemExit: Se a escolha não corresponder a nenhuma função.
    """
    funcoes = MODULOS[nome_modulo]["funcoes"]
    for nome, dados in funcoes.items():
        if escolha == nome or escolha == dados["id"]:
            return dados["func"]
    validos = ", ".join(f"{d['id']}={n}" for n, d in funcoes.items())
    raise SystemExit(
        f"Função inválida: {escolha!r} para o módulo {nome_modulo!r}. "
        f"Opções: {validos}."
    )


def _ajuda_modulos() -> str:
    """Monta o texto de ajuda listando os módulos disponíveis."""
    itens = [f"{d['id']}={n}" for n, d in MODULOS.items()]
    return "Módulo a acessar (nome ou id). Opções: " + ", ".join(itens)


def _ajuda_funcoes() -> str:
    """Monta o texto de ajuda listando as funções de cada módulo."""
    linhas = []
    for nome, dados in MODULOS.items():
        funcs = ", ".join(
            f"{d['id']}={f}" for f, d in dados["funcoes"].items()
        )
        linhas.append(f"{nome}: {funcs}")
    return "Função a acessar (nome ou id). Opções por módulo -> " + " | ".join(linhas)


def criar_parser() -> argparse.ArgumentParser:
    """Cria e configura o ``argparse.ArgumentParser`` da aplicação.

    :returns: O parser com todos os argumentos e opções configurados.
    """
    parser = argparse.ArgumentParser(
        prog="main.py",
        description="Imprime um texto formatado com os recursos da biblioteca rich.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "texto",
        help="Texto a imprimir OU caminho do arquivo (use -a neste caso).",
    )
    parser.add_argument(
        "-a",
        "--arquivo",
        action="store_true",
        help="Indica que o argumento 'texto' é o caminho de um arquivo de texto.",
    )
    parser.add_argument(
        "-m",
        "--modulo",
        default="painel",
        help=_ajuda_modulos() + " (padrão: painel)",
    )
    parser.add_argument(
        "-f",
        "--funcao",
        default="1",
        help=_ajuda_funcoes() + " (padrão: a primeira função do módulo)",
    )
    return parser


def main() -> None:
    """Ponto de entrada: lê os argumentos e executa a função escolhida."""
    parser = criar_parser()
    args = parser.parse_args()

    nome_modulo = resolver_modulo(args.modulo)
    funcao = resolver_funcao(nome_modulo, args.funcao)

    try:
        funcao(args.texto, args.arquivo)
    except FileNotFoundError:
        raise SystemExit(f"Arquivo não encontrado: {args.texto!r}")


if __name__ == "__main__":
    main()
