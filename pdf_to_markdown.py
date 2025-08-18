import fitz  # PyMuPDF
import markdown2


def pdf_to_markdown(pdf_path, output_md="output.md"):
    doc = fitz.open(pdf_path)

    font_sizes = set()
    all_blocks_per_page = []

    for page in doc:
        page_blocks = []

        # --- Find tables ---
        tables = page.find_tables()
        table_bboxes = []
        for t in tables:
            table_md = t.to_markdown()
            page_blocks.append(("table", t.bbox, table_md))
            table_bboxes.append(t.bbox)

        # --- Process text spans (skip table regions to avoid duplicates) ---
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
                            page_blocks.append(("span", bbox, (size, text, flags)))

        # Sort blocks by vertical position (preserve reading order)
        page_blocks.sort(key=lambda b: b[1][1])
        all_blocks_per_page.append(page_blocks)

    # --- Assign font size → Markdown heading ---
    sorted_sizes = sorted(list(font_sizes), reverse=True)
    size_to_md = {}
    if sorted_sizes:
        size_to_md[sorted_sizes[0]] = "# "   # h1
        if len(sorted_sizes) > 1:
            size_to_md[sorted_sizes[1]] = "## "  # h2
        if len(sorted_sizes) > 2:
            size_to_md[sorted_sizes[2]] = "### "  # h3
        for s in sorted_sizes[3:]:
            size_to_md[s] = ""  # paragraph

    # --- Build Markdown ---
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
                if flags == 18 or flags == 22:   # bold + italic
                    text = f"**_{text}_**"
                elif flags==16 or flags == 20:  # bold
                    text = f"**{text}**"
                elif flags==2 or flags == 6:  # italic
                    text = f"_{text}_"

                md_parts.append(f"{prefix}{text}\n")
        md_parts.append("\n---\n")  # page separator

    # --- Save Markdown ---

    return "".join(md_parts)


# Example
markdown_result = pdf_to_markdown("pdfs/javabook-71-89.pdf", "output.md")
html_result = markdown2.markdown(markdown_result,extras=["tables"])


