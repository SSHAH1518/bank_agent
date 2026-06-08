def chunk_text_by_lines(
        text:str,
        rows_per_chunk:int = 20
):
    lines = text.split("\n")
    chunks = []
    for i in range(0, len(lines), rows_per_chunk):
        chunk = "\n".join(lines[i:i+rows_per_chunk])
        chunks.append(chunk)

    return chunks