FROM python:3.10-slim

WORKDIR /app/
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p media/product_images

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--reload" ]