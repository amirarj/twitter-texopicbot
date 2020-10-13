import os
import re
import time

import rtl
import tweepy
from PIL import Image, ImageDraw, ImageFont


class picture_maker:
    def __init__(self):
        self.text=1
    def make_pic(text="your text!", pic="niche.jpg", rgb=(0,0,0), coordinates=(0,0), size=30, font="Vazir.ttf", temp=None):
        if len(text) > 30:
            #Separate the words by ' ' .
            temp_text = text.split(' ')
            text=''
            n=0
            line=0
            lines=['']
            while n!=len(temp_text):
                lines[line]+=temp_text[n]+' '
                if len(lines[line])>=30:
                    lines[line]+='\n'
                    line+=1
                    lines.append('')    
                n+=1
            #Paste the lines together
            if not '\n' in lines[line]: lines[line]+='\n'
            i=0
            for _line in lines:
                text+=_line
                i+=1
                if i==9:break
        img = Image.open(pic)
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(font,size)
        draw.text(coordinates,rtl.rtl(text),rgb,font=font,align='center')
        img.save(temp)



def remove_links(text):
    return re.sub(r'(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})\S*', '', text)



class MyStreamListener(tweepy.StreamListener): 
    def on_status(self, status):
        try:    
            if status.in_reply_to_status_id:
                tw = api.get_status(status.in_reply_to_status_id, tweet_mode="extended")
                text = tw.full_text.replace('!makeit', '')
                text = remove_links(text)
                if len(text) != 0:
                    filename = f"{tw.id}.jpg"
                    picture_maker.make_pic(text, "niche.jpg", (255,255,255), (400,150), 33, font="Vazir.ttf", temp=filename)
                    picture_maker.make_pic("-- "+ tw.user.name, filename, (255,255,255), (950,600), 25, font="Shabnam.ttf", temp=filename)
                    api.update_with_media(filename, in_reply_to_status_id=status.id, auto_populate_reply_metadata=True)
                    os.remove(filename)
            else:
                try:
                    text = status.extended_tweet["full_text"].replace('!makeit', '')
                except AttributeError:
                    text = status.text.replace('!makeit', '')
                text = remove_links(text)   
                if len(text) != 0:
                    filename = f"{status.id}.jpg"
                    picture_maker.make_pic(text, "niche.jpg", (255,255,255), (400,150), 33, font="Vazir.ttf", temp=filename)
                    picture_maker.make_pic("-- "+ status.user.name, filename, (255,255,255), (950,600), 25, font="Shabnam.ttf", temp=filename)
                    api.update_with_media(filename, in_reply_to_status_id=status.id, auto_populate_reply_metadata=True)
                    os.remove(filename)
        except Exception as e:
            print(e)

                



auth = tweepy.OAuthHandler(consumer_key='', consumer_secret='')
auth.set_access_token('', '')
api = tweepy.API(auth, wait_on_rate_limit=True)



myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
myStream.filter(track=['!makeit'])
