import fitz
import pdfplumber
import pandas as pd

def pdf_to_markdown(file):
    pdf = pdfplumber.open(file)
    print("No. of pages = ",len(pdf))
    font_sizes = set()
    all_blocks_per_page = []
    font_size_counts = {}

    for page in pdf:
        page_blocks = []



        bboxes = page.find_tables()
        tables = page.extract_tables()
        table_bboxes = []
        for table,bbox in zip(tables,bboxes):
            df = pd.DataFrame(table[1:], columns=table[0])
            markdown_table = df.to_markdown(index=False)
            table_bboxes.append(bbox.bbox)
            page_blocks.append(("table",bbox.bbox,"\n"+markdown_table))

