FROM python:3.10

WORKDIR /app

COPY requirements.txt requirements.txt

RUN  pip install --upgrade pip \
     && pip install -r requirements.txt --no-cache-dir

COPY . /app
#RUN sh init.sh
CMD ["python", "main.py"]
#["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8081"]