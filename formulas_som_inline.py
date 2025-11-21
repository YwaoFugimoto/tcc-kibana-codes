### Este arquivo acessa o campo formulas_som e remove formulas repetidas
### output:
### "formula"
### "formula"
### "formula"

import json

# --- CONFIGURAÇÃO ---
# Arquivo JSON gerado pelo script anterior
NOME_ARQUIVO_ENTRADA = 'id_e_formulas_som.json'
# Arquivo de texto onde as fórmulas únicas serão salvas
NOME_ARQUIVO_SAIDA = 'formulas_unicas.txt'
# --------------------

try:
    # 1. Abre e lê o arquivo JSON de entrada.
    print(f"Lendo o arquivo '{NOME_ARQUIVO_ENTRADA}'...")
    with open(NOME_ARQUIVO_ENTRADA, 'r', encoding='utf-8') as arquivo_entrada:
        dados = json.load(arquivo_entrada)

    # 2. Extrai todas as fórmulas e remove duplicatas usando um 'set'.
    print("Extraindo fórmulas e removendo duplicatas...")
    formulas_unicas = set()

    # Itera sobre cada objeto na lista de dados
    for item in dados:
        # Adiciona todas as fórmulas da lista 'formulas_som' ao set
        # O método update() é eficiente para adicionar múltiplos itens.
        if 'formulas_som' in item:
            formulas_unicas.update(item['formulas_som'])

    # 3. Salva as fórmulas únicas no arquivo de saída, uma por linha.
    print(f"Salvando {len(formulas_unicas)} fórmulas únicas em '{NOME_ARQUIVO_SAIDA}'...")
    with open(NOME_ARQUIVO_SAIDA, 'w', encoding='utf-8') as arquivo_saida:
        # Converte o set para uma lista e ordena (opcional, mas bom para consistência)
        for formula in sorted(list(formulas_unicas)):
            arquivo_saida.write(f"{formula}\n")

    print("\nExtração concluída com sucesso! ✅")

except FileNotFoundError:
    print(f"\nERRO: O arquivo de entrada '{NOME_ARQUIVO_ENTRADA}' não foi encontrado.")
    print("Por favor, execute o script anterior primeiro ou verifique o nome do arquivo.")

except KeyError:
    print(f"\nERRO: O JSON de entrada não tem o formato esperado.")
    print("Certifique-se de que os objetos no arquivo contêm a chave 'formulas_som'.")
    
except Exception as e:
    print(f"\nOcorreu um erro inesperado: {e}")