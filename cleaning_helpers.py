import requests
from bs4 import BeautifulSoup
import re
import string


def make_soup(url):
    r = requests.get(url).text
    return BeautifulSoup(r, 'html.parser')


def remove_whitespace(text):
    return ' '.join(text.split())


def remove_unicode(text):
    return re.sub(r'[^\x00-\x7F]', '', text)


def clean(t):
    t = [txt.encode("ascii", "ignore").decode("ascii") for txt in t]
    # remove unicode characters
    # lower each string
    t = [txt.lower() for txt in t]
    # remove new line escape character
    t = [txt.replace('\n', ' ') for txt in t]
    # remove punctuation
    t = [re.sub('[%s]' % re.escape(string.punctuation), ' ', txt) for txt in t]
    # remove digits
    t = [re.sub('[%s]' % re.escape(string.digits), ' ', txt) for txt in t]
    # remove empty strings
    t = [txt.strip() for txt in t if txt]
    return t


# remove unicode, tab, and line break characters
# splitting by tab maintains the structure and sections of the document
def clean_opinion_text(opinion_text):
    return [
        [remove_unicode(item) for item in txt.split('\n') if item.strip() != '']
        for txt in opinion_text.split('\t')
        if txt.strip() != ''
    ]
