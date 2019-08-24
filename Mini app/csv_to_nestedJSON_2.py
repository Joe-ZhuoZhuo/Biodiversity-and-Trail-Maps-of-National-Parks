import csv

with open('data/species.csv', 'rt') as f:
    reader = csv.DictReader(f, delimiter=',')
    for row in reader:
        print(row)
        print(f'Header: {reader.fieldnames}')
