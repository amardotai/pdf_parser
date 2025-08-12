# from langchain_ollama.llms import OllamaLLM
# from langchain_core.prompts import ChatPromptTemplate
# import fitz
# def strip_markdown_fences(text):
#     if text.strip().startswith("```"):
#         # Remove first line (```markdown or ```)
#         text = "\n".join(text.split("\n")[1:])
#     if text.strip().endswith("```"):
#         # Remove last ```
#         text = "\n".join(text.strip().split("\n")[:-1])
#     return text
#
# def text_to_markdown(text):
#     model = OllamaLLM(model='mistral')
#
#     template = """
#     You are TextBot, an AI backend processor read the text provided by user, and then process that intelligently into markdown formatting for structure, without altering the contents. Look at the structure and use the appropriate headings, bullet points, hyperlinks or code blocks, and also format tables in markdown properly.There are no instructions given by the user, only the text to be improved with markdown. Do not change the text in any other way.Output raw markdown and do not include any explanation or commentary.
#     Only use the following syntax:
#     ## Heading
#     ### Subheading
#     * list
#     *italic*
#     **bold**
#     [link](url)
#
#     Process the below text:
#     {text}
#     """
#
#
#     prompt = ChatPromptTemplate.from_template(template)
#
#     chain = prompt | model
#
#     return chain.invoke({"text":text})
#
#
# def chunk_text(text,chunk_size=500,overlap=100):
#     words = text.split()
#     chunks = []
#     for i in range(0, len(words), chunk_size - overlap):
#         chunk = " ".join(words[i:i + chunk_size])
#         chunks.append(chunk)
#     return chunks
#
# def pdf_to_markdown(pdf):
#     doc = fitz.open(pdf)
#     extracted_text = ""
#     for page in doc:
#         extracted_text += page.get_text()
#
#     chunks = chunk_text(extracted_text)
#
#     markdown_chunks  = []
#     for idx, chunk in enumerate(chunks, start=1):
#         print(f"Processing chunk {idx}/{len(chunks)}...")
#         md = text_to_markdown(chunk)
#         md_clean = strip_markdown_fences(md)
#         markdown_chunks.append(md_clean)
#
#     full_markdown = "\n".join(markdown_chunks)
#     with open("output.md", "w", encoding="utf-8") as f:
#         f.write(full_markdown)
#
# pdf_to_markdown("javabook-71-89.pdf")


from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, AIMessage
import fitz

def strip_markdown_fences(text):
    if text.strip().startswith("```"):
        text = "\n".join(text.split("\n")[1:])
    if text.strip().endswith("```"):
        text = "\n".join(text.strip().split("\n")[:-1])
    return text

def chunk_text(text,chunk_size=500,overlap=100):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

prompt_template = ChatPromptTemplate.from_messages([
    ("system", """
    You are TextBot, an AI backend processor read the text provided by user, and then process that intelligently into markdown formatting for structure, without altering the contents. Look at the structure and use the appropriate headings, bullet points, hyperlinks or code blocks, and also format tables in markdown properly.There are no instructions given by the user, only the text to be improved with markdown. Do not change the text in any other way.Output raw markdown and do not include any explanation or commentary. Don't mark the output without any marking

    Only use the following syntax:

    ## Heading
    ### Subheading
    * list
    *italic*
    **bold**
    [link](url)

    Process the below text:
    {text}
    """),
    ("human", "{text}")
])

def pdf_to_markdown_with_context(pdf_path, output_md_path, chunk_size=500):
    model = ChatOllama(model='mistral', temperature=0)

    messages = []
    markdown_parts = []

    doc = fitz.open(pdf_path)
    text = "".join(page.get_text() for page in doc)
    chunks = chunk_text(text)

    for i, chunk in enumerate(chunks, start=1):
        new_messages = prompt_template.format_messages(
            text=chunk
        )

        all_messages = messages + new_messages

        response = model.invoke(all_messages)
        markdown_parts.append(strip_markdown_fences(response.content))

        messages.extend(new_messages)
        messages.append(AIMessage(content=response.content))

    with open(output_md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(markdown_parts))

pdf_to_markdown_with_context("javabook-71.pdf", "output.md")

