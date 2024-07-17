
import sys, pathlib, pymupdf
fname = r"resolutions\2014_s.pdf"
with pymupdf.open(fname) as doc:  # open document
    text = "".join([page.get_text() for page in doc])

with open("log.txt", 'w', encoding='utf-8') as f:
    f.write(text)