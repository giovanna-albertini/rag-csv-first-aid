# RAG com CSV + FAISS

Projeto de **Retrieval-Augmented Generation (RAG)** para demonstrar recuperação semântica de conhecimento estruturado em CSV.

O dataset experimental contém conteúdo de primeiros socorros, mas o objetivo do repositório é demonstrar a **arquitetura RAG**, não fornecer orientação médica.

## Arquitetura

```text
CSV
 ↓
Carregamento e preparação
 ↓
Chunking
 ↓
Embeddings
 ↓
FAISS Vector Store
 ↓
Semantic Retrieval
 ↓
Contexto recuperado
 ↓
LLM
 ↓
Resposta contextualizada
```

## Tecnologias

- Python 3.10+
- LangChain
- OpenAI embeddings / LLM
- FAISS
- tiktoken
- Docker (estrutura preparada)
- python-dotenv

## Objetivo técnico

Demonstrar como uma fonte tabular pode ser convertida em uma base pesquisável semanticamente, permitindo recuperar trechos relevantes antes da geração da resposta.

## Execução

```bash
pip install -r requirements.txt
export OPENAI_API_KEY="sua_chave"

python -m src.rag_csv_first_aid.main \
  --build-index \
  --csv data/base_primeiros_socorros_400.csv

python -m src.rag_csv_first_aid.main \
  --query "Pergunta de exemplo"
```

## Estrutura

```text
rag-csv-first-aid/
├── src/
├── notebooks/
├── data/
├── docker/
├── requirements.txt
├── .gitignore
└── LICENSE
```

## Segurança e limitações

- chaves devem ser fornecidas por variável de ambiente;
- respostas de LLM podem conter erros;
- o dataset de demonstração não transforma a aplicação em fonte médica confiável;
- aplicações de alto risco exigem fontes validadas, avaliação, guardrails e revisão especializada.

## Próximas evoluções

- trocar o domínio de demonstração por documentação técnica;
- avaliação de retrieval (Recall@K / MRR);
- reranking;
- metadata filtering;
- testes automatizados;
- FastAPI e containerização executável;
- tracing de prompts e respostas.

## Competências demonstradas

`RAG` · `Embeddings` · `Vector Search` · `FAISS` · `LangChain` · `LLMs` · `Python` · `AI Engineering`
