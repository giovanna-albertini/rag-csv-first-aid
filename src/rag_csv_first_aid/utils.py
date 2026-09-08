"""
Utilitários do projeto: funções de apoio e tratamento comum.
"""

def format_docs(docs):
    return "\n\n".join(getattr(d, 'page_content', str(d)) for d in docs)
