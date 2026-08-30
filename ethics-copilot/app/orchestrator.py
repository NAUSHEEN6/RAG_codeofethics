from rag.retriever import search_policy

from app.prompts import build_prompt

from integrations.gemini import (
    generate_response
)


def answer_ethics_question(
    question: str
):

    # -----------------------------------------------------
    # STEP 1: RAG
    # -----------------------------------------------------

    retrieved = search_policy(
        question,
        top_k=5
    )

    # -----------------------------------------------------
    # STEP 2: Build grounded prompt
    # -----------------------------------------------------

    prompt = build_prompt(
        question,
        retrieved
    )

    # -----------------------------------------------------
    # STEP 3: LLM
    # -----------------------------------------------------

    answer = generate_response(
        prompt
    )

    return {
        "question": question,
        "answer": answer,
        "sources": retrieved
    }