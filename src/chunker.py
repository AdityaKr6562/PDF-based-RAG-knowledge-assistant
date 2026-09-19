def chunk_pages(pages, chunk_size=800, overlap=150):
    """
    Split page text into overlapping chunks.

    Each chunk retains its original
    document and page metadata.
    """

    chunks = []

    for page in pages:

        text = page["text"]

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunk_text = text[start:end].strip()

            if chunk_text:

                chunks.append({
                    "text": chunk_text,
                    "source": page["source"],
                    "page": page["page"]
                })

            start += chunk_size - overlap

    return chunks