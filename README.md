# Descobrindo padrões: a jornada para sincronizar dados complexos

```
  ███████ ██    ██ ███    ██  ██████
  ██       ██  ██  ████   ██ ██         S Y N C P A T T E R N S
  ███████   ████   ██ ██  ██ ██         > PRESS START
       ██    ██    ██  ██ ██ ██
  ███████    ██    ██   ████  ██████     Helena  VS  Marcus
```

> **INSERT COIN.** Dois analistas, dois registros do mesmo fenômeno. Sua missão: encontrar
> todas as maiores subsequências comuns e sincronizar os dados antes do `GAME OVER`.

- **Disciplina:** Fundamentos de Projeto e Análise de Algoritmos
- **Curso:** Sistemas de Informação, PUC Minas, campus Contagem
- **Professora:** Amália Vasconcelos
- **Problema:** Encontrar **todas as Maiores Subsequências Comuns (LCS) distintas** entre duas sequências de eventos, em ordem alfabética.

## Integrantes do grupo

- Daniel Heringer
- Lucas Borges de Freitas
- Mateus Botelho de Souza
- Victor Alves Alcântara
- Vitor Mendonça Braga
- Iago Gonçalves Moysés

## Arquivos da entrega

| Arquivo | Descrição |
|---|---|
| `lcs_dp.py` | Solução usando **somente Programação Dinâmica** (tabela de conjuntos). |
| `lcs_dp_backtracking.py` | Solução usando **Programação Dinâmica + Backtracking**. |
| `README.md` | Este arquivo: descrição da solução e respostas às perguntas. |
| `interface_grafica.html` | **Interface gráfica interativa** (diferencial dos +3 pontos). Abrir no navegador. |
| `apresentacao.html` | **Apresentação de slides** (estética 8-bit, rolagem com scroll-snap). Abrir no navegador. Para gerar o PDF: Ctrl+P, destino "Salvar como PDF", layout paisagem. |
| `apresentacao.pptx` | Versão em PowerPoint da apresentação (alternativa para a entrega formal em .pptx). |

## Como executar

As duas soluções leem da **entrada padrão** (stdin) e escrevem na **saída padrão** (stdout), exatamente no formato do roteiro.

```bash
# a partir de um arquivo de entrada
python3 lcs_dp.py < entrada.txt
python3 lcs_dp_backtracking.py < entrada.txt

# ou digitando manualmente (encerre com Ctrl+D / Ctrl+Z)
python3 lcs_dp.py
```

**Formato da entrada:** a 1ª linha contém `D` (número de conjuntos, `D ≤ 10`); cada conjunto tem 2 linhas (sequência de Helena e sequência de Marcus), com 1 a 80 letras minúsculas.

**Exemplo (do roteiro):**

```
Entrada:                 Saída:
1                        ijiji
ijkijkii                 ijiki
ikjikji                  ijkji
                         ikiji
                         ikiki
                         ikjii
                         ikjki
```

A **interface gráfica** (`interface_grafica.html`) é autocontida (um único arquivo, sem dependências) e mostra, passo a passo: a história de Helena e Marcus, a construção animada da tabela de PD célula a célula, a ramificação do backtracking gerando cada LCS, e o resultado final em ordem alfabética.

---

## Descrição da solução

O problema é o de encontrar **todas** as Maiores Subsequências Comuns (LCS) distintas de duas cadeias. Uma subsequência preserva a ordem dos caracteres, mas pode pular posições. A novidade em relação à LCS clássica é que pode existir **mais de uma** subsequência de tamanho máximo, e precisamos listar **todas, sem repetição e em ordem alfabética**.

Adotamos duas abordagens, conforme exigido:

1. **Somente PD** (`lcs_dp.py`): cada célula `dp[i][j]` guarda o **conjunto de todas as LCS** dos prefixos `Helena[0..i-1]` e `Marcus[0..j-1]`. A tabela é preenchida de baixo para cima e a enumeração das múltiplas soluções emerge naturalmente das **uniões de conjuntos** quando há empate, sem nenhuma recursão.
2. **PD + Backtracking** (`lcs_dp_backtracking.py`): construímos apenas a tabela de **comprimentos** (LCS clássica, barata em memória) e, depois, percorremos a tabela de trás para frente, **ramificando em todos os caminhos ótimos** para reconstruir cada LCS. A recursão é **memoizada** para não recalcular subproblemas.

---

## Perguntas

### 1. Como a programação dinâmica foi aplicada na solução?

A PD foi aplicada na clássica recorrência da LCS sobre **prefixos**. Definimos `dp[i][j]` como uma propriedade da melhor solução para `Helena[0..i-1]` e `Marcus[0..j-1]`, partindo de subproblemas menores já resolvidos (**subestrutura ótima**) e reutilizando esses resultados (**sobreposição de subproblemas**):

- Se `Helena[i-1] == Marcus[j-1]` (as letras casam), o caractere pertence à LCS e:
  `comprimento[i][j] = comprimento[i-1][j-1] + 1`.
- Caso contrário:
  `comprimento[i][j] = max(comprimento[i-1][j], comprimento[i][j-1])`.

Os casos-base são os prefixos vazios (`i = 0` ou `j = 0`), cujo comprimento é 0. A tabela é preenchida **bottom-up**, garantindo que toda célula consultada já foi calculada.

Na versão **somente PD**, estendemos a ideia: em vez de guardar só o número, cada célula guarda o **conjunto de todas as LCS** daquele prefixo. Quando as letras casam, anexamos o caractere a cada sequência do conjunto da diagonal; quando não casam, copiamos o conjunto da direção de maior comprimento; e, no **empate** entre cima e esquerda, fazemos a **união** dos dois conjuntos (o `set` elimina duplicatas automaticamente). Assim, toda a enumeração é feita apenas com tabulação, sem recursão.

### 2. Por que o uso de backtracking é necessário neste problema?

Porque a tabela de PD com comprimentos responde **"qual o tamanho da maior subsequência comum"**, mas **não diz quais são** as subsequências, e podem existir várias de tamanho máximo. Para **reconstruí-las**, é preciso voltar pela tabela a partir de `(m, n)` decidindo, em cada passo, de onde o valor ótimo veio:

- se as letras casam, a letra faz parte da LCS e seguimos na diagonal;
- se não casam, seguimos para a vizinha de maior comprimento.

O ponto crucial é o **empate** (`comprimento[i-1][j] == comprimento[i][j-1]`): nesse caso há **dois caminhos ótimos diferentes**, e cada um pode levar a uma LCS distinta. O backtracking **ramifica** e explora os dois lados, sendo a forma natural de **enumerar exaustivamente** todas as soluções ótimas. Uma simples reconstrução gulosa encontraria apenas **uma** LCS; o backtracking é o que garante encontrarmos **todas**.

### 3. Houve desafios na implementação? Quais? Como foram superados?

- **Eliminar duplicatas.** Caminhos diferentes na tabela podem gerar a **mesma** string. Resolvido usando `set`/`frozenset` para armazenar as subsequências, o que descarta repetições automaticamente.
- **Explosão combinatória / desempenho.** Sem cuidado, o backtracking reexploraria os mesmos subproblemas exponencialmente. Resolvido com **memoização** (`functools.lru_cache`) por célula `(i, j)`, reduzindo a uma quantidade polinomial de estados.
- **Ordem alfabética e formatação exata.** A saída deve estar ordenada e com **uma linha em branco entre conjuntos**. Resolvido com `sorted(...)` e juntando os blocos com `"\n\n"`.
- **Profundidade da recursão.** Com sequências de até 80 caracteres, a pilha padrão poderia ser insuficiente; elevamos o limite com `sys.setrecursionlimit`.
- **Validação das entradas.** Implementamos checagem de `D` (de 1 a 10), tamanho (de 1 a 80) e alfabeto (apenas letras de `a` a `z`), com mensagens de erro claras.

### 4. Qual é a complexidade da solução proposta? (cálculo passo a passo)

Sejam `m` e `n` os tamanhos das sequências de Helena e Marcus, `L = comprimento da LCS` (`L ≤ min(m, n) ≤ 80`), `R = número de LCS distintas` (garantido `R ≤ 1000`) e `K` o tamanho máximo de conjunto de subsequências mantido durante o processo.

#### Versão usando **apenas Programação Dinâmica**

1. **Inicialização das matrizes** `(m+1) × (n+1)`: `O(m·n)`.
2. **Dois laços aninhados** `i = 1..m`, `j = 1..n` → exatamente `m·n` iterações.
3. **Trabalho por célula:** além de `O(1)` para o comprimento, há a operação sobre conjuntos:
   - letras casam → criar novo conjunto anexando 1 caractere a cada string: custo `O(K·L)`;
   - empate → **união** de dois conjuntos de strings de tamanho até `L`: custo `O(K·L)` (o hash de cada string custa `O(L)`).
   Logo, cada célula custa `O(K·L)`.
4. **Total da tabela:** `m·n` células × `O(K·L)` = **`O(m·n·K·L)`**.
5. **Ordenação final:** ordenar `R` strings de tamanho `L`: `O(R·L·log R)`.

> **Resultado:** o cálculo **apenas dos comprimentos** é `Θ(m·n)`. Ao materializar **todas** as subsequências em **todas** as células, o tempo e o **espaço** sobem para **`O(m·n·K·L)`**. O custo (e a principal desvantagem) desta versão é o **alto uso de memória**, pois guarda conjuntos em cada célula.

#### Versão combinando **PD + Backtracking**

1. **Construção da tabela de comprimentos:** dois laços aninhados, `O(1)` por célula → **`Θ(m·n)` tempo e `Θ(m·n) espaço`** (guarda apenas inteiros, memória enxuta).
2. **Reconstrução por backtracking memoizado:** há no máximo `(m+1)·(n+1) = O(m·n)` estados distintos `(i, j)`; com memoização, cada um é calculado **uma única vez**.
3. **Trabalho por estado:** combina os resultados de até 2 filhos; no caso de casamento, anexa 1 caractere a cada uma das até `K` strings (`O(K·L)`); no empate, faz a união (`O(K·L)`). Custo por estado: `O(K·L)`.
4. **Total da enumeração:** `O(m·n)` estados × `O(K·L)` = **`O(m·n·K·L)`**.
5. **Ordenação final:** `O(R·L·log R)`.

> **Resultado:** **`O(m·n)`** para a tabela + **`O(m·n·K·L)`** para enumerar as soluções. A diferença prática para a versão anterior é o **espaço**: aqui a tabela usa apenas `O(m·n)` (inteiros), e os conjuntos só são construídos **sob demanda** ao longo dos caminhos ótimos, ficando bem mais econômico em memória.

**Observação (limite inferior):** como a saída pode conter `R` subsequências de tamanho `L`, qualquer algoritmo correto precisa de pelo menos `Ω(R·L)` só para **escrever** o resultado. Ambas as versões respeitam esse limite; o backtracking apenas o atinge gastando menos memória intermediária.

### 5. O que o grupo aprendeu ao resolver esse problema?

- Que **programação dinâmica e backtracking se complementam**: a PD calcula eficientemente o **ótimo** (o tamanho), e o backtracking **reconstrói** e **enumera** todas as soluções que atingem esse ótimo.
- A importância da **subestrutura ótima** e da **sobreposição de subproblemas** para reconhecer quando a PD se aplica.
- Que **empates na recorrência** são exatamente os pontos que geram **múltiplas soluções**, e que tratá-los corretamente (ramificando) é o que diferencia "achar uma LCS" de "achar todas".
- O papel da **memoização** para transformar uma busca exponencial em uma de custo polinomial nos estados.
- O **trade-off entre tempo e espaço**: dá para resolver tudo com PD pura (mais memória, mais simples) ou com PD + backtracking (tabela enxuta, reconstrução sob demanda).
- Cuidados de engenharia que também contam na nota: **validação de entradas**, **formatação exata da saída**, **legibilidade** e **comentários** no código.

## Referências

- CORMEN, T. H. et al. *Introduction to Algorithms*. 3. ed. MIT Press, 2009. (Cap. 15: Programação Dinâmica; seção da Longest Common Subsequence.)
- ZIVIANI, N. *Projeto de Algoritmos com implementações em Java e C++*. Cengage Learning.
- Documentação oficial do Python: `functools.lru_cache`. Disponível em: https://docs.python.org/3/library/functools.html
