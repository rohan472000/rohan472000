from io import BytesIO
import PySimpleGUI as sg
from PIL import Image
import requests, json

def image_to_data(im):
    with BytesIO() as output:
        
        im = im.resize((400, 400), Image.ANTIALIAS)
        im.save(output, format="PNG",optimize=True)
        data = output.getvalue()
    return data

def get_data():
    reddit_url = 'https://www.reddit.com/r/memes/random.json?limit=1'
    
    headers = {
        'User-Agent': (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
        )
    }
    
    response = requests.get(reddit_url, headers=headers)
    meme_data = json.loads(response.content)
    meme_url = meme_data[0]['data']['children'][0]['data']['url']
    
    data = requests.get(meme_url).content
    stream = BytesIO(data)
    img = Image.open(stream)
    giy = image_to_data(img)
    return giy

control_col = sg.Column([[sg.Button('next meme', key = '_3_')],])
image_col = sg.Column([[sg.Image(get_data(), key = '-IMAGE-')]])
layout = [[control_col,image_col]]
window = sg.Window('meme gen', layout,finalize=True)
w1, h1 = window.size
w2, h2 = sg.Window.get_screen_size()
if w1>w2 or h1>h2:
    window.move(0, 0)
while True:
    event, values = window.read()

    if event is None:
        break
    if event == '_3_':
        window['-IMAGE-'].update(get_data())

window.close()
