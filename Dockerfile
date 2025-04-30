# Usa imagem oficial leve do Python
FROM python:3.11-slim

# Evita criação de arquivos pyc e deixa output mais limpo
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instala dependências de sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# Agora copia o restante do projeto
COPY . /app/
 # Define o diretório de trabalho
WORKDIR /app
ENV PYTHONPATH=/app

# Copia só os requirements para instalar dependências
COPY requirements.txt /app/

# Instala dependências Python
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expõe porta padrão
EXPOSE 8000

# Comando para rodar o servidor
CMD ["gunicorn", "vitor_news.wsgi:application", "--bind", "0.0.0.0:8000"]

# Dá permissão de execução ao entrypointt
RUN chmod +x entrypoint.sh

# Comando padrão
CMD ["./entrypoint.sh"]
