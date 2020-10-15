import os
import glob

import json
import datetime

from pymongo import MongoClient

from termcolor import colored


ROOT_PATH = "base/"


def path_norm(folder):
    path = os.path.basename(os.path.normpath(folder))
    return path


def get_json_files(folder):
    files = glob.glob(os.path.join(folder, "*.json"))
    return files


def read_json_file(file):
    with open(file) as f:
        data = json.load(f)
        return data


def join_json_files(files):
    documents = []

    for file in files:
        documents.extend(read_json_file(file))

    return documents


def walk(folder):
    subfolders = [f.path for f in os.scandir(folder) if f.is_dir()]

    return [
        (path, path_norm(path))
        for path in subfolders]


def read_documents(folder):
    files = get_json_files(folder)
    documents = join_json_files(files)
    return documents


def insert_rows(database_name, collection_name, rows):
    client = MongoClient("localhost", 27017)

    database = client[database_name]
    collection = database[collection_name]

    collections = database.list_collection_names()
    if collection_name in collections:
        print(colored(f"Drop collection {collection_name}", "yellow"))
        client.db.drop_collection(collection_name)

    collection.insert_many(rows)

    now = datetime.datetime.now()
    
    print(colored(
        f"[{str(now)}] Database: {database_name} - insert {len(rows)} row(s) in {collection_name} collection", "green"))


def import_documents():
    databases = walk(ROOT_PATH)
    for database_path, database_name in databases:
        collections = walk(database_path)
        for collection_path, collection_name in collections:
            documents = read_documents(collection_path)
            insert_rows(database_name, collection_name, documents)


if __name__ == "__main__":
    import_documents()
