#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
#  PUC Minas - campus Contagem
#  Sistemas de Informacao - Fundamentos de Projeto e Analise de Algoritmos
#  Profa. Amalia Vasconcelos
#
#  Trabalho pratico: "Descobrindo padroes - a jornada para sincronizar dados"
#  Problema: Todas as Maiores Subsequencias Comuns (LCS) distintas
#
#  ARQUIVO 2 de 2 -> SOLUCAO USANDO PROGRAMACAO DINAMICA + BACKTRACKING
#
#  Autores:
#    Daniel Heringer
#    Lucas Borges de Freitas
#    Mateus Botelho de Souza
#    Victor Alves Alcantara
#    Vitor Mendonca Braga
#    Iago Goncalves Moyses
#
#  Versao : 1.0
#  Data   : 23/06/2026
#  Python : 3.8+
# =============================================================================
#
#  IDEIA GERAL (Programacao Dinamica + Backtracking):
#  -------------------------------------------------------------------------
#  FASE 1 - PROGRAMACAO DINAMICA:
#     Construimos apenas a tabela de COMPRIMENTOS dp[i][j], que guarda o
#     tamanho da maior subsequencia comum dos prefixos A[0..i-1] e B[0..j-1].
#     Esta e a recorrencia classica da LCS:
#        - se A[i-1] == B[j-1]:  dp[i][j] = dp[i-1][j-1] + 1
#        - senao:                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
#     Custo: O(m*n) tempo e espaco. Ela NAO guarda as subsequencias em si,
#     apenas os tamanhos -> ocupa pouca memoria.
#
#  FASE 2 - BACKTRACKING:
#     A tabela de comprimentos sozinha nao lista as subsequencias, e podem
#     existir VARIAS LCS distintas. Para enumera-las TODAS, percorremos a
#     tabela de tras para frente, a partir da celula (m, n), seguindo
#     recursivamente TODOS os caminhos otimos:
#        - se os caracteres casam, ele faz parte da LCS -> anda na diagonal;
#        - se nao casam, seguimos para a(s) vizinha(s) cujo comprimento e o
#          maior. Quando ha EMPATE, o backtracking se RAMIFICA e explora os
#          dois caminhos -> e assim que descobrimos multiplas solucoes.
#     Usamos memoizacao (cache por celula) para nao recalcular sub-resultados
#     ja conhecidos, o que torna a enumeracao eficiente.
# =============================================================================

import sys
from functools import lru_cache

sys.setrecursionlimit(100000)


def validar_sequencia(seq, nome):
    """Valida uma sequencia de eventos conforme as regras do roteiro:
    entre 1 e 80 caracteres e somente letras minusculas de 'a' a 'z'."""
    if len(seq) < 1 or len(seq) > 80:
        sys.exit(
            "ERRO (sequencia de {}): deve ter entre 1 e 80 letras. "
            "Tamanho recebido: {}.".format(nome, len(seq))
        )
    for ch in seq:
        if not ("a" <= ch <= "z"):
            sys.exit(
                "ERRO (sequencia de {}): caractere invalido '{}'. "
                "Use apenas letras minusculas de 'a' a 'z'.".format(nome, ch)
            )


def construir_tabela_dp(a, b):
    """FASE 1 - Programacao Dinamica.
    Retorna a matriz dp de comprimentos da LCS (dimensoes (m+1) x (n+1))."""
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = dp[i - 1][j] if dp[i - 1][j] >= dp[i][j - 1] else dp[i][j - 1]
    return dp


def todas_lcs_dp_backtracking(a, b):
    """FASE 2 - Backtracking sobre a tabela de PD.
    Retorna o conjunto (set) de todas as maiores subsequencias comuns."""
    dp = construir_tabela_dp(a, b)

    @lru_cache(maxsize=None)
    def reconstruir(i, j):
        """Conjunto de todas as LCS dos prefixos a[:i] e b[:j],
        reconstruidas a partir da tabela dp por backtracking memoizado."""
        # Caso base: prefixo vazio -> unica subsequencia possivel e a vazia.
        if i == 0 or j == 0:
            return frozenset({""})

        if a[i - 1] == b[j - 1]:
            # Caractere casa -> pertence a toda LCS; anda na diagonal.
            return frozenset(s + a[i - 1] for s in reconstruir(i - 1, j - 1))

        # Nao casam: seguimos a(s) direcao(oes) de maior comprimento.
        resultado = set()
        if dp[i - 1][j] >= dp[i][j - 1]:
            resultado |= reconstruir(i - 1, j)        # caminho para cima
        if dp[i][j - 1] >= dp[i - 1][j]:
            resultado |= reconstruir(i, j - 1)        # caminho para esquerda
        # Quando dp[i-1][j] == dp[i][j-1], ambos os ramos sao explorados
        # (e aqui que o backtracking gera as multiplas solucoes).
        return frozenset(resultado)

    return set(reconstruir(len(a), len(b)))


def main():
    dados = sys.stdin.read().split("\n")
    pos = 0

    # Primeira linha: numero D de conjuntos de dados (D <= 10).
    while pos < len(dados) and dados[pos].strip() == "":
        pos += 1
    if pos >= len(dados):
        sys.exit("ERRO: entrada vazia. Esperava o numero D de conjuntos.")

    try:
        d = int(dados[pos].strip())
    except ValueError:
        sys.exit("ERRO: a primeira linha deve ser um inteiro D (quantidade de conjuntos).")
    pos += 1

    if d < 1 or d > 10:
        sys.exit("ERRO: D deve estar entre 1 e 10. Valor recebido: {}.".format(d))

    blocos_saida = []
    for _ in range(d):
        if pos >= len(dados):
            sys.exit("ERRO: faltou a sequencia de Helena de um dos conjuntos.")
        helena = dados[pos].strip()
        pos += 1
        if pos >= len(dados):
            sys.exit("ERRO: faltou a sequencia de Marcus de um dos conjuntos.")
        marcus = dados[pos].strip()
        pos += 1

        validar_sequencia(helena, "Helena")
        validar_sequencia(marcus, "Marcus")

        resultado = sorted(todas_lcs_dp_backtracking(helena, marcus))
        blocos_saida.append("\n".join(resultado))

    # Linha em branco entre blocos de conjuntos diferentes.
    print("\n\n".join(blocos_saida))


if __name__ == "__main__":
    main()

# Fim do arquivo lcs_dp_backtracking.py
