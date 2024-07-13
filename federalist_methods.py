from bs4 import BeautifulSoup
import re
import nltk
import string
import requests

url = 'https://avalon.law.yale.edu/18th_century/'

# I set up a for loop to gather each paper, each paper had its own URL
# But I had to account for inconsistent URLs on Yale's server
one_through_nine = [url + 'fed0{0}.asp'.format(i) for i in range(1, 10)]
ten_through_eightysix = [url + 'fed{0}.asp'.format(i) for i in range(10, 86)]
urls = one_through_nine + ten_through_eightysix
page_requests = [requests.get(url) for url in urls]
soups = [BeautifulSoup(page.text, 'html.parser') for page in page_requests]


def return_title(integer: int):
    soup = soups[integer]
    title = [title for title in soup.findAll('div', class_='document-title')][0]
    cleaned_title = [re.sub(r'\r\n', '', item) for item in title]
    return cleaned_title


def return_author(integer: int):
    author = ''
    soup = soups[integer]
    for h3_tag in soup.findAll('h3'):
        author = h3_tag.contents[-1]
    for h4_tag in soup.findAll('h4'):
        author = h4_tag.contents[-1]
    return author


def return_paper(integer: int):
    soup = soups[integer]
    paper = [p.string for p in soup.select('p') if p.string is not None]
    sents = [nltk.sent_tokenize(strng.lower()) for strng in paper]
    joined = [' '.join(sent) for sent in sents]
    sents_joined = [nltk.sent_tokenize(join) for join in joined]
    return sents_joined


def clean_paper(integer: int):
    inner_list, cleaned_list = [], []
    for sents_list in return_paper(integer):
        for sent in sents_list:
            inner_list.append(nltk.sent_tokenize(sent))
    inner_joined = [''.join(nested_list) for nested_list in inner_list]
    for nested_list in inner_list:
        for string_list in nested_list:
            cleaned_string = re.sub(r'[^a-zA-Z\s]', '', string_list)
            if cleaned_string.startswith('to the people of the state of new york:'):
                continue
            elif cleaned_string.startswith('publius.'):
                continue
            else:
                cleaned_list.append(cleaned_string)
    return cleaned_list


def return_subtitle(integer: int):
    subtitle = []
    if integer > len(soups):
        return '{0} is beyond the index of the soups object'.format(integer)
    soup = soups[integer]
    for h4_tag in soup.findAll('h4'):
        subtitle = [h4_tag.text for h4_tag in soup.findAll('h4')]
    for h3_tag in soup.findAll('h3'):
        subtitle = [h3_tag.text for h3_tag in soup.findAll('h3')]
    return subtitle


subtitle_total = [return_subtitle(i) for i in range(0, len(soups))]


def clean_subtitle():
    subtitle_list = []
    for item_list in subtitle_total:
        for item in item_list:
            item_lines = item.splitlines()
            cleaned_lines = [re.sub('HAMILTON', '', item) for item in item_lines]
            cleaned_lines = [re.sub('JAY', '', item) for item in cleaned_lines]
            cleaned_lines = [re.sub('AND MADISON', '', item) for item in cleaned_lines]
            cleaned_lines = [re.sub('MADISON', '', item) for item in cleaned_lines]
            cleaned_lines = [re.sub('OR', '', item) for item in cleaned_lines]
            cleaned_lines = [re.sub('For the Independent Journal', '', item) for item in cleaned_lines]
            cleaned_lines = [re.sub("From McLEAN'S Edition, New York.", '', item.strip()) for item in cleaned_lines]
            cleaned_lines = [item for item in cleaned_lines if item]
            cleaned_lines = [re.sub('\.', '', item) for item in cleaned_lines]

            if len(cleaned_lines) == 0:
                continue
            else:
                subtitle_list.append(' '.join(cleaned_lines))

    return subtitle_list
