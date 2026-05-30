"""Pacote ``personalizador``.

Reúne módulos que envolvem texto com recursos da biblioteca ``rich`` para
exibição formatada no terminal. Cada módulo concentra um tipo de recurso:

==  ==========  ==================================================
id  módulo      recurso do rich
==  ==========  ==================================================
1   layout      divisão da tela em regiões (``rich.layout.Layout``)
2   painel      caixas/painéis (``rich.panel.Panel``)
3   progresso   barras de progresso (``rich.progress``)
4   estilo      cores e estilos de texto (``rich.style``)
==  ==========  ==================================================

Todos os módulos expõem funções com a mesma assinatura
``funcao(texto: str, isArquivo: bool = False)``, o que permite escolhê-las
de forma uniforme pela interface de linha de comando em ``main.py``.
"""

from personalizador import layout, painel, progresso, estilo

__all__ = ["layout", "painel", "progresso", "estilo"]
