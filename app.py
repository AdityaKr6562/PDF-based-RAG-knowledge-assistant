import streamlit as st
from pathlib import Path

from src.document_loader import load_pdf
from src.chunker import chunk_pages
from src.embeddings import create_embeddings
from src.vector_store import VectorStore
from src.generator import generate_answer


# ==================================================
# CONFIGURATION
# ==================================================

DOCUMENT_DIR = Path("data/documents")
VECTORSTORE_DIR = "vectorstore"


DOCUMENT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="AI Knowledge Assistant",
    page_icon="🤖",
    layout="wide"
)


# ==================================================
# TITLE
# ==================================================

st.title("🤖 Mini AI Knowledge Assistant")

st.markdown(
    """
Ask questions about your uploaded documents using
**Retrieval-Augmented Generation (RAG)**.

The system retrieves relevant information from your
documents and uses a local **Qwen3 LLM through Ollama**
to generate the answer.
"""
)


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.header("📄 Knowledge Base")

    uploaded_files = st.file_uploader(
        "Upload PDF documents",
        type=["pdf"],
        accept_multiple_files=True
    )

    build_button = st.button(
        "🔨 Build Knowledge Base",
        use_container_width=True
    )

    st.divider()

    st.header("⚙️ System")

    st.write("**Embedding Model**")
    st.code("all-MiniLM-L6-v2")

    st.write("**Vector Store**")
    st.code("FAISS")

    st.write("**LLM**")
    st.code("Qwen3 8B")

    st.write("**LLM Runtime**")
    st.code("Ollama")


# ==================================================
# BUILD KNOWLEDGE BASE
# ==================================================

if build_button:

    if not uploaded_files:

        st.warning(
            "Please upload at least one PDF."
        )

    else:

        with st.spinner(
            "Building knowledge base..."
        ):

            # ------------------------------------------
            # Save uploaded PDFs
            # ------------------------------------------

            for uploaded_file in uploaded_files:

                file_path = (
                    DOCUMENT_DIR /
                    uploaded_file.name
                )

                with open(
                    file_path,
                    "wb"
                ) as file:

                    file.write(
                        uploaded_file.getbuffer()
                    )


            # ------------------------------------------
            # Extract and chunk documents
            # ------------------------------------------

            all_chunks = []

            pdf_files = list(
                DOCUMENT_DIR.glob("*.pdf")
            )


            for pdf_file in pdf_files:

                pages = load_pdf(
                    pdf_file
                )

                chunks = chunk_pages(
                    pages
                )

                all_chunks.extend(
                    chunks
                )


            if not all_chunks:

                st.error(
                    "No readable text was found "
                    "in the uploaded PDFs."
                )

                st.stop()


            # ------------------------------------------
            # Generate embeddings
            # ------------------------------------------

            texts = [
                chunk["text"]
                for chunk in all_chunks
            ]

            embeddings = create_embeddings(
                texts
            )


            # ------------------------------------------
            # Create FAISS database
            # ------------------------------------------

            dimension = embeddings.shape[1]

            store = VectorStore(
                dimension
            )

            store.add(
                embeddings,
                all_chunks
            )

            store.save(
                VECTORSTORE_DIR
            )


        # ------------------------------------------
        # Success
        # ------------------------------------------

        st.success(
            f"Knowledge base created successfully! "
            f"{len(all_chunks)} chunks indexed."
        )


# ==================================================
# CHAT HISTORY
# ==================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# ==================================================
# DISPLAY PREVIOUS MESSAGES
# ==================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

        if (
            message["role"] == "assistant"
            and "sources" in message
        ):

            with st.expander("📚 Sources"):

                for source in message["sources"]:

                    st.write(
                        f"📄 {source['source']} "
                        f"— Page {source['page']}"
                    )


# ==================================================
# CHAT INPUT
# ==================================================

question = st.chat_input(
    "Ask a question about your documents..."
)


if question:

    # ----------------------------------------------
    # Check knowledge base
    # ----------------------------------------------

    if not Path(
        VECTORSTORE_DIR,
        "index.faiss"
    ).exists():

        st.error(
            "Please upload a PDF and build "
            "the knowledge base first."
        )

        st.stop()


    # ----------------------------------------------
    # Display user question
    # ----------------------------------------------

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })


    with st.chat_message("user"):

        st.markdown(question)


    # ----------------------------------------------
    # Retrieve relevant chunks
    # ----------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "Searching documents..."
        ):

            store = VectorStore.load(
                VECTORSTORE_DIR
            )

            query_embedding = create_embeddings(
                [question]
            )[0]

            results = store.search(
                query_embedding,
                k=5
            )


        # ------------------------------------------
        # Generate answer
        # ------------------------------------------

        with st.spinner(
            "Generating answer..."
        ):

            answer = generate_answer(
                question,
                results
            )


        st.markdown(answer)


        # ------------------------------------------
        # Sources
        # ------------------------------------------

        unique_sources = []

        seen = set()

        for result in results:

            key = (
                result["source"],
                result["page"]
            )

            if key not in seen:

                unique_sources.append({
                    "source": result["source"],
                    "page": result["page"]
                })

                seen.add(key)


        with st.expander("📚 Sources"):

            for source in unique_sources:

                st.write(
                    f"📄 {source['source']} "
                    f"— Page {source['page']}"
                )


    # ----------------------------------------------
    # Save assistant message
    # ----------------------------------------------

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": unique_sources
    })