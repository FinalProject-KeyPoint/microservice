import json
import bs4
import urllib.request
import nltk
import numpy as np
from flask import jsonify, request, Flask
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from sklearn.feature_extraction.text import CountVectorizer

# setup web server
app = Flask(__name__)


@app.route('/', methods=['POST'])
def text_summarizer():
    '''
    fungsi ini menerima request body
    berupa "isi_artikel" yaitu array berisi kalimat
    hasil ekstrasi artikel dari client
    '''

    # ambil body dari request
    body = request.get_data()

    # ubah string menjadi dict python
    data = json.loads(body)

    article_content = data['isi_artikel']

    clean_data = []

    def preprocessing(text):
        stemmer = StemmerFactory().create_stemmer()
        stopwords = StopWordRemoverFactory().get_stop_words()
        text = text.lower()
        text = stemmer.stem(text)

        result = []
        for word in text.split(' '):
            if (word not in stopwords):
                result.append(word)

        return ' '.join(result)

    for sent in article_content:
        clean_data.append(preprocessing(sent))

    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(clean_data)

    res = np.sum(vectors.toarray(), axis=0)
    vocab = vectorizer.vocabulary_
    freq_table = dict()

    for word, ix in vocab.items():
        freq_table[word] = res[ix]

    N = len(freq_table.values())

    for word in freq_table:
        freq_table[word] /= N

    sent_weight = dict()

    for ix, sent in enumerate(clean_data):
        list_word = word_tokenize(sent)
        g_sent = 0

        for word in list_word:
            if word in freq_table:
                g_sent += freq_table[word]

        sent_weight[ix] = g_sent / len(list_word)

    top5 = sorted(sent_weight.items(), key=lambda x: x[1], reverse=True)[:5]

    result = []
    for ix, _ in top5:
        result.append(article_content[ix])

    # buat proteksi, in case client requestnya
    # di luar POST
    if request.method == 'POST':
        return jsonify(result)


@app.route('/test', methods=['GET'])
def text_summarizer_demo():
    '''
    fungsi ini hanya buat demo
    url udah ditentukan jadi user tinggal
    fetch hasilnya saja
    '''

    # Fetch the content from the URL
    url = 'https://nasional.kompas.com/read/2020/02/21/13444071/mahfud-ungkap-2-ancaman-kedaulatan-indonesia-berdasarkan-analisis-prabowo'
    fetched_data = urllib.request.urlopen(url)

    article_read = fetched_data.read()

    # Parsing the URL content and storing in a variable
    soup = bs4.BeautifulSoup(article_read, 'html.parser')

    article_content = []

    for element in soup.find_all('p'):
        article_content.append(element.text)

    article_content = ' '.join(article_content)
    article_content = sent_tokenize(article_content)

    clean_data = []

    def preprocessing(text):
        stemmer = StemmerFactory().create_stemmer()
        stopwords = StopWordRemoverFactory().get_stop_words()
        text = text.lower()
        text = stemmer.stem(text)

        result = []
        for word in text.split(' '):
            if (word not in stopwords):
                result.append(word)

        return ' '.join(result)

    for sent in article_content:
        clean_data.append(preprocessing(sent))

    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(clean_data)

    res = np.sum(vectors.toarray(), axis=0)
    vocab = vectorizer.vocabulary_
    freq_table = dict()

    for word, ix in vocab.items():
        freq_table[word] = res[ix]

    N = len(freq_table.values())

    for word in freq_table:
        freq_table[word] /= N

    sent_weight = dict()

    for ix, sent in enumerate(clean_data):

        list_word = word_tokenize(sent)
        g_sent = 0

        for word in list_word:
            if word in freq_table:
                g_sent += freq_table[word]

        sent_weight[ix] = g_sent / len(list_word)

    top5 = sorted(sent_weight.items(), key=lambda x: x[1], reverse=True)[:5]

    result = []
    for ix, _ in top5:
        result.append(article_content[ix])

    return jsonify({
        "url": url,
        "result": result
    })
