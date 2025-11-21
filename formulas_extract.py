### 

import json

input_json_file = "arquivo-principal.json"
output_json_file = "formulas_processadas.json"

def process_json_data(data):
    """
    - remove a chave 'formulas_math' de cada registro.
    - remove entradas duplicadas na lista 'formulas_som'.
    """
    processed_data = []
    for record in data:
        """ verifica se 'formulas_som' existe e é uma lista para evitar erros. """
        if 'formulas_som' in record and isinstance(record['formulas_som'], list):
            """ usa dict.fromkeys para remover duplicatas preservando a ordem da primeira aparição. """
            """ depois converte de volta para uma lista. """
            record['formulas_som'] = list(dict.fromkeys(record['formulas_som']))

        """ verifica se a chave 'formulas_math' existe e a remove. """
        if 'formulas_math' in record:
            del record['formulas_math']
        
        processed_data.append(record)
        
    return processed_data

def main():
    try:
        """ abrindo arquivo json """
        with open(input_json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: The input file '{input_json_file}' was not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: The file '{input_json_file}' does not contain valid JSON.")
        return
    except Exception as e:
        print(f"An unexpected error occurred while reading the file: {e}")
        return

    """ processa os dados """
    cleaned_data = process_json_data(data)

    with open(output_json_file, "w", encoding="utf-8") as out:
        """ usa indent=2 para formatação e ensure_ascii=False para lidar com caracteres especiais corretamente. """
        json.dump(cleaned_data, out, indent=2, ensure_ascii=False)

    print(f"Processamento concluído. Os dados foram guardados em '{output_json_file}'.")
    print(f"Total de documentos processados: {len(cleaned_data)}")

if __name__ == "__main__":
    main()