import time
from PIL import Image
import requests
from io import BytesIO
from selenium import webdriver
import tweepy 

def get_random_image():
    response = requests.get('https://source.unsplash.com/random')
    img = Image.open(BytesIO(response.content))
    img.save('post.jpg')
    print("Image Fatched !")

def get_random_caption():
    driver = webdriver.Chrome()
    driver.get("https://randomtextgenerator.com/")
    caption = driver.find_element_by_id('generatedtext')
    captions = caption.text.split('.')
    print("Caption Fatched !")
    return captions[0] + '. '+ f'#{captions[1].split()[0]} ' + f'#{captions[1].split()[1]} ' + f'#{captions[1].split()[2]}' 
    
def post(caption):
    consumer_key = "XXX"
    consumer_secret = "XXX"
    access_token = "XXX"
    access_token_secret = "XXX"
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
    auth.set_access_token(access_token, access_token_secret) 
    api = tweepy.API(auth) 
    for follower in api.followers_ids():
        api.create_friendship(follower)
    image_path ='post.jpg' 
    caption+=" #bot #random"
    api.update_with_media(image_path, caption)  
    
if __name__ == "__main__":
    get_random_image()
    caption=get_random_caption()
    post(caption)
