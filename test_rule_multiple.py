#!/usr/bin/env python3

# Teste do novo método add_rule_multiple
# para buildar: C:\Users\yasmin.romeiro\AppData\Local\Programs\Python\Python310\python.exe setup.py build_ext --inplace
# para rodar:  C:\Users\yasmin.romeiro\AppData\Local\Programs\Python\Python310\python.exe test_rule_multiple.py 

import wisardpkg as wp

def test_rule_multiple():
    print("=== Teste do add_rule_multiple ===")
    
    # Criar um modelo WiSARD
    w = wp.Wisard(4)
    
    print("\n1. Testando regra A and (B or C) and D:")
    print("   VariableIndexes: [1, 2, 3, 4] (A=1, B=2, C=3, D=4)")
    print("   RuleValues: [1101, 1110, 1111]")
    print("   Significado: A=1, D=1, e (B=1 ou C=1)")
    
    # Regra: A and (B or C) and D
    # VariableIndexes: [1, 2, 3, 4] (A=1, B=2, C=3, D=4)
    # RuleValues: [1101, 1110, 1111] (todas as combinações onde A=1, D=1, e (B=1 ou C=1))
    w.add_rule(
        label="1",
        variableIndexes=[1, 2, 3, 4],  # A=1, B=2, C=3, D=4
        multipleRuleValues=[
            [1, 1, 0, 1],  # 1101: A=1, B=1, C=0, D=1
            [1, 1, 1, 0],  # 1110: A=1, B=1, C=1, D=0
            [1, 1, 1, 1]   # 1111: A=1, B=1, C=1, D=1
        ],
        alpha=5
    )
    
    print("\n2. Testando classificacao com dados que satisfazem a regra:")
    
    # Teste 1: [0,1,1,0,1] - satisfaz A=1, B=1, C=0, D=1 (1101)
    test1 = [[0,1,1,0,1]]
    result1 = w.classify_with_rules(test1)
    print(f"   Entrada [0,1,1,0,1]: {result1[0]} (deve ser '1')")
    
    # Teste 2: [0,1,1,1,0] - satisfaz A=1, B=1, C=1, D=0 (1110)
    test2 = [[0,1,1,1,0]]
    result2 = w.classify_with_rules(test2)
    print(f"   Entrada [0,1,1,1,0]: {result2[0]} (deve ser '1')")
    
    # Teste 3: [0,1,1,1,1] - satisfaz A=1, B=1, C=1, D=1 (1111)
    test3 = [[0,1,1,1,1]]
    result3 = w.classify_with_rules(test3)
    print(f"   Entrada [0,1,1,1,1]: {result3[0]} (deve ser '1')")
    
    # Teste 4: [0,1,0,0,1] - nao satisfaz (A=1, B=0, C=0, D=1 - falta B ou C)
    test4 = [[0,1,0,0,1]]
    result4 = w.classify_with_rules(test4)
    print(f"   Entrada [0,1,0,0,1]: {result4[0]} (nao satisfaz regra)")
    
    # Teste 5: [0,0,1,1,1] - nao satisfaz (A=0, B=1, C=1, D=1 - falta A)
    test5 = [[0,0,1,1,1]]
    result5 = w.classify_with_rules(test5)
    print(f"   Entrada [0,0,1,1,1]: {result5[0]} (nao satisfaz regra)")
    
    print("\n3. Visualizando conteudo das RAMs:")
    rams_info = w.get_rams_info()
    print(rams_info)
    
    print("\n4. Testando com multiplas entradas:")
    test_multiple = [
        [0,1,1,0,1],  # satisfaz
        [0,1,1,1,0],  # satisfaz
        [0,1,1,1,1],  # satisfaz
        [0,1,0,0,1],  # nao satisfaz
        [0,0,1,1,1]   # nao satisfaz
    ]
    results = w.classify_with_rules(test_multiple)
    for i, (input_data, result) in enumerate(zip(test_multiple, results)):
        print(f"   Entrada {input_data}: {result}")
    
    print("\n=== Teste Concluido ===")

if __name__ == "__main__":
    test_rule_multiple()
