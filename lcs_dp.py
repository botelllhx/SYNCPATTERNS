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
#  ARQUIVO 1 de 2 -> SOLUCAO USANDO SOMENTE PROGRAMACAO DINAMICA
#
#  Autores:
#    Daniel Heringer
#    Lucas Borges de Freitas
#    Mateus Botelho de Souza
#    Victor Alves Alcantara
#    Vitor Mendonca Braga
#    Iago Goncalves Moyses
#    [adicionar 7o/8o integrante - o roteiro exige grupo de 7 ou 8]
#
#  Versao : 1.0
#  Data   : 23/06/2026
#  Python : 3.8+
# =============================================================================
#
#  IDEIA GERAL (somente Programacao Dinamica):
#  -------------------------------------------------------------------------
#  Em vez de guardar apenas o COMPRIMENTO da maior subsequencia comum em
#  cada celula (LCS classica), guardamos em cada celula dp[i][j] o CONJUNTO
#  de TODAS as maiores subsequencias comuns dos prefixos:
#       A[0..i-1]  e  B[0..j-1]
#
#  A tabela e preenchida de baixo para cima (bottom-up), celula a celula,
#  sem nenhuma chamada recursiva e sem backtracking. Toda a enumeracao das
#  multiplas solucoes emerge naturalmente da combinacao dos conjuntos
#  guardados nas celulas vizinhas -> isto e Programacao Dinamica "pura".
#
#  Recorrencia:
#    - Se A[i-1] == B[j-1]:
#         o ultimo caractere pertence a TODA LCS desse prefixo, entao
#         dp[i][j] = { s + A[i-1]  para cada s em dp[i-1][j-1] }
#    - Caso contrario, olhamos o comprimento (len[i][j]) das vizinhas:
#         se a de cima for maior  -> herda dp[i-1][j]
#         se a da esquerda maior  -> herda dp[i][j-1]
#         se houver EMPATE        -> UNIAO dos dois conjuntos (e aqui que
#                                    surgem as multiplas solucoes!)
# =============================================================================

import sys


def validar_sequencia(seq, indice_linha):
    """Valida uma sequencia de eventos conforme as regras do roteiro.

    Regras:
      - entre 1 e 80 caracteres;
      - somente letras minusculas de 'a' a 'z' (ate 26 tipos de eventos).
    Em caso de erro, encerra o programa com mensagem explicativa.
    """
    if len(seq) < 1 or len(seq) > 80:
        sys.exit(
            "ERRO (linha {}): a sequencia deve ter entre 1 e 80 letras. "
            "Tamanho recebido: {}.".format(indice_linha, len(seq))
        )
    for ch in seq:
        if not ("a" <= ch <= "z"):
            sys.exit(
                "ERRO (linha {}): caractere invalido '{}'. "
                "Use apenas letras minusculas de 'a' a 'z'.".format(indice_linha, ch)
            )


def todas_lcs_somente_dp(a, b):
    """Retorna o CONJUNTO de todas as maiores subsequencias comuns (LCS)
    de 'a' e 'b' usando exclusivamente programacao dinamica tabular.

    dp_len[i][j] -> comprimento da LCS dos prefixos a[:i] e b[:j]
    dp_set[i][j] -> conjunto (set) com todas as LCS desses prefixos
    """
    m, n = len(a), len(b)

    # Matriz de comprimentos (PD classica da LCS).
    dp_len = [[0] * (n + 1) for _ in range(m + 1)]

    # Matriz de conjuntos: cada celula guarda todas as LCS daquele prefixo.
    # As celulas da linha 0 e da coluna 0 representam prefixo vazio -> {""}.
    dp_set = [[None] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp_set[i][0] = {""}
    for j in range(n + 1):
        dp_set[0][j] = {""}

    # Preenchimento bottom-up, celula a celula.
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                # O caractere casa: ele entra ao final de toda LCS anterior.
                dp_len[i][j] = dp_len[i - 1][j - 1] + 1
                dp_set[i][j] = {s + a[i - 1] for s in dp_set[i - 1][j - 1]}
            else:
                cima = dp_len[i - 1][j]
                esquerda = dp_len[i][j - 1]
                if cima > esquerda:
                    dp_len[i][j] = cima
                    dp_set[i][j] = dp_set[i - 1][j]
                elif esquerda > cima:
                    dp_len[i][j] = esquerda
                    dp_set[i][j] = dp_set[i][j - 1]
                else:
                    # Empate: as duas direcoes oferecem LCS de mesmo tamanho.
                    # Unimos os conjuntos (set elimina duplicatas).
                    dp_len[i][j] = cima
                    dp_set[i][j] = dp_set[i - 1][j] | dp_set[i][j - 1]

    return dp_set[m][n]


def main():
    # Le toda a entrada de uma vez (stdin) e separa por linhas.
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
        # Sequencia de Helena.
        if pos >= len(dados):
            sys.exit("ERRO: faltou a sequencia de Helena de um dos conjuntos.")
        helena = dados[pos].strip()
        pos += 1
        # Sequencia de Marcus.
        if pos >= len(dados):
            sys.exit("ERRO: faltou a sequencia de Marcus de um dos conjuntos.")
        marcus = dados[pos].strip()
        pos += 1

        validar_sequencia(helena, "Helena")
        validar_sequencia(marcus, "Marcus")

        # Calcula todas as LCS e ordena alfabeticamente, sem repeticoes.
        resultado = sorted(todas_lcs_somente_dp(helena, marcus))
        blocos_saida.append("\n".join(resultado))

    # Linha em branco entre blocos de conjuntos diferentes.
    print("\n\n".join(blocos_saida))


if __name__ == "__main__":
    main()

# Fim do arquivo lcs_dp.py
