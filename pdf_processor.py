import fitz  # PyMuPDF
import markdown2
from pathlib import Path


def pdf_to_markdown(file):
    doc = fitz.open(stream=file, filetype="pdf")
    print("No of pages:",len(doc))
    font_sizes = set()
    all_blocks_per_page = []
    font_size_counts = {}

    for page in doc:
        page_blocks = []

        tables = page.find_tables()
        table_bboxes = []
        for t in tables:
            table_md = t.to_markdown()
            page_blocks.append(("table", t.bbox, table_md))
            table_bboxes.append(t.bbox)

        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        bbox = span["bbox"]
                        # Skip if inside a detected table
                        if any(
                            bbox[0] >= tb[0] and bbox[1] >= tb[1] and
                            bbox[2] <= tb[2] and bbox[3] <= tb[3]
                            for tb in table_bboxes
                        ):
                            continue

                        size = round(span["size"], 1)
                        text = span["text"].strip()
                        flags = span["flags"]
                        if text:
                            font_sizes.add(size)
                            words_in_span = len(text.split())
                            if size in font_size_counts:
                                font_size_counts[size]+=words_in_span
                            else:
                                font_size_counts[size] = words_in_span
                            page_blocks.append(("span", bbox, (size, text, flags)))


        page_blocks.sort(key=lambda b: b[1][1])
        all_blocks_per_page.append(page_blocks)

    para_font_count = max(font_size_counts.values())
    para_font = [key for key,value in font_size_counts.items() if value == para_font_count][0]
    sorted_sizes = sorted(list(font_sizes), reverse=True)
    para_font_index = sorted_sizes.index(para_font)
    size_to_md = {}
    if sorted_sizes:
        size_to_md[para_font] = ""                                  # paragraph
        for s in sorted_sizes[para_font_index:]:
            size_to_md[s] = ""                                      # paragraph
        if para_font_index > 3:
            size_to_md[sorted_sizes[para_font_index-4]] = "# "      # h3
            size_to_md[sorted_sizes[para_font_index - 3]] = "## "   # h2
            size_to_md[sorted_sizes[para_font_index - 2]] = "### "  # h3
            size_to_md[sorted_sizes[para_font_index - 1]] = "#### " # h4
        if para_font_index > 2:
            size_to_md[sorted_sizes[para_font_index-3]] = "# "      # h3
            size_to_md[sorted_sizes[para_font_index - 2]] = "## "   # h2
            size_to_md[sorted_sizes[para_font_index - 1]] = "### "  # h3
        elif para_font_index > 1:
            size_to_md[sorted_sizes[para_font_index-2]] = "# "      # h1
            size_to_md[sorted_sizes[para_font_index - 3]] = "## "   # h2
        elif para_font_index > 0:
            size_to_md[sorted_sizes[para_font_index - 1]] = "# "    # h1
        for s in sorted_sizes[:para_font_index-4]:
            size_to_md[s] = "-rm-"  # outliers

    md_parts = []
    for page_num, blocks in enumerate(all_blocks_per_page, start=1):
        md_parts.append(f"\n<!-- Page {page_num} -->\n")
        for btype, bbox, content in blocks:
            if btype == "table":
                md_parts.append(content + "\n")
            else:  # span
                size, text, flags = content
                prefix = size_to_md.get(size, "")

                # Apply bold/italic
                # if flags == 18 or flags == 22:   # bold + italic
                #     text = f"**_{text}_**"
                # elif flags==16 or flags == 20:  # bold
                #     text = f"**{text}**"
                # elif flags==2 or flags == 6:  # italic
                #     text = f"_{text}_"
                if prefix in ['# ','## ','### ']:
                    md_parts.append(f"\n{prefix}{text}\n")
                elif text[0] == '|':
                    md_parts.append(f"\n{prefix}{text}")
                else:
                    md_parts.append(f"{prefix}{text} ")
        md_parts.append("\n---\n")  # page separator



    return "".join(md_parts)


def pdf_processor(file):
    markdown_result = pdf_to_markdown(file)
    with open("parsed.md","w",encoding='utf-8') as f:
        f.write(markdown_result)

    # html_result = markdown2.markdown(markdown_result,extras=["tables"])
    # with open("parsed.html","w",encoding='utf-8') as f:
    #     f.write(html_result)

    print("PDF Processed successfully")
    return markdown_result


