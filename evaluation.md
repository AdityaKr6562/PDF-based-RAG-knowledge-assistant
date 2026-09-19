# RAG Evaluation

## Objective

The system was tested to verify:

1. PDF content extraction
2. Semantic retrieval
3. Answer generation
4. Source citation
5. Resistance to questions outside the knowledge base

## Test Document

**Student-Code-of-Conduct.pdf**

- Pages: 10
- Chunks: 41
- Embedding dimension: 384

## Test Cases

| Test | Question Type | Expected Result | Result |
|---|---|---|---|
| TC-01 | Information present in PDF | Relevant answer | Pass |
| TC-02 | Information present in PDF | Relevant source page retrieved | Pass |
| TC-03 | Another document-related question | Relevant answer | Pass |
| TC-04 | Information not present | System should state information is unavailable | Pass |
| TC-05 | Multiple questions | Conversation history maintained | Pass |

## Retrieval

The system uses:

- Sentence Transformers: `all-MiniLM-L6-v2`
- FAISS vector similarity search
- Top-5 retrieved chunks

The knowledge base contained:

- 41 chunks
- 384-dimensional embeddings

## Generation

The retrieved chunks are passed to:

**Qwen3 8B via Ollama**

The generation prompt instructs the model to:

- Use only retrieved document context
- Avoid unsupported information
- State when the answer cannot be found

## Source Attribution

Each retrieved chunk stores:

- Document filename
- Page number

The Streamlit interface displays these as sources below each answer.

## Limitations

- Scanned/image-only PDFs are not currently processed with OCR.
- Retrieval quality depends on chunk size and embedding quality.
- The local LLM may occasionally generate unsupported information despite grounding instructions.
- The application currently uses a fixed top-k retrieval value.

## Future Improvements

- OCR support
- Hybrid keyword + semantic search
- Reranking
- Retrieval evaluation metrics
- Cloud deployment
- Support for additional document formats