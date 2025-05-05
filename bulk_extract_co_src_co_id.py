#!/usr/bin/env python3
import json
from pathlib import Path

input_path  = Path('data/bulk_data_insert.ndjson')
output_path = Path('data/bulk_co_id_co_src.ndjson')

with input_path.open('r', encoding='utf-8') as src, \
     output_path.open('w', encoding='utf-8') as dest:

    for line in src:
        line = line.strip()
        if not line:
            continue

        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue

        # only if both
        if "co_id" not in record or "co_src" not in record:
            continue

        co_id  = record["co_id"]
        co_src = record["co_src"]

        # ignore empty
        if co_id == "" and co_src == "":
            continue

        out = {
            "co_id":  co_id,
            "co_src": co_src
        }
        dest.write(json.dumps(out, ensure_ascii=False) + "\n")

print(f"Extraction done. co_id and co_src saved to: {output_path.resolve()}")






# import json

# arquivo_entrada = 'data/bulk_data_insert.ndjson'
# arquivo_saida = 'data/bulk_entrys.ndjson'

# with open(arquivo_entrada, 'r', encoding='utf-8') as src_file, open(arquivo_saida, 'w', encoding='utf-8') as dest_file:
#     for line in src_file:
#         try:
#             record = json.loads(line.strip())
#             dest_file.write(json.dumps({"index": {"_index": indice}}) + '\n')
#             dest_file.write(json.dumps(record) + '\n')
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
#                 record = json.loads(line)
#                 co_src = record.get("co_src", "")
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
