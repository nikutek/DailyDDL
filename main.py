import random
import codecs
import os
import cv2
import datetime
from PIL import Image, ImageFont, ImageDraw
from funcs import predict_encoding, losowanieZdan
import shutil
from CONS import USERNAME, PASSWORD, GODZINA, MINUTA, HASHTAGI
import time



def main():
    #TODO: Pobieranie i zapisywanie tekstów piosenek
    teksty = {}

    for plik in os.listdir("./teksty") :
        teksty[plik] = []

        if predict_encoding(f'{os.getcwd()}/teksty/{plik}', 40) == 'utf-8':
            with codecs.open('./teksty/' + plik, 'r', encoding='utf-8', errors='ignore') as tekst:
                tekst = tekst.read().split('\r\n')
                for i in tekst:
                    teksty.setdefault(plik, []).append(i)
        elif predict_encoding(f'{os.getcwd()}/teksty/{plik}', 40) == 'Windows-1252':
            with codecs.open('./teksty/' + plik, 'r', encoding='ANSI', errors='ignore') as tekst:
                tekst=tekst.read().split('\r\n')
                for i in tekst:
                    teksty.setdefault(plik, []).append(i)
        else:
            print(f'nie znane kodowanie pliku {plik}')
            print('predict: {}'.format(predict_encoding(f'{os.getcwd()}/teksty/{plik}', 40)))




     #TODO: losowanie tekstu

    text = losowanieZdan(teksty)


     #TODO: losowanie obrazu
    video = '{}'.format(random.choice(os.listdir('./teledyski')))

    cap = cv2.VideoCapture(f'./teledyski/{video}')
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    cap.set(1,random.randint(1,frame_count));
    ret, frame = cap.read()
    cv2.imshow('window_name', frame)

    filename = str(datetime.date.today())+'.jpg'
    os.chdir('./produkt')
    cv2.imwrite(filename, frame)

    #TODO: łączenie obrazu z tekstem
    img = Image.open(filename)
    os.chdir('..')

    #losowanie czcionki
    fonts = []
    for font in os.listdir("./fonts"):
        fonts.append(font)


    #formatowanie tekstu
    for t in list(text.values()):

        # losowanie wielkości tekstu
        fontSize = round((100-len(t))*0.5)
        font = random.choice(fonts)
        font = ImageFont.truetype('./fonts/{}'.format(font), size=fontSize)

        #pól losowe wybieranie pozycji (aby bylo w oknie)
        estWidth = fontSize*0.5 * len(t)
        pozycja =(random.randint(0,round(640-estWidth)),random.randint(0,360)) #x, y




        #losowanie koloru
        kolor = (random.randint(0,255),random.randint(0,255),random.randint(0,255))


        editableIMG = ImageDraw.Draw(img)
        editableIMG.text(pozycja, t, kolor, font)

    img.show()
    img.save(f'./produkt/{filename}')

    #generowanie opisu pod post
    for i in list(text.keys()):
        nazwa = text[i]
        tytul = list(i)
        for znak in tytul:
            if znak == '-':
                tytul[tytul.index('-')] = ' '
        tytul = ''.join(tytul).split('.')[0]

    tagi = []
    for i in range(1,10):
        tagi.append(random.choice(HASHTAGI))

    caption = tytul + ' - ' + nazwa +"\n\n"

    for i in tagi:
        caption += '#'+i+' '

    print(caption)
    #TODO: upload na instagrama


    from instabot import Bot

    bot = Bot()

    bot.login(username = USERNAME,
              password = PASSWORD)

    sciezka = os.getcwd()+"\\produkt\\"+ filename

    bot.upload_photo(sciezka, caption =caption)



if __name__ == "__main__":
    while True:
        now = datetime.datetime.now()
        if now.hour == GODZINA and now.minute == MINUTA:
            main()
            time.sleep(3600)
        else:
            time.sleep(30)







