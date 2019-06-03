import os
from flask import Flask, render_template, request, send_file
from werkzeug import secure_filename
import re
import nltk
import string
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')
from textblob.classifiers import NaiveBayesClassifier
import tika
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from sklearn.externals import joblib
import glob
import pandas as pd
import xlsxwriter
import flask_excel as excel
import time
timestr = time.strftime("%Y%m%d%H%M%S")
tika.initVM()

from tika import parser

from nltk import ngrams

app = Flask(__name__)



def get_ngrams(text, n ):
    n_grams = ngrams(word_tokenize(text), n)
    return [ ' '.join(grams) for grams in n_grams]

def create_word_features1(words, n):
    useful_words = [word for word in words if word not in stopwords.words("english")] 
    my_dict = dict([(word, True) for word in useful_words])
    return my_dict


def create_word_features(words, n):
    ngram_vocab = ngrams(words, n)
    my_dict = dict([(ng, True) for ng in ngram_vocab])
    return my_dict

NB_wal_model = open('NB_wal_model.pkl','rb')
cl = joblib.load(NB_wal_model)    


@app.route('/')
def index():
    return render_template('test.html', name='name')

@app.route('/getfile', methods=['GET','POST'])
def getfile():
    if request.method == 'POST':
        # for secure filenames. Read the documentation.
        file = request.files['myfile']
        filename = secure_filename(file.filename) 
        #return filename
        # os.path.join is used so that paths work in every operating system
        
        file.save(os.path.join("test_pdf/",filename))

        # You should use os.path.join here too.
        parsed = parser.from_file("test_pdf/"+filename)

        text = parsed["content"]

        os.remove(os.path.join('test_pdf/', filename))
        
        cachedStopWords = stopwords.words("english")
        
        #convert to lowercase
        text = text.lower()

        #remove all stopwords
        text = ' '.join([word for word in text.split() if word not in cachedStopWords])

        #remove special characters

        punctuations = '''!()“-[]{};:”'"’\,<>./?@#$%^&*_~'''

        no_punct_text = ""

        for char in text:
           if char not in punctuations:
              no_punct_text = no_punct_text + char
        text = re.sub('[ﬂﬁ]', '', no_punct_text)
        text = re.sub('maximum', '', text)

        #remove multiple whitespaces
        text = ' '.join(text.split())

        text = text.split("average life test weighted average life",1)[1]
        text = text.split()[:35]
        text = "".join([" "+i if not i.startswith("'") and i not in string.punctuation else i for i in text]).strip()
        text = ''.join([i for i in text if not i.isdigit()])
        text = re.sub(r'\b\w{1,1}\b', '', text)
        text = ' '.join(text.split())

        test = os.listdir()

        for item in test:
            if item.endswith(".xlsx"):
                os.remove(os.path.join('', item))

        wal = [cl.classify(text)]
        df = pd.DataFrame({'WAL LIFE TEST': wal, 'CATEGORY2': 'pending'})
        file_name = timestr+"-pdf-outcome.xlsx"
        writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1', startrow=1, header=False)
        workbook  = writer.book
        worksheet = writer.sheets['Sheet1']
        header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#D7E4BC',
        'border': 1})

        for col_num, value in enumerate(df.columns.values):
           worksheet.write(0, col_num + 1, value, header_format)

        writer.save() 

        return cl.classify(text)
        #return send_file(file_name, as_attachment=True)
           


    else:
        result = request.args.get['myfile']
    return result

if __name__ == '__main__':
    app.run(debug=True)


