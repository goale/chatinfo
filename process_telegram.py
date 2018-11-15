import glob
from bs4 import BeautifulSoup

files_sorted = sorted(glob.iglob('data/**/*.html'))

message_data_set = []

for filename in files_sorted:
    print('Parsing %s...' % filename)
    with open(filename) as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        messages = soup.findAll('div', {'class': ['message', 'default']})
        name = None
        date = None
        text = None
        for message in messages:
            name_div = message.find('div', {'class': 'from_name'})
            date_div = message.find('div', {'class': 'date'})
            text_div = message.find('div', {'class': 'text'})
            if name_div:
                name = name_div.text.strip()
            if date_div:
                date = date_div['title']
            if text_div:
                text = text_div.text.strip().lower()

            if text:
                message_data_set.append((name, date, text, text.split(' ')))

# print(message_data_set)