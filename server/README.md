# Schemacrawler

Подключение контейнера к сети
```bash
docker run -v $(pwd):/home/schcrwlr/share --name schemacrawler --rm -i -t --entrypoint=/bin/bash schemacrawler/schemacrawler
docker network connect ... schemacrawler
```

***
Активация окружения контейнера
```bash
schemacrawler --shell
```

***
Подключение к БД и построение схемы
```bash
connect --server=postgresql --host=... --user=... --password=... --database=...
load --info-level=maximum
execute --command list
execute --command=schema --output-format=png --output-file=graph.png
```