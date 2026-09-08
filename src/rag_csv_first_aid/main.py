#!/usr/bin/env python3
"""
Pipeline RAG para CSV — modular, com CLI mínima.
- build-index: lê CSV, chunking, cria embeddings e salva FAISS index.
- query: carrega index e responde perguntas usando o LLM.
"""
import os
import argparse
import logging
from pathlib import Path
from typing import List

# LangChain imports
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS

# Some message utilities (versions of langchain differ; we handle calls safely)
try:
    from langchain.schema import HumanMessage
except Exception:
    HumanMessage = None

# Config logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

INDEX_DIR = Path("index")
INDEX_PATH = INDEX_DIR / "faiss_index"

def load_documents(csv_path: str, encoding: str = "utf-8"):
    loader = CSVLoader(file_path=csv_path, encoding=encoding)
    docs = loader.load()
    logger.info("Documentos carregados: %d", len(docs))
    return docs

def split_documents(documents, chunk_size=500, chunk_overlap=50):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = splitter.split_documents(documents)
    logger.info("Chunks geradas: %d", len(chunks))
    return chunks

def create_embeddings(model_name="text-embedding-3-small"):
    emb = OpenAIEmbeddings(model=model_name)
    return emb

def build_index(chunks, embeddings, index_path: Path = INDEX_PATH):
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    vector_store = FAISS.from_documents(documents=chunks, embedding=embeddings)
    vector_store.save_local(str(index_path))
    logger.info("Índice salvo em: %s", index_path)
    return vector_store

def load_index(embeddings, index_path: Path = INDEX_PATH):
    if not index_path.exists():
        raise FileNotFoundError("Índice FAISS não encontrado. Rode --build-index primeiro.")
    vs = FAISS.load_local(str(index_path), embeddings)
    logger.info("Índice carregado de: %s", index_path)
    return vs

def query_index(vector_store, question: str, k: int = 3):
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": k})
    # Depending on langchain version, the retriever API can vary
    if hasattr(retriever, 'get_relevant_documents'):
        results = retriever.get_relevant_documents(question)
    else:
        # fallback to similarity_search
        results = vector_store.similarity_search(question, k=k)
    return results

def format_docs(docs: List):
    return "\n\n".join(getattr(d, 'page_content', str(d)) for d in docs)

def answer_with_llm(context: str, question: str):
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    prompt = (
        "Você é um assistente especialista em primeiros socorros.\n"
        "Responda a pergunta utilizando apenas as informações do contexto fornecido.\n\n"
        f"Contexto:\n{context}\n\nPergunta: {question}\n"
    )
    try:
        if HumanMessage is not None:
            response = llm([HumanMessage(content=prompt)])
            # try to get text
            if hasattr(response, 'generations'):
                answer = response.generations[0][0].text
            elif isinstance(response, list) and len(response) and hasattr(response[0], 'content'):
                answer = response[0].content
            else:
                answer = str(response)
        else:
            # fallback: call llm as a simple callable
            response = llm(prompt)
            if hasattr(response, 'generations'):
                answer = response.generations[0][0].text
            else:
                answer = str(response)
    except Exception as e:
        answer = f"Erro ao chamar o LLM: {e}\n\nPrompt:\n{prompt}"
    return answer


def main():
    parser = argparse.ArgumentParser(description="RAG CSV First Aid")
    parser.add_argument("--build-index", action="store_true", help="Build FAISS index from CSV")
    parser.add_argument("--csv", type=str, help="Path to CSV file")
    parser.add_argument("--query", type=str, help="Query to ask the index")
    parser.add_argument("--k", type=int, default=3, help="Número de documentos a recuperar")
    args = parser.parse_args()

    # Ensure OPENAI_API_KEY is set
    if os.environ.get('OPENAI_API_KEY') is None:
        logger.warning('OPENAI_API_KEY não definida. Algumas operações podem falhar.')

    if args.build_index:
        if not args.csv:
            raise SystemExit("Forneça --csv path/to.csv para construir o índice.")
        docs = load_documents(args.csv)
        chunks = split_documents(docs)
        embeddings = create_embeddings()
        build_index(chunks, embeddings)
        logger.info("Build concluído.")
        return

    if args.query:
        embeddings = create_embeddings()
        vs = load_index(embeddings)
        docs = query_index(vs, args.query, k=args.k)
        context = format_docs(docs)
        answer = answer_with_llm(context, args.query)
        print("=== Resposta ===")
        print(answer)
        return

    parser.print_help()

if __name__ == "__main__":
    main()
