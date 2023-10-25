from concurrent.futures import ThreadPoolExecutor
from fastapi import FastAPI
from dotenv import load_dotenv
from api.sqlite_to_postgres.load_data import run

executor = ThreadPoolExecutor(max_workers=3)
app = FastAPI()
load_dotenv()


@app.get("/")
def main_page():
    return 'Data Transfer (from sqlite to postgres)'


@app.get("/migrate")
def migrate_from_sqlite_to_postgres():
    executor.submit(run)
    return {"result": "Start migrate data"}
