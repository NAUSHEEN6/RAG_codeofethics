from rag.vectorstore import get_collection
from rag.embeddings import create_embedding


def search_policy(
    question: str,
    top_k: int = 5
):

    collection = get_collection()

    query_embedding = create_embedding(
        question
    )

    results = collection.query(
        query_embeddings=[
            query_embedding
        ],
        n_results=top_k,
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    retrieved = []

    for i in range(
        len(results["documents"][0])
    ):

        retrieved.append(
            {
                "text":
                    results["documents"][0][i],

                "page":
                    results["metadatas"][0][i][
                        "page"
                    ],

                "section":
                    results["metadatas"][0][i][
                        "section"
                    ],

                "distance":
                    results["distances"][0][i]
            }
        )

    return retrieved