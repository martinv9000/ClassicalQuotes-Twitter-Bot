import tweepy
import openai
import time
from keep_alive import keep_alive
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from keys import uri, API_key, API_key_secret, Bearer_token, Access_token, Access_token_secret, openai_key

client = MongoClient(uri, server_api=ServerApi('1'))
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

mydb = client['TwitterBot']
mycollection = mydb["ClassicalQuotes"]

client = tweepy.Client(Bearer_token,API_key,API_key_secret,Access_token,Access_token_secret)
auth = tweepy.OAuth1UserHandler(API_key,API_key_secret,Access_token,Access_token_secret)
api = tweepy.API(auth)

message = "Give me a deep and meaningful quote from an influential philosopher born before 1800. Respond with just the quote. Put it in the format \"Quote.\" - philosopher"

def tweet(quote):
    client.create_tweet(text=quote)

def chatgpt(message):
    openai.api_key = openai_key
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=message,
        max_tokens=50,
        temperature=0.7
    )
    if 'choices' in response and len(response['choices']) > 0:
        return response['choices'][0]['text'].strip()
    else:
        return ''


keep_alive()

k=0
while True:
    response = chatgpt(message)
    if mycollection.find_one({"Tweet": response}):
      print("duplicate")
    else:
      if response[0]==".":
        print("Typo generated")
      else:
        tweet(response)
        print("Tweeted: ", response)
        item = {"Tweet":response}
        last = mycollection.insert_one(item)

        
        time.sleep(21600)
