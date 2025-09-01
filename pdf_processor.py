import fitz  # PyMuPDF
import pdfplumber
import pandas as pd
import uuid


def table_to_markdown(file):
    all_tables = []
    with pdfplumber.open(file) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            table_bbox = page.find_tables()
            tables = page.extract_tables()
            for bbox, table in zip(table_bbox, tables):
                df = pd.DataFrame(table[1:], columns=table[0])
                df = df.loc[:, [c for c in df.columns if c not in [None, ""]]]
                markdown_table = df.to_markdown(index=False)
                all_tables.append(("table",bbox.bbox,"\n"+markdown_table+"\n",page_number))

    return all_tables

def pdf_to_markdown(file):
    doc = fitz.open(stream=file, filetype="pdf")
    print("No of pages:",len(doc))
    font_sizes = set()
    all_blocks_per_page = []
    font_size_counts = {}
    all_tables = table_to_markdown(file)
    line_height_average = 0
    lines = 0
    for page_number,page in enumerate(doc,start=1):
        page_blocks = []
        table_bboxes = []
        tables_in_page = page.find_tables()
        if tables_in_page:
            for table in tables_in_page:
                df = table.to_pandas()
                table_md = df.to_markdown()
                table_bboxes.append(table.bbox)
                page_blocks.append(("table",table.bbox,"\n"+table_md+"\n"))
        # for table in all_tables:
        #     table_block = table[:3]
        #     table_page = table[3]
        #     if table_page > page_number:
        #         break
        #     if table_page == page_number:
        #         page_blocks.append(table_block)
        #         table_bboxes.append(table[1])

        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    line_height_average+=line["bbox"][3]-line["bbox"][1]
                    lines+=1
                    for span in line["spans"]:
                        bbox = span["bbox"]
                        # Skip if inside a detected table
                        inside_table = False
                        for tb in table_bboxes:
                            if bbox[3] > tb[1] and bbox[1] < tb[3]:
                                inside_table = True
                                break
                        # if any(
                        #         bbox[0] >= tb[0] and bbox[1] >= tb[1] and
                        #         bbox[2] <= tb[2] and bbox[3] <= tb[3]
                        #         for tb in table_bboxes
                        # ):
                        #     continue
                        if inside_table:
                            continue
                        size = round(span["size"], 1)
                        text = span["text"].strip()
                        flags = span["flags"]
                        if text:
                            font_sizes.add(size)
                            words_in_span = len(text.split())
                            if size in font_size_counts:
                                font_size_counts[size] += words_in_span
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
            size_to_md[sorted_sizes[para_font_index-4]] = "# "      # h1
            size_to_md[sorted_sizes[para_font_index - 3]] = "## "   # h2
            size_to_md[sorted_sizes[para_font_index - 2]] = "### "  # h3
            size_to_md[sorted_sizes[para_font_index - 1]] = "#### " # h4
        elif para_font_index > 2:
            size_to_md[sorted_sizes[para_font_index-3]] = "# "      # h1
            size_to_md[sorted_sizes[para_font_index - 2]] = "## "   # h2
            size_to_md[sorted_sizes[para_font_index - 1]] = "### "  # h3
        elif para_font_index > 1:
            size_to_md[sorted_sizes[para_font_index-2]] = "# "      # h1
            size_to_md[sorted_sizes[para_font_index - 3]] = "## "   # h2
        elif para_font_index > 0:
            size_to_md[sorted_sizes[para_font_index - 1]] = "# "    # h1
        for s in sorted_sizes[:para_font_index-4]:
            size_to_md[s] = "# "  # outliers

    md_parts = []
    for page_num, blocks in enumerate(all_blocks_per_page, start=1):
        for btype, bbox, content in blocks:
            if btype == "table":
                md_parts.append({"content":content + "\n","type":"table","bbox":bbox,"id":str(uuid.uuid4())})
            else:
                size, text, flag = content
                prefix = size_to_md.get(size, "")

                if prefix in ['# ','## ','### ','#### ']:
                    md_parts.append({"content":f"\n{prefix}{text}\n","type":"header","bbox":bbox,"id":str(uuid.uuid4())})
                else:
                    md_parts.append({"content":f"{prefix}{text}","type":"para","bbox":bbox,"id":str(uuid.uuid4())})
        # md_parts.append("\n---\n")  # page separator
    line_height_average = line_height_average/lines
    tolerance = line_height_average*2
    print(tolerance)
    for index,part in enumerate(md_parts):
        content,part_type,bbox,part_id = part.values()

        if part_type == "table":
            if index in range(1,len(md_parts)-1):
                above = md_parts[index-1]
                below = md_parts[index+1]
                if bbox[1]-above["bbox"][3] <= tolerance:
                    above["type"] = "table-caption"
                    above["id"] = part_id
                    print(above["bbox"][1] - md_parts[index-2]["bbox"][1])

                    if (above["bbox"][1] - md_parts[index-2]["bbox"][1]) < line_height_average/2:
                        above["content"] = (above["content"] + md_parts[index-2]["content"].replace("\n"," "))

                if below["bbox"][1]-bbox[3] <= tolerance:
                    below["type"] = "table-caption"
                    below["id"] = part_id
                    if (below["bbox"][1] - md_parts[index+2]["bbox"][1]) < line_height_average/2:
                        below["content"] = (below["content"] + md_parts[index+2]["content"].replace("\n"," "))

    return md_parts


def pdf_processor(file):
    markdown_result= pdf_to_markdown(file)
    with open("parsed.md","w",encoding='utf-8') as f:
        for part in markdown_result:
            f.write(part["content"])

    print("PDF Processed successfully")
    return markdown_result


