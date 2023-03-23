from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponse as Response
# for Model
from . import shared as model
import nltk

## nltk settings
nltk.download('punkt')

url = "A:\\4 second term\\NLP\Assignments\\Assignment 1\\trigramemodel\\Dataset\\data.txt"


def ReadData():  # Read From File
    with open(url, "r", encoding="utf8") as f:
        data = f.read()
    return data


def preprocessing(data):
    tokens = []
    finalTokens = []

    # preprocessing Data
    sentences = data.split('\n')
    sentences = [s.replace('"', ' ') for s in sentences]
    sentences = [s.replace('*', ' ') for s in sentences]
    sentences = [s.replace('%', ' ') for s in sentences]
    sentences = [s.replace('-', ' ') for s in sentences]
    sentences = [s.replace('+', ' ') for s in sentences]
    sentences = [s.replace(':', ' ') for s in sentences]
    sentences = [s.replace('.', ' ') for s in sentences]
    sentences = [s.replace('?', ' ') for s in sentences]
    sentences = [s.replace('[', ' ') for s in sentences]
    sentences = [s.replace('|', ' ') for s in sentences]
    sentences = [s.replace('--', ' ') for s in sentences]
    sentences = [s.replace('-', ' ') for s in sentences]
    sentences = [s.replace('‘', ' ') for s in sentences]
    sentences = [s.replace('’', ' ') for s in sentences]
    sentences = [s.replace('!', ' ') for s in sentences]
    sentences = [s.replace('/', ' ') for s in sentences]
    sentences = [s.replace('\\', ' ') for s in sentences]
    sentences = [s.replace(']', ' ') for s in sentences]
    sentences = [s.replace('(', ' ') for s in sentences]
    sentences = [s.replace(')', ' ') for s in sentences]
    sentences = [s.replace('&', ' ') for s in sentences]
    sentences = [s.strip() for s in sentences]
    sentences = [s for s in sentences if len(s) > 0]

    for sentence in sentences:
        sentence = sentence.lower()
        token = nltk.word_tokenize(sentence)
        tokens.append(token)  # [[],[],[]]

    for words in tokens:
        for word in words:
            finalTokens.append(word)
    return finalTokens  # [,,,,,]


def ngrame(data, n):
    ngrame = []
    for i in range(len(data)):
        D = data[i: i + n]
        size = len(data[i: i + n])
        if size == n:
            ngrame.append(D)
    return ngrame


def count_the_words(data):
    frequency = {}
    for t in data:
        if tuple(t) in frequency:
            frequency[tuple(t)] += 1
        else:
            frequency[tuple(t)] = 1
    return frequency


def probability(unigram, bigram, trigram):
    model = []
    for trigram_value, trigram_count in trigram.items():
        prob = 1

        prob *= unigram[(trigram_value[0],)]
        prob *= bigram[(trigram_value[0], trigram_value[1])] / unigram[(trigram_value[0],)]
        prob *= trigram_count / bigram[(trigram_value[0], trigram_value[1])]

        model.append([trigram_value, prob / len(trigram)])
    return model


def suggestion(request, input):
    suggest = []
    input = input.lower()
    for p, v in model.mymodel:
        if p == '_':
            continue
        for i in range(len(p)):
            if not (p[i].startswith(input)):
                continue
            arr = []
            if i == 0:
                arr.append(p[0])
                arr.append(p[1])
                arr.append(p[2])
            elif i == 1:
                arr.append(p[1])
                arr.append(p[2])
            if len(arr):
                suggest.append((arr, v))
    return Response(list(filter(suggest)))


def filter(suggest):
    filterd = []
    temp = []
    final_suggest = []
    for i in suggest:
        if temp.count(i[0]) == 0:
            filterd.append(i)
            temp.append(i[0])
        else:
            tup = [item for item in filterd if i[0] in item]
            if i[1] > tup[0][1]:
                index = filterd.index(tup[0])
                filterd[index] = i
    filterd.sort(key=lambda a: a[1], reverse=True)
    for i in filterd:
        arr = []
        for j in i[0]:
            arr.append(j)
        final_suggest.append(arr)
    return final_suggest


def createModel():
    data = ReadData()
    tokens = preprocessing(data)

    unigram = ngrame(tokens, 1)
    bigram = ngrame(tokens, 2)
    trigram = ngrame(tokens, 3)

    unigram = count_the_words(unigram)
    bigram = count_the_words(bigram)
    trigram = count_the_words(trigram)

    return probability(unigram, bigram, trigram)


def build_model(request):
    model.mymodel = createModel()
    return redirect("search")


def search(request):
    return render(request, "search.html", {"model": model.mymodel})
