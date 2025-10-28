# 🏥 Sistema de Controle de Estoque e Consumo de Insumos para Diagnóstico

Este projeto implementa um sistema de gerenciamento de estoque e registro de consumo de insumos (reagentes e descartáveis) para unidades de diagnóstico, com o objetivo de otimizar o controle e a previsão de reposição, conforme o problema proposto.

## 🧑‍🎓 Integrantes - 2ESPI

| Nome | RM |
| :--- | :--- |
| Fernando Najavas | RM555080 |
| José Guilherme Sipauba | RM557274 |
| Rafael Teofilo Lucena | RM555600 |
| Vinicius Fernandes Tavares Bittencourt | RM558909 |
| Weslley Cardoso | RM557927 |

---

## 🛠️ Requisitos e Como Rodar o Código

### Requisitos
O script é escrito em Python puro e só requer a biblioteca padrão `datetime` (importada no início do código).

### Como Rodar
1.  **Clone o Repositório:**
    ```bash
    git clone https://github.com/uBittencourt/estoque_otimizado.git
    cd <pasta de download>
    ```
2.  **Execute o Script Python:**
    ```bash
    python estoque_otimizado.py
    ```
3.  O programa iniciará um *loop* interativo no terminal, permitindo que o usuário escolha as funcionalidades.

---

## 💡 Relatório: Solução para o Controle de Insumos (Programação Dinâmica e Estruturas Clássicas)

O problema central é duplo: gerenciar eficientemente o estoque diário e, de forma mais complexa, **otimizar a decisão de compra de reposição** dentro de um orçamento limitado.

### 1. Modelagem dos Dados

Utilizamos duas estruturas principais (listas de listas) para simular o cenário:

* **`estoque`**: `['Nome', Qtde, Validade, Importância(1-5), Preço Unitário]`. Esta lista é mantida ordenada alfabeticamente para a Busca Binária.
* **`consumo`**: `[Data do Consumo, Nome do Insumo, Quantidade Consumida]`.

### 2. Estruturas e Algoritmos Clássicos Aplicados

| Funcionalidade | Estrutura/Algoritmo | Explicação da Solução no Contexto |
| :--- | :--- | :--- |
| **Registro de Consumo** | **Fila (FIFO) e Busca Binária** | O consumo é inserido no final da lista `consumo` em **ordem cronológica (FIFO)**, mantendo a rastreabilidade exata. A **Busca Binária** é usada no estoque para localizar o insumo a ser debitado de forma eficiente ($O(\log n)$). |
| **Consulta Rápida de Consumo** | **Pilha (LIFO)** | A função `ultimos_consumos` usa a lista de consumo como uma **Pilha (LIFO)**. Permite que a gestão veja imediatamente os **eventos mais recentes** (`pop()` na lista), auxiliando em auditorias ou na verificação de picos de uso em tempo real. |
| **Prevenção de Perdas** | **Quick Sort** | A função `quick_sort` ordena o estoque pela **data de validade**. Este algoritmo de alta performance garante que o sistema exiba o **item prioritário para consumo**, minimizando o descarte de materiais vencidos. |
| **Análise de Demanda** | **Merge Sort** | O **Merge Sort** é aplicado para ordenar os insumos **por quantidade total consumida**, identificando rapidamente o **insumo mais demandado**. Essencial para a previsão de reposição. |
| **Agregação de Dados** | **Recursão** | A função `soma_qtde` utiliza a **recursão** para percorrer a lista de consumo e agregar as quantidades por insumo. Demonstra a capacidade de processar os dados históricos de consumo de forma concisa antes da ordenação. |
| **Rastreamento Diário** | **Busca Sequencial** | A função `consumo_por_dia` percorre a lista `consumo` para encontrar todas as ocorrências de uma data específica. É a escolha ideal para filtros em listas não ordenadas pelo critério de busca. |

### 3. Otimização da Reposição: Problema da Mochila

O desafio mais sofisticado é decidir quais itens urgentes comprar, respeitando o orçamento (`Capacidade da Mochila`). Para isso, utilizamos a Programação Dinâmica (DP).

#### Mapeamento do Problema

| Conceito da DP | Contexto no Problema | Lógica de Cálculo |
| :--- | :--- | :--- |
| **Mochila (Capacidade)** | O Orçamento Máximo (R$) disponível. | Valor inserido pelo usuário (ex: R$ 500). |
| **Itens** | Insumos cujo `Estoque Atual < ESTOQUE_MINIMO (50)`. | Apenas itens urgentes são candidatos à compra. |
| **Benefício (Valor)** | A `Importância` (5 para reagentes críticos, 2 para seringas, etc.). | Valor entre 1 e 5 (índice 3 do `estoque`). O objetivo é **Maximizar** a soma dos benefícios. |
| **Custo (Peso)** | O custo total para comprar a **quantidade necessária** para atingir 50 unidades. | $Custo = (50 - Qtde\ Atual) \times Preço\ Unitário$. |

#### Implementações da DP (Garantindo Separação)

Para demonstrar as duas abordagens da Programação Dinâmica, implementamos funcionalidades separadas:

| Opção | Abordagem | Função Principal | Rastreamento (Traceback) |
| :---: | :--- | :--- | :--- |
| **7** | **Recursiva (Top-Down)** | `mochila_recursiva(i, capacidade, itens)` | **`rastrear_recursivo(N, capacidade, itens)`:** A função `mochila_recursiva` armazena o *caminho ótimo* (`(valor, booleano_incluído)`) na tabela global `memo`. A função `rastrear_recursivo` utiliza essa `memo` para reconstruir a lista de itens comprados de forma nativa e dedicada à recursão, garantindo a independência do método. |
| **8** | **Iterativa (Bottom-Up)** | `mochila_iterativa(capacidade, itens)` | **`rastrear_itens(dp_table, N, capacidade, itens)`:** A função `mochila_iterativa` constrói a matriz completa (`dp_table`). O rastreamento utiliza essa matriz, comparando os valores da linha atual (`dp[i][w]`) com a linha anterior (`dp[i-1][w]`) para determinar se o item foi incluído. |

Esta estrutura modular permite ao usuário escolher o método de otimização e garante que as duas técnicas sejam implementadas e rastreadas de forma autônoma e correta.