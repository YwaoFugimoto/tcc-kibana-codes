### Esse arquivo retira campos do dump json. Deixando apenas os campos: "id" e
### "formulas_som"

import json

# --- CONFIGURAÇÃO ---
# Altere os nomes dos arquivos de entrada e saída conforme sua necessidade.
NOME_ARQUIVO_ENTRADA = 'formulas_processadas.json'
NOME_ARQUIVO_SAIDA = 'id_e_formulas_som.json'
# --------------------

try:
    # 1. Abre e lê o arquivo JSON de entrada.
    # O 'with open(...)' garante que o arquivo será fechado corretamente.
    # 'r' significa modo de leitura (read).
    # 'encoding="utf-8"' é importante para evitar erros com acentuação.
    print(f"Lendo o arquivo '{NOME_ARQUIVO_ENTRADA}'...")
    with open(NOME_ARQUIVO_ENTRADA, 'r', encoding='utf-8') as arquivo_entrada:
        # Usa json.load() para ler diretamente de um arquivo (diferente de json.loads())
        dados = json.load(arquivo_entrada)

    # 2. Processa os dados, mantendo apenas os campos "id" e "formulas_som".
    # A lógica é a mesma, usando uma List Comprehension.
    print("Processando os dados...")
    dados_processados = [
        {"id": item["id"], "formulas_som": item["formulas_som"]} 
        for item in dados
    ]

    # 3. Salva a nova lista em um arquivo JSON de saída.
    # 'w' significa modo de escrita (write), que cria um novo arquivo ou sobrescreve um existente.
    print(f"Salvando o resultado em '{NOME_ARQUIVO_SAIDA}'...")
    with open(NOME_ARQUIVO_SAIDA, 'w', encoding='utf-8') as arquivo_saida:
        # Usa json.dump() para escrever os dados em um arquivo.
        json.dump(dados_processados, arquivo_saida, indent=2, ensure_ascii=False)

    print("\nProcessamento concluído com sucesso!")

except FileNotFoundError:
    print(f"\nERRO: O arquivo de entrada '{NOME_ARQUIVO_ENTRADA}' não foi encontrado.")
    print("Por favor, verifique se o nome do arquivo está correto e se ele está na mesma pasta do script.")

except KeyError as e:
    print(f"\nERRO: O JSON de entrada não tem o formato esperado.")
    print(f"A chave {e} não foi encontrada em um dos objetos do arquivo.")

except json.JSONDecodeError:
    print(f"\nERRO: O arquivo '{NOME_ARQUIVO_ENTRADA}' não contém um JSON válido.")
    print("Por favor, verifique a formatação do arquivo de entrada.")

except Exception as e:
    print(f"\nOcorreu um erro inesperado: {e}")