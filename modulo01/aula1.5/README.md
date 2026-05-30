# Aula 1.5 — Pacote `personalizador`

Programa que imprime um texto (ou o conteúdo de um arquivo) formatado com a
biblioteca [`rich`](https://rich.readthedocs.io/), escolhendo o módulo e a
função desejados por **nome** ou por **id** via linha de comando.

## Estrutura

```
aula1.5/
├── personalizador/        # pacote
│   ├── __init__.py
│   ├── _comum.py          # utilitário interno (lê string ou arquivo)
│   ├── layout.py          # módulo 1 -> colunas (1), linhas (2)
│   ├── painel.py          # módulo 2 -> simples (1), destacado (2)
│   ├── progresso.py       # módulo 3 -> barra (1), girando (2)
│   └── estilo.py          # módulo 4 -> colorido (1), arco_iris (2)
├── main.py                # interface de linha de comando (argparse)
├── docs/                  # documentação HTML gerada com pydoc
├── exemplo.txt            # arquivo de teste para a opção -a
├── requirements.txt
└── venv/                  # ambiente virtual
```

## Como usar

```bash
# 1. Ativar o ambiente virtual (Windows / PowerShell)
venv\Scripts\Activate.ps1

# 2. (Se necessário) instalar as dependências
pip install -r requirements.txt

# 3. Executar
python main.py "Olá, mundo!"
python main.py "Em destaque" -m painel -f destacado
python main.py "Por id" -m 4 -f 2
python main.py exemplo.txt -a -m estilo -f colorido
python main.py -h          # ajuda completa com todas as opções
```

## Argumentos da CLI

| Argumento        | Descrição                                                          |
|------------------|--------------------------------------------------------------------|
| `texto`          | Obrigatório. Texto a imprimir ou caminho do arquivo (com `-a`).    |
| `-a, --arquivo`  | Indica que `texto` é o caminho de um arquivo de texto.             |
| `-m, --modulo`   | Módulo (nome ou id): `1=layout`, `2=painel`, `3=progresso`, `4=estilo`. |
| `-f, --funcao`   | Função do módulo (nome ou id `1`/`2`).                             |

## Documentação

A documentação HTML do pacote está em `docs/`, gerada com:

```bash
python -m pydoc -w personalizador personalizador.layout personalizador.painel personalizador.progresso personalizador.estilo main
```

Abra `docs/personalizador.html` no navegador.
