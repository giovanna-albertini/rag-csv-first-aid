FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "-m", "src.rag_csv_first_aid.main", "--query", "Como tratar uma queimadura grave?"]
