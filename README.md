# Заключительное задание первого модуля

`data_transfer_sqlite_to_pg` - образ с прошлых заданий для заполнения Postgres

## Installation
### 1 step

create **.env** file based on **.env.example**<br>

### 2 step
Сборка проекта
```bash
docker-compose up -d --build
```

### 3 step
Заполнение базы данных

```bash
curl -XGET http://0.0.0.0:8888/migrate
```

### 4 step
Проверить выполнения запроса к ElasticSearch

```bash
curl -XGET http://127.0.0.1:9200/movies/_search/ -H 'Content-Type: application/json' -d '{
    "query": {
        "bool": {
            "must": [
                {"match": {"title": "star"}}
            ]
        }
    }
}'
```
