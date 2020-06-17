import time
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
from selenium import webdriver
import tweepy 
import random
import textwrap
import json

consumer_key = "XXX"
consumer_secret = "XXX"
access_token = "XXX"
access_token_secret = "XXX"
deepai_API_key = "XXX"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
auth.set_access_token(access_token, access_token_secret) 
api = tweepy.API(auth) 


def get_random_caption():
    driver = webdriver.Chrome()
    driver.get("https://randomtextgenerator.com/")
    caption = driver.find_element_by_id('generatedtext')
    captions = caption.text.split('.')
    return captions[0]

def genrate_image_with_text(text):
    para = textwrap.wrap(text, width = 85)
    MAX_W, MAX_H = 800, len(para) * 75 
    im = Image.new('RGB', (MAX_W, MAX_H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    current_h, pad = 50, 10
    for line in para:
        w, h = draw.textsize(line, font=ImageFont.truetype('arial.ttf', 18))
        draw.text(((MAX_W - w) / 2, current_h), line, font=ImageFont.truetype('arial.ttf', 18))
        current_h += h + pad
    im.save('post.jpg')

def post_weird_image_and_caption():
    c = get_random_caption()
    r = requests.post(
        "https://api.deepai.org/api/text2img",
        data = 
        {
            'text': c.split()[0] + c.split()[1],
        },
        headers = 
        {
            'api-key': deepai_API_key
        }
    )
    Image.open(BytesIO(requests.get(r.json()["output_url"]).content)).save('post.jpg')
    api.update_with_media('post.jpg' , c + f". #AI #random #bot #{c.split()[0]} #{c.split()[1]}")  
    
def post_random_beautiful_image():
    Image.open(BytesIO(requests.get('https://source.unsplash.com/random').content)).save('post.jpg')
    api.update_with_media('post.jpg', "I present to you a random image. #image #random #bot #unsplash")

def post_random_trivia():
    driver = webdriver.Chrome()
    driver.get('https://www.google.com/search?q=im+feeling+curious')
    time.sleep(5)
    Q = driver.find_element_by_class_name('sW6dbe').text
    A = driver.find_element_by_class_name('EikfZ').text 
    genrate_image_with_text(A)
    for q in Q.split():
        if '?' in q:
            Q += f" #{q[0:len(q) - 1]}"
        else:
            Q += f" #{q}"
    Q += " #randomfact #trivia #bot "
    api.update_with_media('post.jpg', Q)
    
def post_random_number_fact():
    caption = requests.get('http://numbersapi.com/random/trivia').text
    caption += f" #number{caption.split()[0]} #mathfact #maths #randomnumber #number #bot #random"
    api.update_status(caption)
 
if __name__ == "__main__":
    fns = [post_random_beautiful_image, post_random_number_fact, post_random_trivia, post_weird_image_and_caption]
    random.choice(fns)()
