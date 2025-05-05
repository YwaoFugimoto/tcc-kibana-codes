#!/bin/bash
# Itera pelos primeiros caracteres de 'a' a 'd'
for first in {a..c}; do
  # Itera pelos segundos caracteres de 'a' a 'y'
  for second in {a..y}; do
    file="bulk_part_${first}${second}"
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
