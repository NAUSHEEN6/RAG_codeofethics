from pathlib import Path
import re

import pymupdf
import chromadb
from sentence_transformers import SentenceTransformer


# =========================================================
# CONFIGURATION
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"
VECTORSTORE_DIR = PROJECT_ROOT / "vectorstore"

PDF_PATH = DATA_DIR / "code_of_ethics.pdf"

COLLECTION_NAME = "code_of_ethics_v3"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150


# =========================================================
# KNOWN DOCUMENT STRUCTURE
# =========================================================

# These are section headings observed in the actual
# Code of Business Ethics document.
#
# We use them ONLY for structural parsing.
#
# The actual policy content always comes from the PDF.

KNOWN_SECTIONS = [
    "1. Our Code of Business Ethics",

    "1.1 What is our Code of Business Ethics?",
    "1.2 Who is it for and what are our roles?",
    "1.3 SpeakUp",

    "2. People",

    "2.1 Health and safety",
    "2.2 Equality, diversity, and inclusion",
    "2.3 Harassment",
    "2.4 Open dialogue",
    "2.5 Behavior at work and work-related events",

    "3. Business integrity",

    "3.1 Fair competition",
    "3.2 Bribery and corruption",
    "3.3 Conflict of interest",
    "3.4 Insider trading",
    "3.5 Accurate and correct business and financial information",
    "3.6 Political activities",

    "4. Business relationships",

    "4.1 Working with our clients",
    "4.2 Working with our partners and ecosystems",
    "4.3 Working with our suppliers",

    "5. Group and",

    "6. Corporate social responsibility",
]


# =========================================================
# NORMALIZATION
# =========================================================

def normalize_text(text: str) -> str:

    text = text.replace(
        "\x00",
        " "
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# =========================================================
# SECTION MATCHING
# =========================================================

def find_section_in_text(
    text: str,
    current_section: str
) -> str:

    normalized = normalize_text(
        text
    )

    # -----------------------------------------------------
    # Ignore obvious table-of-contents lines
    # -----------------------------------------------------

    if "..." in normalized:
        return current_section

    # Lines ending with page numbers from TOC
    if re.search(
        r"\s+\d{1,2}$",
        normalized
    ) and len(normalized) < 100:

        # Don't automatically accept these as headings
        return current_section

    # -----------------------------------------------------
    # Exact section matching
    # -----------------------------------------------------

    for section in KNOWN_SECTIONS:

        if normalized == normalize_text(section):

            return section

    # -----------------------------------------------------
    # Special handling for split headings
    # -----------------------------------------------------

    if normalized == "1. Our Code of":

        return "1. Our Code of Business Ethics"

    if normalized == "2. Business":

        return current_section

    if normalized == "3. Business":

        return current_section

    if normalized == "4. Business":

        return current_section

    if normalized == "5. Group and":

        return current_section

    if normalized == "6. Corporate social":

        return current_section

    return current_section


# =========================================================
# EXTRACT PDF
# =========================================================

def extract_document(
    pdf_path: Path
) -> list[dict]:

    if not pdf_path.exists():

        raise FileNotFoundError(
            f"PDF not found: {pdf_path}"
        )

    document = pymupdf.open(
        pdf_path
    )

    pages = []

    current_section = "Unknown"

    for page_number, page in enumerate(
        document,
        start=1
    ):

        raw_text = page.get_text(
            "text"
        )

        lines = raw_text.splitlines()

        cleaned_lines = []

        for raw_line in lines:

            line = normalize_text(
                raw_line
            )

            if not line:
                continue

            new_section = find_section_in_text(
                line,
                current_section
            )

            if new_section != current_section:

                current_section = new_section

            cleaned_lines.append(
                line
            )

        page_text = "\n".join(
            cleaned_lines
        )

        if page_text.strip():

            pages.append(
                {
                    "page": page_number,
                    "section": current_section,
                    "text": page_text,
                }
            )

    document.close()

    return pages


# =========================================================
# CREATE CHUNKS
# =========================================================

def create_chunks(
    pages: list[dict],
    chunk_size: int = CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP,
) -> list[dict]:

    chunks = []

    chunk_number = 0

    for page in pages:

        text = page["text"]

        page_number = page["page"]

        section = page["section"]

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunk_text = text[
                start:end
            ].strip()

            if chunk_text:

                chunks.append(
                    {
                        "chunk_id":
                            f"ethics_v3_{chunk_number}",

                        "page":
                            page_number,

                        "section":
                            section,

                        "text":
                            chunk_text,
                    }
                )

                chunk_number += 1

            if end >= len(text):

                break

            start += (
                chunk_size - overlap
            )

    return chunks


# =========================================================
# CREATE CHROMA COLLECTION
# =========================================================

def create_vectorstore(
    chunks: list[dict]
):

    print(
        "\nLoading embedding model..."
    )

    model = SentenceTransformer(
        EMBEDDING_MODEL
    )

    print(
        "Embedding model loaded."
    )

    VECTORSTORE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    client = chromadb.PersistentClient(
        path=str(
            VECTORSTORE_DIR
        )
    )

    # Delete previous V3 collection
    existing_names = [
        collection.name
        for collection in
        client.list_collections()
    ]

    if COLLECTION_NAME in existing_names:

        client.delete_collection(
            name=COLLECTION_NAME
        )

    collection = client.create_collection(
        name=COLLECTION_NAME
    )

    documents = [
        chunk["text"]
        for chunk in chunks
    ]

    ids = [
        chunk["chunk_id"]
        for chunk in chunks
    ]

    metadatas = [
        {
            "document":
                "Code of Business Ethics",

            "page":
                chunk["page"],

            "section":
                chunk["section"],

            "chunk_id":
                chunk["chunk_id"],
        }
        for chunk in chunks
    ]

    print(
        f"\nCreating embeddings "
        f"for {len(documents)} chunks..."
    )

    embeddings = model.encode(
        documents,
        show_progress_bar=True
    ).tolist()

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    return collection


# =========================================================
# DISPLAY SECTIONS
# =========================================================

def display_sections(
    pages: list[dict]
):

    print("\n")
    print("=" * 80)
    print("DETECTED DOCUMENT SECTIONS")
    print("=" * 80)

    previous = None

    for page in pages:

        section = page["section"]

        if section != previous:

            print(
                f"Page {page['page']:>2} "
                f"→ {section}"
            )

            previous = section


# =========================================================
# MAIN
# =========================================================

def main():

    print("=" * 80)

    print(
        "ETHICS COPILOT - "
        "SECTION-AWARE INGESTION V3"
    )

    print("=" * 80)

    print(
        f"\nPDF: {PDF_PATH}"
    )

    print(
        "\nExtracting document..."
    )

    pages = extract_document(
        PDF_PATH
    )

    print(
        f"Extracted "
        f"{len(pages)} pages."
    )

    display_sections(
        pages
    )

    print(
        "\nCreating chunks..."
    )

    chunks = create_chunks(
        pages
    )

    print(
        f"Created "
        f"{len(chunks)} chunks."
    )

    collection = create_vectorstore(
        chunks
    )

    print("\n")

    print("=" * 80)

    print(
        "INGESTION COMPLETE"
    )

    print("=" * 80)

    print(
        f"\nCollection: "
        f"{COLLECTION_NAME}"
    )

    print(
        f"Chunks: "
        f"{collection.count()}"
    )


if __name__ == "__main__":
    main()