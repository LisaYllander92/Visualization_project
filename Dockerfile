FROM python:3.13

WORKDIR /app

COPY pyproject.toml .

RUN pip install uv && uv sync

COPY . .

RUN mkdir /app/output

# streamlit port
EXPOSE 8501

CMD ["uv", "run", "streamlit", "run", "main.py"]