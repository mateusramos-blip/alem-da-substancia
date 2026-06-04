FROM ghcr.io/astral-sh/uv:python3.12-alpine

WORKDIR /app

# Copia os arquivos de configuração do projeto
COPY pyproject.toml uv.lock ./

# Instala as dependências usando o uv de forma otimizada
RUN uv sync --frozen --no-cache

# Copia o resto do código fonte
COPY . .

# Expõe a porta padrão que o Render utiliza
EXPOSE 10000

# Executa o servidor Flask garantindo que ele escute na porta correta
CMD ["uv", "run", "python", "-m", "flask", "run", "--host=0.0.0.0", "--port=10000"]