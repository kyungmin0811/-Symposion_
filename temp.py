
import sys, pathlib, pymupdf
fname = r"resolutions\2024_s.pdf"
with pymupdf.open(fname) as doc:  # open document
    text = "".join([page.get_text() for page in doc])

with open("log.txt", 'w') as f:
    f.write(text)