import json
from pathlib import Path

arquivo_entrada = Path('data/bulk_data_insert.ndjson')
arquivo_saida = Path('data/bulk_entrys.ndjson')


with open(arquivo_entrada, 'r', encoding='utf-8') as f_in, open(arquivo_saida, 'w', encoding='utf-8') as f_out:
    for line in f_in:
        try:
            doc = json.loads(line.strip())
            co_src = doc.get("co_src", "")

            f_out.write(json.dumps(co_src, ensure_ascii=False) + '\n')
        except json.JSONDecodeError:

            continue

print(f"Extração concluída! Todos os campos 'co_src' foram salvos em: {arquivo_saida.resolve()}")




# import json

# arquivo_entrada = 'data/bulk_data_insert.ndjson'
# arquivo_saida = 'data/bulk_entrys.ndjson'

# with open(arquivo_entrada, 'r', encoding='utf-8') as f_in, open(arquivo_saida, 'w', encoding='utf-8') as f_out:
#     for line in f_in:
#         try:
#             doc = json.loads(line.strip())
#             f_out.write(json.dumps({"index": {"_index": indice}}) + '\n')
#             f_out.write(json.dumps(doc) + '\n')
#         except Exception as e:
#             print("Erro ao processar linha:", e)


# import json
# import sys
# from pathlib import Path

# def extract_co_src(ndjson_path):
#     co_src_list = []
#     with open(ndjson_path, 'r', encoding='utf-8') as f:
#         for line in f:
#             # pula as linhas de metadado do Bulk API
#             if line.lstrip().startswith('{"index"'):
#                 continue
#             # tenta decodificar a linha como JSON e extrair o campo co_src
#             try:
#                 doc = json.loads(line)
#                 co_src = doc.get("co_src", "")
#                 co_src_list.append(co_src)
#             except json.JSONDecodeError:
#                 # pula linhas mal formadas
#                 continue
#     return co_src_list

# def main():
#     if len(sys.argv) != 2:
#         print(f"Uso: python {sys.argv[0]} /home/noSecureOption/tcc/data/bulk_data_insert.ndjson")
#         sys.exit(1)

#     ndjson_file = Path(sys.argv[1])
#     if not ndjson_file.is_file():
#         print(f"Arquivo {ndjson_file} não encontrado.")
#         sys.exit(1)

#     srcs = extract_co_src(ndjson_file)

#     output_path = Path("/data/bulk_entrys")
#     with open(output_path, 'w', encoding='utf-8') as out:
#         json.dump(srcs, out, ensure_ascii=False, indent=2)

#     print(f"{len(srcs)} entradas extraídas e salvas em '{output_path}'")

# if __name__ == "__main__":
#     main()
