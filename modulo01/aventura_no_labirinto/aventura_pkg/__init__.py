"""Pacote ``aventura_pkg`` — o jogo *Aventura no Labirinto*.

Reúne os três módulos do jogo:

* :mod:`aventura_pkg.labirinto` — geração (recursiva), exibição e resolução
  (recursiva) do labirinto, com itens colecionáveis.
* :mod:`aventura_pkg.jogador` — estado, movimentação (via **pynput**) e
  pontuação do jogador.
* :mod:`aventura_pkg.utils` — apresentação com **rich** (menu, instruções,
  telas finais, animação recursiva) e som de abertura.

O controle principal e a interface de linha de comando ficam em ``main.py``.
"""

from aventura_pkg import labirinto, jogador, utils

__all__ = ["labirinto", "jogador", "utils"]
