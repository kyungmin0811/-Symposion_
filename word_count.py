import pymupdf, re
error_count = 0



def scan_qs(path, critical, nq): 
    global error_count
    #scannig questions(2010~), 
    #path: sat pdf path / critical : ex. "[41~43]___.~" point. / nq : number of questions

    print(f"\n\n\n**********{path}**********")
    with pymupdf.open(r"resolutions\\"+path) as doc:  # open document
        ws = "".join([page.get_text() for page in doc]) #whole sentence of document (str)

    #line 17-39:scanning index of question
    num = 18 #question No.
    QidxLst = [] #Question Index List
    ContinueQLst = [] #Continueal Question List
    preQidx = ws.find(f"[{num}～") + len(str(num)) + 5
    titles = [] #title of question
    while num <= nq:
        if (ws.find(f"[{num}～") != -1 and ws.find(f"[{num}～") > preQidx):
            start = num
            preQidx = ws.find(f"[{num}～") + len(str(num)) + 5
            end = int(ws[preQidx-3:preQidx-1])
            print(f"{path}) ques.{start}~{end} cont")
            QidxLst += [ws.find(f"[{num}～")] + [-5 for i in range(end - start)]
            ContinueQLst += [num, end-start]
            num += end - start     
        
            title = re.compile(str(end) + r"\] .*?(은\?|시오\.)", flags = re.DOTALL).search(ws)
        elif(ws.find(f"\n{num}.") != -1 and ws.find(f"\n{num}.") > preQidx):
            print(f"{path}) ques.{num} sing")
            QidxLst.append(ws.find(f"\n{num}."))
            preQidx = ws.find(f"\n{num}.")

            title = re.compile(str(num) + r"\. .*?(은\?|시오\.)", flags = re.DOTALL).search(ws)
        else:
            print(f"{path}) ques.{num} is not found.")
            QidxLst.append(-10)
            error_count += 1
        
        
        
        num += 1
    QidxLst.append(0)
    next = 0 #next index in questions
    sentences = []
    for n in range(18, num):
        if (QidxLst[n-18] != -5):
            if (n in ContinueQLst[::2]):
                next = ContinueQLst[ContinueQLst[::2].index(n)*2  + 1] + n + 1  #ContinueQLst start from 18, next start from 0 
                print(f"{n}~{next-1} is continuous questions")
                
                
            else:
                next = n+1
                

            print(f"reading {n} (~ prev. {next}).... ", end='')
            print(f"<idx : {QidxLst[n-18]} ~ {QidxLst[next-18]}-1>.... [", end='')
            
            
            print(titles[n-18], end="")
            txt = ws[QidxLst[n-18]:QidxLst[next-18]-1]
            eng_str = re.sub(r"[^a-zA-Z.? ,'xd ]+", "", txt) # remain only Eng
            sentences.append(re.sub("[.?]", ".\n", eng_str))
            titles += [title for i in range(next - n)]
            print("]")
            print('done!')
    
    with open(f"resolution_txt\{path}.txt", 'w') as f:
        for s_num, sentence in enumerate(sentences):
            f.write("\n"*3 + f"**********N.{s_num+18}**********\n")
            f.write(sentence)


for year in range(2014, 2025):
    scan_qs(f"{year}_s.pdf", 41, 45)
print(f"{error_count} errors occurred.")