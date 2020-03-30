#!/usr/bin/env python
# coding: utf-8

# In[1]:


##This script transfers an Youtube playlist to an Anghami playlist
##To get this wroking you need fill in the variables below with:
# 1. playlist ID
# 2. your youtube API key
# 3. your Anghami api key
##It is also VERY IMPORTANT TO CREATE A PLAYLIST IN ANGHAMI NAMED "Youtube" (case-sensitive)
##The playlist is limited to 50 songs
##
## THIS SCRIPT IS NOT PERFECT
## IT DOES NOT VALIDATE THE SONGS BEFORE ADDING THEM - SO IT COULD ADD THE WRONG SONG


# In[2]:


import requests ##for online access
import json ##to properly parse JSON
import re ##for regex functionality


# In[3]:


playlistID = "PLFgquLnL59alCl_2TQvOiD5Vgm1hCaGSI" ##Playlist ID
youtubeKey = "" ##Youtube OAuth Key
anghamiKey =  "" ##Anghami api auth key


# In[4]:


##get youtube playlist
r = requests.get('https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId={}&key={}'.format(playlistID,youtubeKey))
t = json.loads(r.text)


# In[5]:


##get list of song names
songNames = [];
for song in t["items"]:
    songNames.append(song["snippet"]["title"])


# In[6]:


##get the right playlist ID from the Anghami app
r = requests.get('https://bus.anghami.com/public/user/playlists/', headers={'XAT': 'interns', 'XATH': anghamiKey})
t = json.loads(r.text)
#get ID of playlist called Youtube
playlistID = ""
for playlist in t["playlists"]:
    if playlist['name'] == "Youtube":
        playlistID = playlist['id']


# In[12]:


#Now we need to search for the song
for song in songNames:
    #replace irrelavent bits of video titles
    song = re.sub("[[(]?(Official)? (Music )?(Video|Audio)[])]?","",song)
    song = re.sub("\(Official\)|\(Audio\)","",song)
    song = re.sub("\(.*\)","",song) #extreme option
    #get actual artist name 
    #it seems the format is always Artist - Song Name
    artist = ""
    name = ""
    if re.match("(.*)-(.*)",song):
        artist = re.match("(.*?)-",song).group(1)
        name = re.match("(.*)-(.*)",song).group(2) #not too accurate so i'll ignore it
    
    #issue search request
    r = requests.get('https://bus.anghami.com/public/search?query={}'.format(song) , headers={'XAT': 'interns', 'XATH': anghamiKey})
    # take the first result only
    t = json.loads(r.text)
    songIDtoAdd = t["results"][0]["id"]
    #now add it to the playlist
    r = requests.get('https://bus.anghami.com/public/playlist/add?song_id={}&playlist_id={}'.format(songIDtoAdd,playlistID) , headers={'XAT': 'interns', 'XATH': anghamiKey})
    #check if its is successful
    if r.ok != True:
        print("Error! Couldn't add: " , song)
    else:
        print("added: ", song)


# In[ ]:





# In[ ]:





# In[ ]:




