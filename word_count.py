import sys, pathlib, pymupdf
fname = r"resolutions\2025_6.pdf"
error_count = 0



def scan_qs(path, critical, nq): 
    global error_count
    #scannig questions(2010~), 
    #path: sat pdf path / critical : ex. "[41~43]___.~" point. / nq : number of questions

    print(f"\n\n\n**********{path}**********")
    with pymupdf.open(fname) as doc:  # open document
        ws = "".join([page.get_text() for page in doc]) #whole sentence of document (str)

    #line 17-39:scanning index of question
    num = 18 #question No.
    QidxLst = [] #Question Index List
    ContinueQLst = [] #Continueal Question List
    while num <= nq:
        if (ws.find(f"[{num}～") != -1 and ws.find(f"[{num}～") > preQidx and num >= critical):
            start = num
            preQidx = ws.find(f"[{num}～") + len(str(num)) + 5
            end = int(ws[preQidx-3:preQidx-1])
            print(f"{path}) ques.{start}~{end} cont")
            QidxLst += [ws.find(f"[{num}～") for i in range(end - start + 1)]
            ContinueQLst += [i for i in range(start, end)]
            num += end - start 
            
        elif(ws.find(f"\n{num}.") != -1 and ws.find(f"[{num}～") > preQidx):
            print(f"{path}) ques.{num} sing")
            QidxLst.append(ws.find(f"\n{num}."))
        else:
            print(f"{path}) ques.{num} is not found.")
            QidxLst.append(-10)
            error_count += 1
        num += 1
    
    #extrect sentence from questions
    num = 18
    ignore = False # continue situation
    while num <= nq:

        if (not ignore):
            index = num-18 
            if (num)
            sentence = ws[QidxLst[index] : QidxLst[index+1]-1]
        

        
        if (num in ContinueQLst):
            ignore = True
        else:
            ignore = False

        num += 1
        

for year in range(2014, 2025):
    scan_qs(f"{year}_s.pdf", 41, 45)
print(f"{error_count} errors occurred.")