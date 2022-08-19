FROM python:3.8-slim
WORKDIR /app
RUN pip3 install --no-cache-dir pika loguru
COPY receive.py ./ 
CMD python3 /app/receive.py --rabbit $RABBIT_URL
