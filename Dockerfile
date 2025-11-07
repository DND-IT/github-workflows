FROM python:3.13-slim
ENV PYTHONUNBUFFERED=1

WORKDIR /app/

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY ./requirements.txt /app/requirements.txt

RUN pip install -Ur requirements.txt

EXPOSE 8000

CMD ["mkdocs", "serve"]
