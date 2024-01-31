FROM python:3.11-slim
WORKDIR /app
COPY ./ .
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt
COPY ./app ./app
EXPOSE 8888
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8888"]