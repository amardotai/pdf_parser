import fitz

def handle_urls(line:str):
    words = line.split(" ")
    for i in range(len(words)):
        if 'http://' in words[i] or 'https://' in words[i]:
            words[i] = '[link]('+words[i]+')'

    return ' '.join(words)

def text_to_markdown(text:str):
    lines = text.split('/n')
    for i in range(len(lines)):
        if lines[i][0] == '\u2022':
            lines[i] = '* ' + lines[i][1:]
        if 'http://' in lines[i] or 'https://' in lines[0]:
            lines[i] = handle_urls(lines[i])

    return '\n'.join(lines)


def extract_text_and_tables_in_order(page):
    # Extract text blocks and table blocks with their vertical coordinates
    blocks = page.get_text("blocks")  # Returns list of (x0, y0, x1, y1, "text", block_no, block_type)
    tables = page.find_tables()

    # Convert tables to their bounding boxes and Markdown text
    table_blocks = []
    for table in tables:
        rect = table.bbox  # bounding box of the table
        md_table = table.to_markdown()
        table_blocks.append((rect[1], rect[3], md_table))
    # Prepare list to merge: (y0, content, type)
    elements = []

    # Add text blocks: type='text'
    for b in blocks:
        x0, y0, x1, y1, text, block_no, block_type = b
        if text.strip():
            flag = True
            for ty0,ty1,t in table_blocks:
                if ty0 < y0 and ty1 > y1:
                    flag = False
                    break
            if flag:
                md_text = text_to_markdown(text)
                elements.append((y0, y1, md_text.strip(), 'text'))
    # Add tables: type='table'
    for (y0, y1, md_table) in table_blocks:
        elements.append((y0, y1, md_table, 'table'))

    # Sort elements by vertical position (y0)
    elements.sort(key=lambda e: e[0])

    # Compose markdown combining text and tables in order
    markdown_parts = []
    for _, _, content, typ in elements:
        if typ == 'text':
            markdown_parts.append(content + "\n")  # separate paragraphs by newline
        else:  # table
            markdown_parts.append(content + "\n")

    return "\n".join(markdown_parts)

def pdf_to_markdown_with_preserved_table_location(pdf_path, md_path):
    doc = fitz.open(pdf_path)
    all_markdown = ""

    for page in doc:
        page_md = extract_text_and_tables_in_order(page)
        all_markdown += page_md + "\n\n---\n\n"  # page separator

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(all_markdown)

# Usage example
pdf_to_markdown_with_preserved_table_location("javabook-71-89.pdf","output.md")