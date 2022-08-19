FROM python:3.8-slim
WORKDIR /app
RUN pip3 install --no-cache-dir pika loguru
COPY send.py ./ 
CMD python3 /app/send.py --rabbit $RABBIT_URL
