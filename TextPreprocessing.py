from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from nltk.tokenize import word_tokenize
import string
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
def textprocessing(df):
    factory_wordremoval = StopWordRemoverFactory()
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    stopword = factory_wordremoval.create_stop_word_remover()
    kalimat = df
    kalimat = kalimat.translate(str.maketrans('','',string.punctuation)).lower()
    stop = stopword.remove(kalimat)
    # hasil = stemmer.stem(stop)
    return kalimat
# stopwords = factory.get_stop_words()
# print(stopwords)