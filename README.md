
## Passos para importar os dados

Baixe os dados em https://www.cnj.jus.br/owncloud/index.php/s/yIby5NidzxB1sQ8

Descompacte os dados
```
unzip base.zip 
```

```
find . -iname '*.zip' -exec sh -c 'unzip -o -d "${0%.*}" "$0"' '{}' ';'
```

Iniciando o MongoDB
```
docker run --rm -d -p 27017:27017 -p 28017:28017 -e AUTH=no -it -v mongodata:/data/db mongo
```

Importando os dados
```
pip install -r requirements.txt
```

```
python import.py
```
