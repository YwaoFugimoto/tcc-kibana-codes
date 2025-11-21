#!/bin/bash
for file in formulas_embedding/chunks/chunk_formulas_*; do
    if [ -f "$file" ]; then
      echo "Indexando $file..."
      curl -u elastic:user123 -k -X POST "https://localhost:9200/_bulk" \
        -H "Content-Type: application/x-ndjson" \
        --data-binary @"$file"
      echo ""
    else
      echo "Arquivo $file não encontrado. Pulando..."
    fi
  done
done

echo "Processo concluído."
