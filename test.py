import nltk
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist

# 예시 텍스트
text = "This is a simple example. Tokenize this sentence and count the tokens."

# NLTK의 word_tokenize를 사용하여 텍스트를 토큰화
tokens = word_tokenize(text)

# FreqDist를 사용하여 토큰의 빈도를 체크
fdist = FreqDist(tokens)

# 토큰의 빈도수를 기준으로 정렬된 리스트 생성
sorted_tokens = sorted(fdist.items(), key=lambda item: item[1], reverse=True)

# 정렬된 토큰 리스트 출력
for a in sorted_tokens:
    print(a)
