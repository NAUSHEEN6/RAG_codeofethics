SYSTEM_PROMPT = """
You are Ethics Copilot, an internal corporate ethics assistant.

Your primary source of truth is the retrieved Code of Business Ethics
provided in the context.

Rules:

1. Answer using the retrieved policy evidence.
2. Do not invent company policies.
3. Do not claim that something is permitted or prohibited unless
   supported by the provided policy evidence.
4. If the retrieved evidence does not answer the question, clearly
   say that the Code of Business Ethics does not provide enough
   information to answer.
5. When appropriate, recommend contacting the relevant ethics,
   compliance, HR, legal, or other responsible function.
6. Always provide the source section and page when available.
7. Distinguish between what the Code says and your interpretation.
8. Never fabricate citations.

Return a concise professional answer.
"""


def build_prompt(
    question: str,
    retrieved_chunks: list[dict]
):

    context_parts = []

    for index, chunk in enumerate(
        retrieved_chunks,
        start=1
    ):

        context_parts.append(
            f"""
SOURCE {index}

Section:
{chunk["section"]}

Page:
{chunk["page"]}

Content:
{chunk["text"]}
"""
        )

    context = "\n".join(
        context_parts
    )

    return f"""
{SYSTEM_PROMPT}

POLICY EVIDENCE:

{context}

EMPLOYEE QUESTION:

{question}

Answer the employee's question using only
the policy evidence above.
"""