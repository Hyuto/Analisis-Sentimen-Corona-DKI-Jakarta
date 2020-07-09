import re
import string
from nltk.tokenize import word_tokenize
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# Create Sastrawi stemmer
stemmer = StemmerFactory().create_stemmer()

# Create Stopword
f = open("Kamus/Stopword.txt", "r")
my_stop_words = f.readline()
f.close()
my_stop_words = my_stop_words.split()

# Preprocessor
def my_preprocessor(mytext):
    #Convert to lower case
    mytext = mytext.lower()
    #Convert www.* or https?://* to URL
    mytext = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',mytext)
    #Convert @username to AT_USER
    mytext = re.sub('@[^\s]+','ATUSER',mytext)
    #Remove additional white spaces
    mytext = re.sub('[\s]+', ' ', mytext)
    #Replace #word with word
    mytext = re.sub(r'#([^\s]+)', r'\1',mytext)
    #Menghapus angka dari teks
    mytext = re.sub(r"\d+", "", mytext)
    #Menghapus tanda baca
    mytext = mytext.translate(str.maketrans(string.punctuation, ' '*len(string.punctuation)))
    return mytext

# Tokenizer
def my_tokenizer(mytext):
    words = word_tokenize(mytext)
    tokens=[]
    for w in words:
        #add tokens
        if w not in ['ATUSER','URL'] and len(w) > 3:
            w = stemmer.stem(w)
            tokens.append(w.lower())
    return tokens

# Cleanner 
def cleaning(text):
    text= text[2:]
    text = text.replace('\\n',' ')
    return text

f = open('Kamus/Kata_Positif.txt', 'r')
positif = f.readlines()
f.close()

f = open('Kamus/Kata_Negatif.txt', 'r')
negatif = f.readlines()
f.close()

for i in range(len(positif)):
    if i>=len(negatif):
        positif[i] = positif[i].strip()
    else :
        positif[i] = positif[i].strip()
        negatif[i] = negatif[i].strip()

def analis(string) :
    string = cleaning(string)
    string = my_preprocessor(string)
    string = my_tokenizer(string)
    
    for i in range(len(string)-1,-1,-1):
        if string[i] in my_stop_words:
            del string[i]
    
    n_p = 0
    n_n = 0
    for kata in string :
        if kata in positif:
            n_p += 1
        elif kata in negatif:
            n_n += 1
    
    if n_p > n_n :
        return 1
    elif n_p < n_n:
        return -1
    else :
        return 0