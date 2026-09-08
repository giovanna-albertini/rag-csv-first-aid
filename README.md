# RAG com CSV — Sistema de Recuperação (FAISS) para Primeiros Socorros

Descrição
--------
Sistema RAG (Retrieval-Augmented Generation) para consultas sobre primeiros socorros usando embeddings e FAISS. Permite construir um índice de vetores a partir de um CSV contendo conteúdo de primeiros socorros e responder perguntas com base apenas no contexto da base.

Principais tecnologias
----------------------
- Python 3.10+
- LangChain (integração com LLMs e embeddings)
- OpenAI (modelos de embeddings e LLM)
- FAISS (armazenamento e busca vetorial)
- tiktoken (tokenização compatível)
- Docker (opcional, para reprodução)
- GitHub Actions (CI) — opcional

Instalação
---------
1. Clone o repositório:
   git clone https://github.com/giovanna-albertini/rag-csv-first-aid.git
2. Crie e ative um ambiente virtual:
   python -m venv .venv
   source .venv/bin/activate
3. Instale dependências:
   pip install -r requirements.txt
4. Adicione seu arquivo CSV em `data/` (nome padrão: `base_primeiros_socorros_400.csv`) e configure a variável de ambiente:
   export OPENAI_API_KEY="sua_chave_aqui"

Uso
---
- Para construir o índice:
  python -m src.rag_csv_first_aid.main --build-index --csv data/base_primeiros_socorros_400.csv
- Para consultar:
  python -m src.rag_csv_first_aid.main --query "Como tratar uma queimadura grave?"

Estrutura
--------
- src/rag_csv_first_aid: código principal
- notebooks: notebook original com experimentos (limpo, sem chaves)
- data: arquivos CSV (não incluir chaves sensíveis)
- docker: Dockerfile e configuração

Boas práticas e segurança
------------------------
- Nunca commitar chaves de API no repositório. Substitua por variáveis de ambiente.
- Use `.env` local ou o mecanismo de Secrets do CI para armazenar chaves em ambientes remotos.
- Valide e sanitize o conteúdo do CSV antes de indexar.

Licença
-------
MIT (padrão). Mudar se preferir outra.
