'''MESSAGE TO CLIENT: I am creating the code in units, which I will then integrate into the flask application
                    : I have had lots of trouble reading PDFs into the code. I suspect PyPDF2 is not the best module for reading Moody's PDFs. I shall perform
                      further testing tomorrow'''
import PyPDF2
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

def get_text():
    '''This function retrieves text from the PDF file. It closely mirrors the operations in 'app.py'

    MESSAGE TO CLIENT: I used PyPDF2 because I was having lots of trouble with Tika and Flask. PyPDF2 isn't reading some of the PDFs you sent me
    either so I will retest tomorrow or Sunday after reinstalling Flask and Tika
    '''
    pdf_file_object = open(r'Sample_PDFs/ALME 4.pdf', 'rb')
    pdf_object = PyPDF2.PdfFileReader(pdf_file_object)
    text = ""
    for x in range(pdf_object.getNumPages()):
        page = pdf_object.getPage(x)
        page_content = page.extractText()
        text = text + page_content

    # text = text.replace(r'\n', '')
    text = text.lower()

    cachedStopWords = stopwords.words("english")
    clean_text = ' '.join([word for word in text.split() if word not in cachedStopWords])

    punctuations = '''!()“-[]{};:”'"’\,<>./?@#$%^&*_~'''
    no_punct_text = ""
    for char in clean_text:
        if char not in punctuations:
            no_punct_text = no_punct_text + char


    return text, clean_text

def WARF_condition_test(text):
    '''Return the WARF WARF_condition

    Parameters: text
    Possible outputs: STRONG, WEAK, or NOT FOUND
    MESSAGE TO CLIENT: I will modify the regular expression in this function based on the output of Tika parser, which may be different from that of PyPDF2
    '''

    new_text = re.split(r'(?:reinvestment of collateral obligations|reinvestment of collateral debt obligations)(?:\s"reinvestment criteria")', text)[1]#select the part of the text after the regular expression match
    new_text = re.split(r'following the expiry of the reinvestment period following the expiry of the reinvestment period', new_text)[1]#select the part of the text after the regular expression match
    #TODO: Ensure that error is not thrown in case the phrases above are not found. Could do so by checking with if statements
    regex = re.search(r'maximum weighted average rating[^;]*', new_text)#search for text from the phrase 'maximum weighted average rating' until the next semicolon
    new_text= regex.group()#pass matching text into the new_text string

    WARF_condition = 'NOT FOUND'#set WARF_condition flag to NOT FOUND. Useful in case document does not contain information about the condition
    if new_text:#if new_text is blank, program will not enter the if function and WARF_condition will remain NOT FOUND
        if 'maintain or improve' in new_text:
            WARF_condition = 'WEAK'
        else:
            WARF_condition = 'STRONG'

    return WARF_condition

text, clean_text = get_text()
text = text.replace("\n", '')

WARF_condition = WARF_condition_test(text)
print(WARF_condition)
