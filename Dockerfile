FROM python:3.11-slim 

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt


COPY . . 

EXPOSE 5000

CMD ["bash", "-c", "echo 'this image was created by nir' && flask --app app.py init-db && python app.py"]
