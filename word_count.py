from PyPDF2 import PdfReader as reader
path = "/workspaces/-Symposion_/resolutions"

def extract_pdf(name):
    with open(f"{path}/{name}.pdf", "rb") as file:
        read = reader(file)
        num_pages = len(read.pages)
        for page in (read.pages):
            text = page.extract_text()
            print(text.replace("\n", ""))
        title = read.info["Title"]
        author = read.info["Author"]
        print(num_pages, title, author)

extract_pdf("2025_6")