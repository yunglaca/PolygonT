FROM python:3.12-slim as app
WORKDIR /polygonT
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["./start.sh"]

