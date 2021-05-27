import re, string
from nltk.tokenize import word_tokenize
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# Create Sastrawi stemmer
STEMMER = StemmerFactory().create_stemmer()

# Create Stopword
with open("kamus/Stopword.txt", "r") as f:
    STOPWORDS = f.readline().split()

# Kata Positif
with open('kamus/Kata Positif.txt', 'r') as f:
    POSITIF = f.readlines()

# Kata Negatif
with open('kamus/Kata Negatif.txt', 'r') as f:
    NEGATIF = f.readlines()

# Kata positif dan negatif yang timpang tindih
for i in range(len(POSITIF)):
    if i>=len(NEGATIF):
        POSITIF[i] = POSITIF[i].strip()
    else :
        POSITIF[i] = POSITIF[i].strip()
        NEGATIF[i] = NEGATIF[i].strip()

# Preprocessor
def preprocessor(text):
    # Convert to lower case
    text = text.lower()
    # Convert www.* or https?://* to URL
    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',text)
    # Convert @username to AT_USER
    text = re.sub('@[^\s]+','ATUSER',text)
    # Remove additional white spaces
    text = re.sub('[\s]+', ' ', text)
    # Replace #word with word
    text = re.sub(r'#([^\s]+)', r'\1',text)
    # Menghapus angka dari teks
    text = re.sub(r"\d+", "", text)
    # Menghapus tanda baca
    text = text.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation)))
    return text

# Tokenizer
def tokenizer(text):
    words = word_tokenize(text)
    tokens=[]
    for w in words:
        # add tokens
        if w not in ['ATUSER','URL'] and len(w) > 3:
            w = STEMMER.stem(w)
            tokens.append(w.lower())
    return tokens

# Cleanner 
def cleaning(text):
    text= text[2:]
    text = text.replace('\\n',' ')
    return text

def analyst(string) :
    string = cleaning(string)
    string = preprocessor(string)
    string = tokenizer(string)
    
    for i in range(len(string)-1,-1,-1):
        if string[i] in STOPWORDS:
            string.pop(i)
    
    n_p = 0
    n_n = 0
    for kata in string :
        if kata in POSITIF:
            n_p += 1
        elif kata in NEGATIF:
            n_n += 1
    
    if n_p > n_n :
        return 1
    elif n_p < n_n:
        return -1
    else :
        return 0