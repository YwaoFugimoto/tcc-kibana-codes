#!/usr/bin/env python3
import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
import sys

# --- Configurações ---

# Define o diretório base como o local do script
SCRIPT_DIR = Path(__file__).parent.resolve()

# Caminhos de entrada e saída (relativos ao local do script)
INPUT_PATH   = SCRIPT_DIR / 'wiki_modified.json'
OUTPUT_PATH  = SCRIPT_DIR / 'bulk_wikipedia_with_embeddings.ndjson'

# Configurações do Modelo e Processamento
MODEL_NAME   = 'all-MiniLM-L12-v2' # ⚠️ ATENÇÃO: Gera 384 dimensões!
BATCH_SIZE   = 64   # Ajuste conforme a VRAM da sua GPU
CHUNK_SIZE   = 512  # Quantos *documentos* (pares de linhas) processar por vez
CONTENT_FIELD = "content" # Campo que contém o texto para gerar o embedding

# --- Fim das Configurações ---

print(f"Carregando modelo '{MODEL_NAME}'... (pode levar um momento)")
try:
    model = SentenceTransformer(MODEL_NAME)
except Exception as e:
    print(f"Erro ao carregar o modelo: {e}")
    print("Por favor, garanta que você tenha 'sentence-transformers' instalado no seu venv.")
    print("Lembre-se de ativar o venv: source .venv/bin/activate")
    sys.exit(1)

# Verifica a dimensão do modelo e avisa sobre o mapping
model_dims = model.get_sentence_embedding_dimension()
print(f"Modelo carregado. Dimensão dos embeddings: {model_dims}")
if model_dims != 768: # O valor que você tinha no mapping anterior


print(f"Iniciando processamento de {INPUT_PATH.name}...")

try:
    with INPUT_PATH.open('r', encoding='utf-8') as fin, OUTPUT_PATH.open('w', encoding='utf-8') as fout:
        total = 0
        
        # Listas para guardar o "lote" (chunk)
        action_lines_chunk = []
        data_objects_chunk = []
        texts_to_embed_chunk = []

        while True:
            # Lemos o arquivo em pares: linha de ação, linha de dados
            action_line = fin.readline()
            data_line = fin.readline()

            # Se qualquer uma das linhas estiver vazia, chegamos ao fim do arquivo
            if not action_line or not data_line:
                break

            action_line = action_line.strip()
            data_line = data_line.strip()

            if not action_line or not data_line:
                continue

            try:
                # A linha de ação não precisa ser lida, apenas guardada
                data_obj = json.loads(data_line)
            except json.JSONDecodeError:
                print(f"Aviso: Linha de dados mal formatada, pulando par: {data_line}")
                continue

            # Pega o texto do campo de conteúdo especificado
            text_to_embed = data_obj.get(CONTENT_FIELD, '')

            # Se não houver texto, apenas escrevemos as linhas originais e pulamos
            if not text_to_embed:
                fout.write(action_line + "\n")
                fout.write(data_line + "\n")
                continue
            
            # Adiciona ao nosso lote (chunk)
            action_lines_chunk.append(action_line)
            data_objects_chunk.append(data_obj)
            texts_to_embed_chunk.append(text_to_embed)

            # Quando o lote (chunk) estiver cheio, processa
            if len(texts_to_embed_chunk) >= CHUNK_SIZE:
                print(f"Processando lote de {len(texts_to_embed_chunk)} documentos...")
                embeddings = model.encode(
                    texts_to_embed_chunk, 
                    batch_size=BATCH_SIZE, 
                    show_progress_bar=True
                )
                
                # Adiciona o embedding e escreve no arquivo de saída
                for action, data, emb in zip(action_lines_chunk, data_objects_chunk, embeddings):
                    data['embedding'] = emb.tolist() # Adiciona o campo embedding
                    fout.write(action + "\n")
                    fout.write(json.dumps(data, ensure_ascii=False) + "\n")
                
                total += len(texts_to_embed_chunk)
                
                # Limpa os lotes
                action_lines_chunk.clear()
                data_objects_chunk.clear()
                texts_to_embed_chunk.clear()

        # Processa qualquer item restante no lote final
        if texts_to_embed_chunk:
            print(f"Processando lote final de {len(texts_to_embed_chunk)} documentos...")
            embeddings = model.encode(
                texts_to_embed_chunk, 
                batch_size=BATCH_SIZE, 
                show_progress_bar=True
            )
            
            for action, data, emb in zip(action_lines_chunk, data_objects_chunk, embeddings):
                data['embedding'] = emb.tolist() # Adiciona o campo embedding
                fout.write(action + "\n")
                fout.write(json.dumps(data, ensure_ascii=False) + "\n")
            
            total += len(texts_to_embed_chunk)

    print("\n---")
    print(f"✅ Processo concluído!")
    print(f"{total} embeddings foram gerados e salvos em:")
    print(f"{OUTPUT_PATH.resolve()}")

except FileNotFoundError:
    print(f"Erro: Arquivo de entrada não encontrado em {INPUT_PATH}")
    print("Verifique se o arquivo 'wiki_modified.json' está no mesmo diretório do script.")
except Exception as e:
    print(f"Ocorreu um erro inesperado: {e}")