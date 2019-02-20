#!/usr/bin/env python
# coding: utf-8

# # Request Intro

# In[38]:


import requests
import json
import random
from pprint import pprint


# In[2]:


url = "https://api.spacexdata.com/v2/launchpads"
print(requests.get(url))

#200 is a good signal code


# In[3]:


#Raw Data
print(requests.get(url).json())


# In[4]:


#Pretty print the json
response = requests.get(url).json()
print(json.dumps(response, indent=4, sort_keys=True))


# # Manipulating JSON

# In[13]:


url_space = "https://api.spacexdata.com/v2/rockets/falcon9"
response_space = requests.get(url_space)
response_space_json = response_space.json()
print(json.dumps(response_space_json, indent=4, sort_keys=True))


# In[17]:


print(response_space_json["cost_per_launch"])
number_payloads = len(response_space_json['payload_weights'])
print(f'There are {number_payloads} payloads.')
payload_weight = response_space_json["payload_weights"][0]["kg"]
print(f"The first payload weighed {payload_weight} Kilograms")


# # Star Wars API
# Using the starter file provided, collect the following pieces of information from the Star Wars API.
# 
# - The name of the character
# - The number of films they were in
# - The name of their first starship
# - Collect and print out all of the films a character appeared 
# 
# Once the data has been collected, print it out to the console.

# In[19]:


url_star = "https://swapi.co/api/people/"
print(json.dumps(requests.get(url_star).json(), indent=4, sort_keys=True))


# In[21]:


# Create a url with a specific character id
character_id = '4'
url_character = url_star + character_id
print(url_character)


# In[27]:


# Perform a get request for this character
response_character = requests.get(url_character)
print(response_character.json)


# In[28]:


print(json.dumps(response_character.json(), indent=4, sort_keys=True))


# In[34]:


#The name of the character
character_name = response_character.json()['name']

#The number of films they were in
film_number = len(response_character.json()['films'])

#The name of their first starship
ship_url = response_character.json()['starships'][0]
response_ship = requests.get(ship_url).json()
first_ship = response_ship['name']
response_ship


# In[35]:


print(f"{character_name} was in {film_number} films")
print(f"Their first ship: {first_ship}")


# In[37]:


#Collect and print out all of the films a character appeared
films = []

for film in response_character.json()['films']:
    url_film = requests.get(film).json()
    film_title = url_film['title']
    films.append(film_title)

print(f'{character_name} was in: {films}')


# # Number Facts API

# In[6]:


url_num = 'http://numbersapi.com/'
url_example = 'http://numbersapi.com/42?json'
print(json.dumps(requests.get(url_example).json(), indent=4, sort_keys=True))


# In[13]:


search = input("What you want to search for? [Trivia, Math, Date, or Year] ")


# In[14]:


if(search.lower() == 'date'):
    month = input('What month? ')
    day = input('What day? ')
    response_num = requests.get(f'{url_num}{month}/{day}/{search.lower()}?json').json()
    print(response_num['text'])
else:
    number = input('What number? ')
    response_num = requests.get(url_num + number + "/" + search.lower() + "?json").json()
    print(response_num['text'])    


# # The Open Movie Database API (OMDb)
# Use the OMDb API to retrieve and print the following information.
# - Who was the director of the movie Aliens?
# - What was the movie Gladiator rated?
# - What year was 50 First Dates released?
# - Who wrote Moana?
# - What was the plot of the movie Sing?

# In[27]:


#Get the url
url_movie = "http://www.omdbapi.com/?apikey=trilogy&t="

#Director of ALiens
movie = requests.get(url_movie + "Aliens").json()
print(f'The director of Aliens was {movie["Director"]}.')
      
#Rating of the Gladiator
movie = requests.get(url_movie + "Gladiator").json()
print(f'The rating of Gladiator was {movie["Rated"]}.')
      
#50 First Dates release year
movie = requests.get(url_movie + "50 First Dates").json()
print(f'The movie 50 First Dates was released in {movie["Year"]}.')
      
#Writer of Moana
movie = requests.get(url_movie + "Moana").json()
print(f'Moana was written by {movie["Writer"]}.')

#Plot of the movie Sing?
movie = requests.get(url_movie + "Sing").json()
print(f'The plot of Sing was: {movie["Plot"]}')


# # Movie Loop

# In[37]:


movies = ["Aliens", "Sing", "Moana"]

response_movie = [];

for movie in movies:
    movie_data = requests.get(url_movie + movie).json()
    response_movie.append(movie_data)
    print(f'The director of {movie} is {movie_data["Director"]}')


# In[30]:


response_movie


# # New York Times API

# In[44]:


api_key = 'JlZ0WPv6ICsUucubnQHcpUvZdD43HNGE'
url_sample_nyt = 'https://api.nytimes.com/svc/search/v2/articlesearch.json?api-key='+api_key+'&q='
url_nyt = 'https://api.nytimes.com/svc/search/v2/articlesearch.json?'
print(json.dumps(requests.get(url_sample_nyt).json(), indent=4, sort_keys=True))


# In[78]:


query = 'vietnam'
query_url = url_nyt + 'api-key=' + api_key + '&q=' + query
articles = requests.get(query_url).json()
for i in range(0,10):
    articles_list = [article for article in articles["response"]["docs"][i]["headline"]["main"]]
    output = ''.join(articles_list)
    print(output)


# In[ ]:




