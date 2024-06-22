### API service using minio storage for saving photos.
MinIO - S3-compatible storage
#### How to start:
1. include docker-compose.yml
2. python3.12 -m venv venv
3. source venv/bin/activate
4. pip install -r requirements.txt
5. uvicorn main:app --reload




#### additional checks for MinIO:<br>
nc -zv 127.0.0.1 9000<br>
docker-compose logs -f<br>
docker logs minio<br>
http://localhost:9001/browser/images/
