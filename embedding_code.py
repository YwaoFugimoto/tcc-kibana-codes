#!/usr/bin/env python3
import json
from pathlib import Path
from sentence_transformers import SentenceTransformer


input_path = Path('data/bulk_entrys.ndjson')
output_path = Path('data/bulk_entrys_embedded.ndjson')

model = SentenceTransformer('all-MiniLM-L12-v2')

texts = []
with open(input_path, 'r', encoding='utf-8') as f_in:
    for line in f_in:
        raw = line.strip()
        if not raw:
            continue
        try:
            text = json.loads(raw)
        except json.JSONDecodeError:
            continue
        # Ignora strings vazias
        if text == "":
            continue
        texts.append(text)

embeddings = model.encode(texts, batch_size=32, show_progress_bar=True)

with open(output_path, 'w', encoding='utf-8') as f_out:
    for emb in embeddings:
        record = {
            "co_embedding": emb.tolist()
        }
        f_out.write(json.dumps(record, ensure_ascii=False) + '\n')

print(f"Processo concluído! {len(texts)} textos embutidos salvos em: {output_path.resolve()}")




# from sentence_transformers import SentenceTransformer
# from pathlib import Path
# # from sklearn.metrics.pairwise import cosine_similarity
# # from pprint import pprint

# model = SentenceTransformer('all-MiniLM-L12-v2')

# entry = Path('data/bulk_entrys.ndjson')

# entry_embedding = model.encode(entry)
