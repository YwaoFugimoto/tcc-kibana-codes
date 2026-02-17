# Process Documentation

### First install the formula's dump:
    - Link: https://drive.google.com/file/d/19lkA3h_CKD8U-Utfyj8I0XFVdtJ2gmFV/view?usp=sharing


Este é o arquivo base.
A seguir uma lista dos scripts e suas respectivas funções:

'''
- formulas_som.py 
    - Este arquivo remove todos os campos do dump inicial, deixando apenas "id" e "formulas_som" no corpo.

- formulas_som_inline.py
    - Este script remove todos os campos e lista todas as formulas,  removendo as repetidas.

    - Retorna um txt, já que remove a estrutura json.

- embedding_code.py
    -
    
'''

A seguir uma lista dos arquivos json e seus estados:

'''
- formulas_extraidas.json
    - Este é o arquivo inicial, extraido diretamente do dump.

- 


- formulas_unicas.txt
    - Arquivo que contem todas as formulas_som por linha e com formulas repetidas removidas.
'''


O codigo JAVA:

Recebe um post: 

" curl -X POST -F "file=@formulas_unicas.txt" http://localhost:8080/api/formulas/process-file " 

A formula deve estar no mesmo diretorio em que a requisição é feita.

Com isso o codigo executa o WSL para rodar grammar2.6.
A aplicação salva a formula e o token, no formato 
[
    {
        "formula": "formula",
        "token": "token",
    }
]

Algumas formulas estão erradas e devem ser limpadas. #TODO 

O output deste processo esta dentro do codigo JAVA (Intelli) 
com o nome de  `first_round.json`


# Executando a fase de teste

- Iniciando o kibana

    - Clonar repo `https://github.com/leonardosantosp/mathseek`
    - Rodar docker compose up -d

- Fazer mapping de: 
    - dumpping do flavio (Elastic normal (Indice Invertido))
    ```
        PUT /wikipedia
        {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0, 
            "index.mapping.coerce": false,
            "analysis": {
            "analyzer": {
                "analyzer_for_content": {
                "type": "custom",
                "char_filter": [ ],
                "tokenizer": "standard",
                "filter": [
                    "asciifolding",
                    "lowercase",
                    "snowball"
                ]
                }
            }
            }
        },
        "mappings": {
            "dynamic": "strict",
            "properties": {
            "title": {
                "type": "text",
                "analyzer": "analyzer_for_content"
            },
            "url": {
                "type": "keyword",
                "doc_values": false,
                "index": false
            },
            "content": {
                "type": "text",
                "analyzer": "analyzer_for_content"
            },
            "dt_creation":{
                "type": "date"
            },
            "reading_time":{
                "type": "integer"
            },
            "access_count": {
                "type": "integer"
            }
            }
        }
        }
    ```

    - Wikipedia semantic (Com embeddings, (busca semantica)):
    ```
    PUT /wikipedia_semantic
    {
        "settings": {
            "number_of_shards": "1",
            "number_of_replicas": "0",
            "analysis": {
            "filter": {
                "port_snow": {
                "type": "snowball",
                "language": "portuguese"
                }
            },
            "analyzer": {
                "my_analyzer": {
                "char_filter": [
                    "html_strip"
                ],
                "tokenizer": "standard",
                "filter": [
                    "asciifolding",
                    "lowercase",
                    "port_snow"
                ],
                "type": "custom"
                }
            }
            }
        },
        "mappings": {
            "properties": {
            "title": {
                "type": "text",
                "fields": {
                "keyword": {
                    "type": "keyword",
                    "ignore_above": 256
                }
                }
            },
            "url": {
                "type": "keyword"
            },
            "content": {
                "type": "text"
            },
            "dt_creation": {
                "type": "date"
            },
            "reading_time": {
                "type": "float"
            },
            "access_count": {
                "type": "integer"
            },
            # Me ajude nesta variavel, ela deve ser um vetor denso
            # Responsavel pelos embeddings
            "embedding": {
                "type": "dense_vector",
                "dims": 768,
                "index": "true",
                "similarity": "cosine",
                "index_options": {
                "type": "hnsw",
                "m": 16,
                "ef_construction": 100
                }
            }
            }
        }
    }
    ```


    
- Executar e criar os mappings.( GET dump-flavio & dump-semantic)

- Para povoar a base primeiro, instalar o dump wiki_modified.json (Classroom do materia: ElasticSearch)
    - Povoar o dump semantic: 
    ```
    curl -H "Content-Type: application/x-ndjson" -XPOST https://localhost:5601/wikipedia/_bulk --data-binary "@wiki_modified.json" --user "elastic:user123" --insecure

    ```


- Adicionando ambiente virtual.



- Quebrar em splits;

- Refazer os mappings, com base nas formulas
Campos 
    - id
    - formula
    - embedding

- Tranformar em tipo elastic (ndjson)
- Splitar para jogar no elastic (Povoar o dump)
    - Sem truncar objeto.


# Final Files

- formulas_elastic.py 
    - Recebe o arquivo `formulas_unicas.txt` e transforma em um objeto json indexavel para o elastic.

    - Proximo passo
        - Gerar embeddings em cima do campo "formula"

    - Gerando embedding para formulas

- add_new_embedding.py
    - Adiciona o campo "embedding" para cada formula em cada objeto da lista ndjson.


- semantic-math-search => Pesquisador

- embedding_service => gera os embeddings

- api => gera os tokens 

- kibana_tcc => docker elastic

ambiente virtual 
create: python3 -m venv .venv

use: source .venv/bin/activate

### Ultimo review

A aplicação principal é `semantic-math-search`, 
para funcionar ambos endpoints é necessario:

- embedding_service estar rodando porta 3000

- token_service (codigo JAVA) estar rodando porta 8080

- elasticsSearch (docker compose de kibana-tcc) estar rodando, para fazer a hit.



### Faz embedding da entrada e procura
GET http://localhost:3000/search-formula?formula=(p(x) = \frac{1}{\sigma \sqrt{2\pi}}e^{-\frac{(x-\mu)^2}{2\sigma^2}})&mode=DIRECT


### Tokeniza a entrada, faz embedding da entrada e procura 
GET http://localhost:3000/search-formula?formula=(p(x) = \frac{1}{\sigma \sqrt{2\pi}}e^{-\frac{(x-\mu)^2}{2\sigma^2}})&mode=TOKENIZED
