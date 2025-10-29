from datetime import date

estoque = [
    ['Reagente A', 40, date(2026, 11, 10), 5, 50.0],
    ['Reagente B', 60, date(2026, 10, 5), 4, 35.0],
    ['Reagente C', 30, date(2026, 10, 30), 5, 40.0],
    ['Seringa', 200, date(2026, 1, 20), 2, 5.0],
    ['Luva', 150, date(2026, 12, 15), 3, 10.0],
]

consumo = [
    [date(2025, 9, 15), 'Reagente A', 10],
    [date(2025, 9, 16), 'Reagente B', 5],
    [date(2025, 9, 16), 'Luva', 30],
    [date(2025, 9, 17), 'Reagente A', 20]
]

soma_consumos = {} 
memo = {}

ESTOQUE_MINIMO = 50 


# ESTRUTURA DE BUSCA BINÁRIA PARA RETORNAR O INDÍCE DO INSUMO NO ESTOQUE
def busca_binaria(insumo):
    inicio = 0
    fim = len(estoque) - 1
    while inicio <= fim:
        meio = (inicio + fim) // 2
        if estoque[meio][0] == insumo:
            return meio
        elif insumo > estoque[meio][0]:
            inicio = meio + 1
        else:
            fim = meio - 1
    return -1


# ESTRUTURA DE FIFO (FILA)
def adicionar_consumo(insumo, qtde):
    estoque_insumo = busca_binaria(insumo)
    if estoque_insumo < 0:
        return 'Insumo inexistente!'
        
    qtde_estoque = estoque[estoque_insumo][1] - qtde
    
    if qtde_estoque < 0:
        return 'Quantidade em estoque insuficiente!'
    else:
        estoque[estoque_insumo][1] -= qtde
        consumo.append([date.today(), insumo, qtde])
        return 'Insumo consumido!'


# ESTRUTURA DE BUSCA SEQUENCIAL
def consumo_por_dia(data):
    print(f'Consumos do dia {data.strftime('%d/%m/%Y')}:')
    encontrados = False
    for ocorrencia in consumo:
        if ocorrencia[0] == data:
            print(f'\tInsumo: {ocorrencia[1]} | Qtde: {ocorrencia[2]}')
            encontrados = True
    if not encontrados:
        print("\tNenhum consumo registrado para esta data.")


# ESTRUTURA DE LIFO (PILHA)
def ultimos_consumos(qtde):
    _consumo = consumo.copy() 
    if qtde > len(_consumo):
        print('Quantidade maior que consumos cadastrados!')
        qtde = len(_consumo)
    print(f'Último(s) {qtde} consumo(s):')
    for _ in range(qtde):
        ocorrencia = _consumo.pop()
        print(f'\tData: {ocorrencia[0].strftime('%d/%m/%Y')} | Insumo: {ocorrencia[1]} | Qtde: {ocorrencia[2]}')


# ESTRUTURA QUICK SORT
def quick_sort(lista):
    if len(lista) <= 1:
        return lista
    pivo = lista[-1]
    menores = [x for x in lista[:-1] if x[2] <= pivo[2]]
    maiores = [x for x in lista[:-1] if x[2] > pivo[2]]
    return quick_sort(menores) + [pivo] + quick_sort(maiores)


# ESTRUTURA DE SOMA (RECURSÃO)
def soma_qtde(i):
    global soma_consumos
    if i < 0:
        return soma_consumos
    insumo = consumo[i][1]
    qtde = consumo[i][2]
    if insumo in soma_consumos:
        soma_consumos[insumo] += qtde
    else:
        soma_consumos[insumo] = qtde
    return soma_qtde(i - 1) 


# ESTRUTURA DE MERGE SORT
def merge_sort(lista):
    if len(lista) <= 1:
        return lista 
    meio = len(lista) // 2
    esquerda = merge_sort(lista[:meio])
    direita = merge_sort(lista[meio:])
    resultado = []
    i = j = 0
    while i < len(esquerda) and j < len(direita):
        if esquerda[i][1] < direita[j][1]:
            resultado.append(esquerda[i])
            i += 1
        else: 
            resultado.append(direita[j])
            j += 1
    return resultado + esquerda[i:] + direita[j:]


def adicionar_estoque(insumo, quantidade, validade):
    estoque_insumo = busca_binaria(insumo)
    if estoque_insumo < 0:
        estoque.append([insumo, quantidade, validade, 1, 0.0]) 
        estoque.sort(key=lambda x: x[0]) 
        return 'Estoque adicionado como novo insumo! Defina a importância e o preço.'
        
    estoque[estoque_insumo][1] += quantidade
    estoque[estoque_insumo][2] = validade 
    return 'Estoque atualizado!'


# FAZ O CÁLCULO DA IMPORTÂNCIA NO ESTOQUE E O CUSTO
def preparar_dados_mochila(estoque):
    itens = []
    
    for nome, qtde_estoque, _, importancia, preco_unitario in estoque:
        beneficio = 0
        qtde_necessaria = 0
        urgencia_texto = f"Baixa Urgência (Estoque: {qtde_estoque} >= {ESTOQUE_MINIMO})"

        if qtde_estoque < ESTOQUE_MINIMO:
            beneficio = importancia 
            urgencia_texto = f"ALTA URGÊNCIA (Estoque: {qtde_estoque} < {ESTOQUE_MINIMO})"
            qtde_necessaria = ESTOQUE_MINIMO - qtde_estoque
            
        custo = preco_unitario * qtde_necessaria
        custo = int(round(custo))
        
        if beneficio > 0 and custo > 0:
            itens.append({
                'nome': nome, 
                'beneficio': beneficio, 
                'custo': custo,
                'urgencia': urgencia_texto,
                'qtde_compra': qtde_necessaria
            })
            
    return itens


# VERSÃO RECURSIVA COM MEMORIZAÇÃO (TOP-DOWN)
def mochila_recursiva(i, capacidade, itens):
    global memo
    chave = (i, capacidade)
    
    if i == 0 or capacidade == 0:
        return 0
    
    if chave in memo:
        return memo[chave][0]
    
    beneficio = itens[i-1]['beneficio']
    custo = itens[i-1]['custo']
    
    if custo > capacidade:
        resultado = mochila_recursiva(i - 1, capacidade, itens)
        memo[chave] = (resultado, False)
        return resultado
    else:
        nao_incluir = mochila_recursiva(i - 1, capacidade, itens)
        incluir = beneficio + mochila_recursiva(i - 1, capacidade - custo, itens)
        
        if incluir > nao_incluir:
            memo[chave] = (incluir, True)
            return incluir
        else:
            memo[chave] = (nao_incluir, False)
            return nao_incluir


# RASTREAMENTO DOS INSUMOS INCLUÍDOS (RECURSIVO)
def rastrear_recursivo(N, capacidade, itens):
    itens_comprados = []
    w = capacidade
    
    for i in range(N, 0, -1):
        chave = (i, w)
        
        if w == 0 or chave not in memo:
             break 
             
        _beneficio, item_foi_incluido = memo[chave]
        
        if item_foi_incluido:
            itens_comprados.append(itens[i-1])
            w -= itens[i-1]['custo']
            
    return itens_comprados[::-1]


# RASTREAMENTO DOS INSUMOS INCLUÍDOS (ITERATIVO)
def rastrear_iterativo(dp_table, N, capacidade, itens):
    itens_comprados = []
    w = capacidade
    
    for i in range(N, 0, -1):
        custo = itens[i-1]['custo']
        
        if dp_table[i][w] != dp_table[i-1][w]:
            itens_comprados.append(itens[i-1])
            w -= custo
            
    return itens_comprados[::-1]


# VERSÃO ITERATIVA (BOTTOM-UP)
def mochila_iterativa(capacidade, itens):
    N = len(itens)
    dp = [[0] * (capacidade + 1) for _ in range(N + 1)]
    
    for i in range(1, N + 1):
        beneficio = itens[i-1]['beneficio']
        custo = itens[i-1]['custo']
        
        for w in range(1, capacidade + 1):
            if custo > w:
                dp[i][w] = dp[i-1][w]
            else:
                dp[i][w] = max(dp[i-1][w], beneficio + dp[i-1][w - custo])
                
    return dp, N, capacidade


# EXIBIÇÃO DAS MELHORES OPÇÕES DE COMPRA
def exibir_otimizacao(orcamento, max_beneficio, itens_comprados):
    custo_final = sum(item['custo'] for item in itens_comprados)
    
    print()
    print(30*'=')
    print(f"Benefício Máximo: {max_beneficio} pontos (Urgência)")
    print(f"ORÇAMENTO TOTAL DISPONÍVEL: R${orcamento:.2f}")
    
    if itens_comprados:
        print("\nITENS RECOMENDADOS PARA COMPRA:")
        for item in itens_comprados:
            print(f"  -> {item['nome']}: Custo R${item['custo']:.2f} ({item['qtde_compra']} un. para atingir {ESTOQUE_MINIMO} em estoque)")
        print(f"\nCUSTO TOTAL DA COMPRA OTIMIZADA: R${custo_final:.2f}")
        print(f"CRÉDITO RESTANTE: R${orcamento - custo_final:.2f}")
    else:
        print("\nNENHUM ITEM URGENTE (Estoque < 50) coube no orçamento.")
    print(30*'=')


# MENU DA VERSÃO RECURSIVA
def menu_recursivo():
    print(5*'-=', "OTIMIZAÇÃO DE ESTOQUE: MÉTODO RECURSIVO", 5*'-=')
    
    try:
        orcamento = int(input(f"Informe o ORÇAMENTO MÁXIMO para reposição: R$"))
        itens_para_otimizar = preparar_dados_mochila(estoque)
        N = len(itens_para_otimizar)

        print("\nITENS CANDIDATOS E URGÊNCIA:")
        for item in itens_para_otimizar:
             print(f"- {item['nome']}: Importância {item['beneficio']} | Custo R${item['custo']:.2f} | Necessário: {item['qtde_compra']} un.")
        
        global memo 
        memo = {}

        max_beneficio = mochila_recursiva(N, orcamento, itens_para_otimizar)
        itens_comprados = rastrear_recursivo(N, orcamento, itens_para_otimizar)
        exibir_otimizacao(orcamento, max_beneficio, itens_comprados)

    except ValueError:
        print("Entrada inválida. Certifique-se de digitar um número.")


# MENU PARA FAZER APRESENTAÇÃO DOS INSUMOS
def menu_iterativo():
    print(5*'-=', "OTIMIZAÇÃO DE ESTOQUE: MÉTODO ITERATIVO", 5*'-=')
    
    try:
        orcamento = int(input(f"Informe o ORÇAMENTO MÁXIMO para reposição: R$"))
        itens_para_otimizar = preparar_dados_mochila(estoque)
        N = len(itens_para_otimizar)

        print("\nITENS CANDIDATOS E URGÊNCIA:")
        for item in itens_para_otimizar:
             print(f"- {item['nome']}: Importância {item['beneficio']} | Custo R${item['custo']:.2f} | Necessário: {item['qtde_compra']} un.")
             
        dp_table, N, capacidade_final = mochila_iterativa(orcamento, itens_para_otimizar)
        max_beneficio = dp_table[N][capacidade_final]
        itens_comprados = rastrear_iterativo(dp_table, N, capacidade_final, itens_para_otimizar)
        exibir_otimizacao(orcamento, max_beneficio, itens_comprados)

    except ValueError:
        print("Entrada inválida. Certifique-se de digitar um número.")


continuar = 'Sim'
while continuar != 'Não':
    soma_consumos = {} 
    
    print()
    print(5*'=-', 'CONTROLE DE ESTOQUE', 5*'-=')
    try:
        opcao = int(input('\n[1] - Adicionar Consumo \n[2] - Últimos Consumos \n[3] - Consumos no dia \n[4] - Insumo próximo de vencer \n[5] - Verificar insumo mais consumido \n[6] - Adicionar Estoque \n[7] - Otimizar Reposição (Recursiva - Top-Down) \n[8] - Otimizar Reposição (Iterativa - Bottom-Up) \nSelecione uma opção: '))

        print()
        match opcao:
            case 1:
                nome = input('Qual insumo você deseja consumir: ').title()
                qtde = int(input('Qual a quantidade: '))
                print(adicionar_consumo(nome, qtde))
            case 2:
                qtde = int(input('Digite a quantidade que deseja verificar: '))
                ultimos_consumos(qtde)
            case 3:
                dia = int(input('Digite o dia que deseja ver: '))
                mes = int(input('Digite o mês que deseja ver: '))
                ano = int(input('Digite o ano que deseja ver: '))
                consumo_por_dia(date(ano, mes, dia))
            case 4:
                estoque_validade = quick_sort(estoque.copy())
                insumo_validade = estoque_validade.pop(0)
                print('Insumo mais próximo da data de vencimento:')
                print(f'\tInsumo: {insumo_validade[0]} | Qtde: {insumo_validade[1]} | Validade: {insumo_validade[2].strftime('%d/%m/%Y')}')
            case 5:
                soma_qtde(len(consumo) - 1)
                soma_consumos_lista = merge_sort(list(soma_consumos.items()))
                
                if soma_consumos_lista:
                    insumo_mais_consumido = soma_consumos_lista[-1]
                    print('Insumo mais consumido:')
                    print(f'\tInsumo: {insumo_mais_consumido[0]} | Qtde Total: {insumo_mais_consumido[1]}')
                else:
                    print("Nenhum consumo registrado ainda.")
            case 6:
                nome = input('Qual insumo você deseja adicionar: ').title()
                qtde = int(input('Qual a quantidade: '))
                dia = int(input('Digite o dia de validade do lote: '))
                mes = int(input('Digite o mês de validade do lote: '))
                ano = int(input('Digite o ano de validade do lote: '))
                print(adicionar_estoque(nome, qtde, date(ano, mes, dia)))
            case 7:
                menu_recursivo() 
            case 8:
                menu_iterativo() 
            case _:
                print('Selecione uma opção válida!')
    except ValueError:
        print('\nDigite uma entrada válida!')
    
    continuar = input('\nDeseja continuar (Sim/Não): ').title()