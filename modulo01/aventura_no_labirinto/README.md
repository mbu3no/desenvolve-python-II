# 🗺️ Aventura no Labirinto

Jogo de terminal onde você explora um **labirinto gerado aleatoriamente**,
coleta itens e tenta chegar à saída. Trabalho Prático I do Módulo 1 — exercita
recursão, `match-case`, ambiente virtual com bibliotecas externas, organização
modular, docstrings/documentação HTML e uma CLI com `argparse`.

Feito com [`rich`](https://github.com/Textualize/rich) (terminal colorido) e
[`pynput`](https://pynput.readthedocs.io/) (leitura do teclado).

## 🎮 Como jogar

- Mova o personagem **`@`** com as **setas** ou as teclas **W / A / S / D**.
- Colete os itens **`●`** (valem 10 pontos cada) no caminho até a saída **`⚑`**.
- As paredes são **`█`**. Pressione **ESC** para sair da partida.
- Chegue à saída para **vencer**; se houver limite de movimentos e ele acabar,
  você **perde**.

## 📦 Estrutura

```
aventura_no_labirinto/
├── aventura_pkg/
│   ├── __init__.py
│   ├── labirinto.py     # gera (recursivo), desenha e resolve (recursivo) o labirinto
│   ├── jogador.py       # estado, movimentação (pynput) e pontuação — usa match-case
│   └── utils.py         # menu, instruções, telas finais e animação recursiva (rich)
├── main.py              # CLI (argparse) + menu (match-case) + laço do jogo
├── instrucoes.txt       # instruções lidas pelo utils.imprime_instrucoes
├── requirements.txt
├── aventura_pkg.html    # documentação gerada com pydoc
└── README.md
```

## 🛠️ Instalação e execução

```powershell
# 1. Criar e ativar o ambiente virtual (Windows / PowerShell)
py -m venv venv
venv\Scripts\Activate.ps1

# 2. Instalar as dependências
pip install -r requirements.txt

# 3. Jogar (--name é obrigatório)
python main.py --name SeuNome
```

## ⚙️ Opções da CLI

| Opção                       | Descrição                                                    |
|-----------------------------|-------------------------------------------------------------|
| `--name <nome>`             | **(obrigatório)** Nome do(a) jogador(a).                     |
| `--color <cor>`             | Cor principal do jogo (nome de cor do `rich`). Padrão: cyan. |
| `--dificuldade {1,2,3}`     | Tamanho do labirinto: 1=fácil, 2=médio, 3=difícil.          |
| `--max-movimentos <n>`      | Limite de movimentos antes da derrota (sem limite por padrão). |
| `--disable-sound`           | Desativa o som de abertura.                                  |
| `--help`                    | Ajuda personalizada.                                         |

Exemplos:

```powershell
python main.py --name Bia --color magenta --dificuldade 3
python main.py --name Léo --disable-sound --max-movimentos 80
```

## 🧭 Menu

Ao iniciar, aparece um menu (controlado por `match-case`):

1. **Instruções** — lê e exibe `instrucoes.txt` formatado.
2. **Jogar** — gera o labirinto e inicia a partida.
3. **Assistir a solução automática** — usa a **busca recursiva** para resolver
   o labirinto e anima o personagem executando os movimentos.
4. **Sair**.

## ✅ Requisitos do trabalho atendidos

- **Função recursiva:** geração do labirinto (`_escavar`), resolução
  (`resolver_labirinto`) e animação de vitória (`animacao_vitoria`).
- **`match-case`:** menu principal, escolha de direção e tradução de teclas.
- **Ambiente virtual + `requirements.txt`:** `rich` e `pynput` instalados.
- **Modularidade:** pacote `aventura_pkg` com três módulos + `main.py`.
- **Docstrings + HTML:** todas as funções/módulos documentados; HTML em
  `aventura_pkg.html` (gerado com `pydoc`).
- **CLI:** 5 elementos no `argparse`, sendo `--name` obrigatório.

## 📚 Regenerar a documentação

```powershell
python -m pydoc -w aventura_pkg aventura_pkg.labirinto aventura_pkg.jogador aventura_pkg.utils main
```

## 🖼️ Telas

> _Substitua por prints reais rodando o jogo no seu terminal._
>
> - Menu principal
> - Labirinto em jogo (com `@`, `●`, `⚑`)
> - Tela de vitória com a animação de estrelas

## ⚠️ Observações

- O jogo lê o teclado com **pynput**, então precisa ser executado em um
  **terminal real** (PowerShell/Windows Terminal), não em saída redirecionada.
- O som de abertura usa `winsound` (Windows). Em outros sistemas ele é
  ignorado silenciosamente.
