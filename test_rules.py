#!/usr/bin/env python3

# Teste das regras neuro-simbolicas no WiSARD
# para buildar: C:\Users\yasmin.romeiro\AppData\Local\Programs\Python\Python310\python.exe setup.py build_ext --inplace
# para rodar:  C:\Users\yasmin.romeiro\AppData\Local\Programs\Python\Python310\python.exe test_rules.py 


import wisardpkg as wp

def test_neuro_symbolic_rules():
    print("=== Teste das Regras Neuro-Simbolicas ===")
    
    # Criar um modelo WiSARD
    w = wp.Wisard(4)  # addressSize=4 para RAMs aleatórias
    w.train([[1,0,0,0,1,1,1,0], [0,0,0,0,1,0,0,0]], ["1","0"])  

    print("\nVisualizando conteúdo das RAMs após treinamento:")
    rams_info = w.get_rams_info()
    print(rams_info)
    
    print("\n1. Adicionando regras para a classe '1':")
    
    # Regra: A and not B and not C -> 1
    # Variáveis: A=posição 0, B=posição 1, C=posição 2
    # Valores: A=1, B=0, C=0 (ou seja, 100 em binário)
    w.add_rule(
        label="1",
        variableIndexes=[0, 1, 2],  # ordem: [A, B, C]
        multipleRuleValues=[[1, 0, 0],[1,1,0]],       # 100 (base 2)
        alpha=5,
        ignoreZero=False
    )
    print("   ✓ Regra A and not B and not C -> 1 (endereco 100)")
    
    # Regra: A and D and not C -> 1
    # Variáveis: A=posição 0, D=posição 3, C=posição 2
    # Valores: A=1, D=1, C=0 (ou seja, 110 em binário)
    w.add_rule(
        label="1",
        variableIndexes=[0, 3, 2],  # ordem: [A, D, C]
        multipleRuleValues=[[1, 1, 0]],       # 110 (base 2)
        alpha=5
    )
    print("   ✓ Regra A and D and not C -> 1 (endereco 110)")
    
    # Regra: not A and not B and not C -> 1
    # Variáveis: A=posição 0, B=posição 1, C=posição 2
    # Valores: A=0, B=0, C=0 (ou seja, 000 em binário)
    w.add_rule(
        label="1",
        variableIndexes=[0, 1, 2],  # ordem: [A, B, C]
        multipleRuleValues=[[0, 0, 0]],       # 000 (base 2)
        alpha=5
    )
    print("   ✓ Regra not A and not B and not C -> 1 (endereco 000)")


    print("\nVisualizando conteúdo das RAMs após adição das regras:")
    rams_info = w.get_rams_info()
    print(rams_info)

    print("\n2. Testando classificação com dados que satisfazem as regras:")
    
    # Teste 1: [1,0,0,0] - satisfaz A and not B and not C
    test1 = [[1,0,0,0]]
    result1 = w.classify_with_rules(test1)
    print(f"   Entrada [1,0,0,0]: {result1[0]}")
    
    # Teste 2: [1,0,0,1] - satisfaz A and D and not C
    test2 = [[1,0,0,1]]
    result2 = w.classify_with_rules(test2)
    print(f"   Entrada [1,0,0,1]: {result2[0]}")
    
    # Teste 3: [0,0,0,0] - satisfaz not A and not B and not C
    test3 = [[1,1,0,0, 1, 0, 0, 0]]
    result3 = w.classify_with_rules(test3)
    print(f"   Entrada [0,0,0,0]: {result3[0]}")
    
    # Teste 4: [1,1,0,0] - nao satisfaz nenhuma regra
    test4 = [[0, 0, 0, 0, 1, 0, 0, 0]]
    result4 = w.classify_with_rules(test4)
    print(f"   Entrada [0,1,0,0]: {result4[0]} (nao satisfaz regras)")
    
    print("\n3. Testando com multiplas entradas:")
    test_multiple = [[1,0,0,0], [1,0,0,1], [0,0,0,0], [1,1,0,0]]
    results = w.classify_with_rules(test_multiple)
    for i, (input_data, result) in enumerate(zip(test_multiple, results)):
        print(f"   Entrada {input_data}: {result}")
    
    print("\n4. Verificando mental images:")
    mental_images = w.getMentalImages()
    print(f"   Classes com discriminadores: {list(mental_images.keys())}")
    if "1" in mental_images:
        print(f"   Mental image da classe '1': {mental_images['1']}")
    if "0" in mental_images:
        print(f"   Mental image da classe '0': {mental_images['0']}")
if __name__ == "__main__":
    test_neuro_symbolic_rules()
