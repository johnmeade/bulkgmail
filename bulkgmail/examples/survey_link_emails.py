'''
Consumes a CSV containing emails and names, outputs a new CSV with additional "uid" and "url" columns.
'''

import csv
from argparse import ArgumentParser
from random import randint, choice as rand_choice

URLS = [
    'https://google.com#a',
    'https://google.com#b',
    'https://google.com#c',
    'https://google.com#d',
    'https://google.com#e',
    'https://google.com#f',
    'https://google.com#g',
    'https://google.com#h',
]

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--names_and_emails", required=True, type=str,
        help='CSV file containing "name" and "email" fields')
    parser.add_argument("--output", required=True, type=str,
        help='Output filename')
    args = parser.parse_args()

    codes = set()

    with open(args.names_and_emails, 'r') as f:
        contexts = list(csv.DictReader(f))

    data = list()
    for context in contexts:
        # get unique code
        cond = True
        while cond:
            code = str(randint(0, 1e8)).zfill(8)
            cond = code in codes
        codes.add(code)
        # add metadata to context
        context.update({
            'uid': code,
            'url': rand_choice(URLS),
        })
        data.append(context)

    header = list(data[0].keys())
    with open(args.output, 'w') as f:
        f.write(','.join(header) + '\n')
        for dat in data:
            row = ','.join([ dat[k] for k in header ])
            f.write(row + '\n')

    print(f'Finished, now run the main program with "{args.output}" as the "data"')
