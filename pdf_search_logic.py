import fitz # PyMuPDF

def search_content(query, file_path="data/RTSA.pdf"):
    doc = fitz.open(file_path)
    results = []

    for page_num, page in enumerate(doc, start=1):
        text = page.get_text()
        if query.lower() in text.lower():
            lines = text.split('\n')

            # Find line where query occurs
            matched_line = ""
            matched = ""

            for i, line in enumerate(lines):
                if query.lower() in line.lower():
                    prev_line = lines[i - 1].strip() if i > 0 else ""
                    next_line = lines[i + 1].strip() if i < len(lines) - 1 else ""
                    matched = line.strip()
                    matched_line = f"{prev_line} {matched} {next_line}"

            results.append({
                #"page": page_num,
                "match": matched_line
            })

    doc.close()

    if results:
        list_results = [
            f" the content is: \"{r['match']}\""
            for r in results]
        return "\n".join(list_results)
    else:
        return "No relevant information found in the document."

#On page {r['page']},