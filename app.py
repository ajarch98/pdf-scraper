import os
from flask import Flask, render_template, request, send_file, jsonify
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

def point2(text):
   if  re.search("redemption purchase a final redemption", text):

    text = text.split("redemption purchase a final redemption",1)[1]
    
    text = text.split("optional redemption",1)[1]

    text = text.split()[:70]

    text = "".join([" "+i if not i.startswith("'") and i not in string.punctuation else i for i in text]).strip()
    
    #print(text)
    
    if  re.search("business day | call date", text):
        return 'Business Day'
    elif re.search("payment date", text):
        return 'Payment Date'
    else:
        return 'Not Found'
        
   elif re.search("redemption purchase final redemption save", text):

    text = text.split("redemption purchase final redemption save",1)[1]
    
    text = text.split("optional redemption",1)[1]

    text = text.split()[:70]

    text = "".join([" "+i if not i.startswith("'") and i not in string.punctuation else i for i in text]).strip()
    
    #print(text)
    
    if  re.search("business day | call date", text):
        return 'Business Day'
    elif re.search("payment date", text):
        return 'Payment Date'
    else:
        return 'Not Found'        

   else:            
    return 'Not found'



def point3(text):
   if  re.search("interest account issuer", text):
        
        start = 'interest account issuer'
        end = 'unused proceeds account issuer procure'
        text = ''.join([i for i in text if not i.isdigit()])
        text = ' '.join(text.split())
        text = text[text.find(start)+len(start):text.rfind(end)]

        if  re.search("trading gains | investment gains", text):
            return 'Yes'
        else:
            return 'No'
       
        
   else:
         return 'Not found'

def point4(text): 
   if  re.search("reinvestment overcollateralisation test means test apply", text):

        text = text.split("reinvestment overcollateralisation test means test apply",1)[1]
       
        text = text.split()[:35]
        
        text = "".join([" "+i if not i.startswith("'") and i not in string.punctuation else i for i in text]).strip()
        
        result = re.findall(r"[-+]?\d*\.\d+|\d+", text)
        
        if len(result) == 0:
            return 'Not found'
        else:
            return result[0]+'%'

   elif re.search("required diversion respect class f par value test", text):

        text = text.split("required diversion respect class f par value test",1)[1]
       
        text = text.split()[:35]
        
        text = "".join([" "+i if not i.startswith("'") and i not in string.punctuation else i for i in text]).strip()
        
        result = re.findall(r"[-+]?\d*\.\d+|\d+", text)
        
        if len(result) == 0:
            return 'Not found'
        else:
            return result[0]+'%'
        
   elif re.search("interest diversion test", text):

        text = text.split("interest diversion test means",1)[1]
       
        text = text.split()[:35]
        
        text = "".join([" "+i if not i.startswith("'") and i not in string.punctuation else i for i in text]).strip()
        
        result = re.findall(r"[-+]?\d*\.\d+|\d+", text)
        
        if len(result) == 0:
            return 'Not found'
        else:
            return result[0]+'%'
        
   elif re.search("additional reinvestment test apply", text):

        text = text.split("additional reinvestment test apply",1)[1]
        text = text.split("class f par value ratio",1)[1]
       
        text = text.split()[:50]
        
        text = "".join([" "+i if not i.startswith("'") and i not in string.punctuation else i for i in text]).strip()
        
        result = re.findall(r"[-+]?\d*\.\d+|\d+", text)
        
        if len(result) == 0:
            return 'Not found'
        else:
            return result[0]+'%'
        
   elif re.search("reinvestment par value test means", text):

        text = text.split("reinvestment par value test means",1)[1]

        text = text.split()[:50]
        
        text = "".join([" "+i if not i.startswith("'") and i not in string.punctuation else i for i in text]).strip()
        
        result = re.findall(r"[-+]?\d*\.\d+|\d+", text)
        
        if len(result) == 0:
            return 'Not found'
        else:
            return result[0]+'%'
        
   elif re.search("reinvestment test met date", text):

        text = text.split("reinvestment test met date",1)[1]

        text = text.split()[:50]
        
        text = "".join([" "+i if not i.startswith("'") and i not in string.punctuation else i for i in text]).strip()
        
        result = re.findall(r"[-+]?\d*\.\d+|\d+", text)
        
        if len(result) == 0:
            return 'Not found'
        else:
            return result[0]+'%'       
        
   else:
        return 'Not found'


def point5(text):
   if  re.search("covlite loan means", text):
        
        text = text.split("covlite loan means",1)[1]

        text = text.split()[:100]

        text = "".join([" "+i if not i.startswith("'") and i not in string.punctuation else i for i in text]).strip()

        text = ''.join([i for i in text if not i.isdigit()])

        text = re.sub(r'\b\w{1,1}\b', '', text)
        text = ' '.join(text.split()) 
        
        if  re.search("crossdefault | pari passu", text):
            return 'WEAK'
        
        else:
            return 'STRONG'
            
        
   else:
        return 'Not found'


def point6(text):
   if  re.search("covlite loans", text):
       if  re.search("portfolio profile tests consist following the percentage", text):
           text = text.split("portfolio profile tests consist following the percentage",1)[1]
           text = text.split("covlite loans",1)[1]
           text = text.split()[:5]
           text = "".join([" "+i if not i.startswith("'") and i not in string.punctuation else i for i in text]).strip()
           result = re.findall(r"[-+]?\d*\.\d+|\d+", text)
           return result[0]+'%'
        
       elif  re.search("moodys rating derived sp rating", text):
             text = text.split("moodys rating derived sp rating",1)[1]
             text = text.split()[:5]
             text = "".join([" "+i if not i.startswith("'") and i not in string.punctuation else i for i in text]).strip()
             result = re.findall(r"[-+]?\d*\.\d+|\d+", text)
             return result[0]+'%'
       
       else:
           return 'Not found'
        
   else:
       return 'Not found'                          

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

        punctuations4 = '''!()“-[]{};:”'"’\,<>/?@#$%^&*_~'''

        no_punct_text = ""
        no_punct_text4 = ""

        for char in text:
           if char not in punctuations:
              no_punct_text = no_punct_text + char
           if char not in punctuations4:
              no_punct_text4 = no_punct_text4 + char
                
        text = re.sub('[ﬂﬁ]', '', no_punct_text)
        text = re.sub('maximum', '', text)

        #remove multiple whitespaces
        text = ' '.join(text.split()) 

        text2 = ''.join([i for i in text if not i.isdigit()])
        text2 = ' '.join(text2.split())

        text3 = text.replace('accounts', 'account')
        text4 = ' '.join(no_punct_text4.split()) #Use this text for keypoint 4 & 6
        text5 = ' '.join(no_punct_text.split())
        text6 = text4


        if  re.search("average life test weighted average life", text):

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
                
                text1 = cl.classify(text)
                text2 = point2(text2)
                text3 = point3(text3)
                text4 = point4(text4)
                text5 = point5(text5)
                text6 = point6(text6)
                return jsonify(point1 = text1, point2 = text2, point3 = text3, point4 = text4, point5 = text5, point6 = text6)
                # return send_file(file_name, as_attachment=True)

        else:        
                return 'Not Found'
           


    else:
        result = request.args.get['myfile']
    return result

if __name__ == '__main__':
    app.run(debug=True)


