import random

def predict_encoding(file_path, n_lines=20):
    '''Predict a file's encoding using chardet'''
    import chardet

    # Open the file as binary data
    with open(file_path, 'rb') as f:
        # Join binary lines for specified number of lines
        rawdata = b''.join([f.readline() for _ in range(n_lines)])

    return chardet.detect(rawdata)['encoding']

def szansa(x):
    return round(x**3)

def losowanieZdan(Dict):
    text = {}

    iloscZdan=1       # losowanie ilosci zdan w jakis dziwny sposob na szybko wymyslony
    for i in range(2, 10):
        if random.randint(1, szansa(i)) == 1: iloscZdan += 1

    for i in range(iloscZdan):
        tytul = random.choice(list(Dict.keys()))
        zdanie = random.choice(list(Dict[tytul]))
        text[tytul] = zdanie

    return text