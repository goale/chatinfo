import glob
from bs4 import BeautifulSoup
import csv
import re

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

        non_alpha = re.compile(r'[^A-Za-zА-Яа-я\s\-\d]')

        for message in messages:
            name_div = message.find('div', {'class': 'from_name'})
            date_div = message.find('div', {'class': 'date'})
            text_div = message.find('div', {'class': 'text'})
            if name_div:
                name = name_div.text.strip()
            if date_div:
                date = date_div['title']
            if text_div:
                text = non_alpha.sub('', text_div.text.strip()).lower()

            if name and date and text:
                message_data_set.append((name, date, text))

# print(message_data_set)
print('Writing message data set to csv...')
with open('output/messages.csv', 'w') as csv_file:
    writer = csv.writer(csv_file, delimiter='\t')
    writer.writerows(message_data_set)