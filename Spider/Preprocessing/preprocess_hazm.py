from hazm import *
import re
import pandas
from parsivar import FindStems,SpellCheck


normalizer=Normalizer()
stemmer=Stemmer()
lemmatizer=Lemmatizer()

def Normalizer(text):

    # normalizer = Normalizer()
    normalized = normalizer.normalize(text)

    return normalized


def SentenceSplitter_Tokenizer(text):

    Tokens=list(word_tokenize(text))

    return Tokens

def Stemmer(token):
    my_stemmer = FindStems()
    stemming=[]
    for word in token:
        stem = my_stemmer.convert_to_stem(word)
        # print(stem)
        if "&" not in stem and stem.strip() != "":
            stemming.append(stem)

    return stemming

def RemoveStopwords_Punc(token):

    with open('stopwords') as f:
        sw = [re.sub(r"[\u200c-\u200f]","",line.rstrip().replace(" ","")) for line in f]
    # print(sw)

    punctuation = '!"#$%&\'()*+–,-./:;<=>?@[\\]^_`{|}~،؟«؛'
    result=[]
    for word in token:
        for s in punctuation:
            if s in word:
                word=word.replace(s,"")
            # print(word)
        if re.sub(r"[\u200c-\u200f]","",word.replace(" ","")) in sw:
            continue

        result.append(word)

    # print(result)
    return result

def EmojiRemoving(text):

    emoj = re.compile("["
                      u"\U0001F600-\U0001F64F"  # emoticons
                      u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                      u"\U0001F680-\U0001F6FF"  # transport & map symbols
                      u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                      u"\U00002500-\U00002BEF"  # chinese char
                      u"\U00002702-\U000027B0"
                      u"\U00002702-\U000027B0"
                      u"\U000024C2-\U0001F251"
                      u"\U0001f926-\U0001f937"
                      u"\U00010000-\U0010ffff"
                      u"\u2640-\u2642"
                      u"\u2600-\u2B55"
                      u"\u200d"
                      u"\u23cf"
                      u"\u23e9"
                      u"\u231a"
                      u"\ufe0f"  # dingbats
                      u"\u3030"
                      "]+", re.UNICODE)
    text= re.sub(emoj, '', text)

    return text

if __name__ == '__main__':
    path="/home/myubuntu/PycharmProjects/AIcampus/Spider/dataset.csv"
    data = pandas.read_csv(path)
    myspell_checker = SpellCheck()
    for i in range(len(data)):
        print("Record "+str(i)+" is processed.")
        text=data.loc[i,"body"]
        # print(text)
        # remove half-space
        # print(text)
        text=EmojiRemoving(text)
        text=myspell_checker.spell_corrector(text)
        text = text.replace("\u200c", " ")
        normalized = Normalizer(text)
        # print("norm",normalized)
        split = SentenceSplitter_Tokenizer(normalized)
        # print(split)
        tokens = RemoveStopwords_Punc(split)
        # print("tokens:",tokens)
        stemming = Stemmer(tokens)
        # print("stemm", stemming)
        data.loc[i, "body"]=str(stemming)

    data.to_csv("preprocessed.csv", index=False)







