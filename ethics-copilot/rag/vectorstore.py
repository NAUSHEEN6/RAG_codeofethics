import chromadb

from app.config import CHROMA_PATH


COLLECTION_NAME = "code_of_ethics_v3"


def get_collection():

    client = chromadb.PersistentClient(
        path=CHROMA_PATH
    )

    return client.get_collection(
        name=COLLECTION_NAME
    )