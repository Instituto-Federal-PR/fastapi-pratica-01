# Imagem oficial e leve (slim) do Python  
FROM python:3.12-slim

# Cria um usuário correspondente ao seu usuário local para evitar problemas de permissão
RUN useradd -u 1000 -m appuser

# Define o diretório de trabalho dentro do container
WORKDIR /code

# Garante que a pasta pertence ao novo usuário
RUN chown appuser:appuser /code

# Copia o arquivo de requerimentos primeiro (ajuda no cache do Docker)
COPY ./requirements.txt /code/requirements.txt

# Instala as dependências do Python
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copia todo o resto do código para dentro do container
COPY ./app /code/app

# Muda para o usuário não-root antes de rodar a aplicação
USER appuser

# Comando para rodar o servidor Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]