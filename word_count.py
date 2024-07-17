import pymupdf, re
error_count = 0

def list_in_str(sls, ss): #배열 안의 원소가 문자열 안에 있는지 점검
    for sl in sls:
        if sl in ss:return True
    return False

def scan_qs(path,  specialQ, insertQ, fromQ, toQ): 
    global error_count
    #scannig questions(2010~), 
    #path: sat pdf path / pecialQ : 유형별 정리가 별도로 필요한 + inserQ : 지문 내에 선지가 삽입돼 있는 문제의 키워드
    #fromQ : 스캔 시작 + toQ : 스캔 끝 문제 지점

    print(f"\n\n\n**********{path}**********")
    with pymupdf.open(r"resolutions\\"+path) as doc:  # open document
        ws = "".join([page.get_text() for page in doc]) #whole sentence of document (str)

    #line 17-39:scanning index of question
    num = fromQ #question No.
    QidxLst = [] #Question Index List
    ContinueQLst = [] #Continueal Question List
    preQidx = ws.find(f"[{num}～") + len(str(num)) + 5
    titles = [] #title of question
    sentences = [] #문항 원문
    sentences_num = [] #문항 번호 정리

    while num <= toQ:
        start, end = 0, 0
        if (ws.find(f"[{num}～") != -1 and ws.find(f"[{num}～") > preQidx):
            start = num
            preQidx = ws.find(f"[{num}～") + len(str(num)) + 5
            end = int(ws[preQidx-3:preQidx-1])
            print(f"{path}) ques.{start}~{end} cont")
             
            ContinueQLst += [num, end-start]
            num += end - start      
            title = re.compile(str(end) + r"\] [^①]*?(은\?|시오\.)", flags = re.DOTALL).search(ws)

            sentences_num.append(f"{start} ~ {end}")
        elif(ws.find(f"\n{num}.") != -1 and ws.find(f"\n{num}.") > preQidx):
            print(f"{path}) ques.{num} sing")
            
            preQidx = ws.find(f"\n{num}.")

            title = re.compile(str(num) + r"\. [^①]*?(은\?|시오\.)", flags = re.DOTALL).search(ws)
            sentences_num.append(str(num))
        else:
            print(f"{path}) ques.{num} is not found.")
            QidxLst.append(-5)
            error_count += 1
               
        QidxLst += [(title.start(), title.end()+1)] + [-5 for i in range(end - start)] 
        titles += [title]*(end-start+1)

        num += 1
    QidxLst += [(0,0)]
    next = 0 #next index in questions
    
    for n in range(18, num):
        
        if (QidxLst[n-18] != -5):
            title = titles[n-18].group().replace("\n", "")[4:]
            if (n in ContinueQLst[::2]):
                next = ContinueQLst[ContinueQLst[::2].index(n)*2  + 1] + n + 1  #ContinueQLst start from 18, next start from 0 
                print(f"{n}~{next-1} is continuous questions")
                
                
            else:
                next = n+1
                

            print(f"{path})  reading {n} (~ prev. {next}).... ", end='')
            print(f"<idx : {QidxLst[n-18][1]} ~ {QidxLst[next-18][0]}-1>.... ")
            #print(title, list(set(insertQ) & set(title.split())) == [])
            if (not list_in_str(insertQ, title)): # 문제의 키워드와 예외 키워드(insert)가 켭치는지 확인
                #print(ws[QidxLst[n-18][1]:QidxLst[next-18][0]-1])
                txt = re.compile("(.*?)\①", flags = re.DOTALL).search(ws[QidxLst[n-18][1]:QidxLst[next-18][0]-1]).group()[:-2]
                #print(txt)
            else:
                if ("읽고" in title):
                    txt = re.compile(f"(.*?){n}. ", flags = re.DOTALL).search(ws[QidxLst[n-18][1]:QidxLst[next-18][0]-1]).group()[:-4]
                else:
                    txt = ws[QidxLst[n-18][1]:QidxLst[next-18][0]-1]
            txt_proceed = re.sub(r"[^a-zA-Z.? ,'xd ]+", "", txt).replace("\n ", "")
            #print(txt_proceed)
            sentences.append(re.sub("[.?]", ".\n", txt_proceed))
            #print(sentences)
                
            # if ( list(set(specialQ) & set(title.split())) != []): # 문제의 키워드와 예외 키워드(special)가 켭치는지 확인


            print("**********************")
            print('done!')
    
        
        

    with open(f"resolution_txt\{path}.txt", 'w') as f:
        for s_num, sentence in enumerate(sentences):

            f.write("\n"*3 + f"**********N.{sentences_num[s_num]}**********\n")
            f.write(sentence)


for year in range(2014, 2025):
    scan_qs(f"{year}_s.pdf", [], ['어법', '흐름', '도표', '읽고,', '문맥'], 18, 45)
print(f"{error_count} errors occurred.")