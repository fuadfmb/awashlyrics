# Kiilolee Music
## Music & Lyrics site for East Africa


Kiilolee Music is a music and lyrics website powered with Django web framework. The Aim of this project is putting together representative samples of music in East Africa/archiving all east African music on a our server and allowing others to access those resources in an easy way.

This project contains different models. some of the models are : 

- Language
- Category
- Artist
- Album
- Song
- Lyrics
- Gallery
- ArtImage
- AlbumComments
- SongComments
- SongLikes and
- Playlist

## How the Model is designed

According to this project:- 
- An **Artist** can have many **Albums**.
- When a new **Artist** created, an new **Album** that belongs to an **Artist** called **'Singles'** will be added to **Albums**.
- An **Album** always belongs to an **Artist**.
- A Song always belongs to an **Album** or **Singles** album.
- and a **Lyrics** always belongs to a **Song**.
- A **Song** belongs to a **Language**

## Other Features

- An Admin can CRUD an **Artist, Album, Song, Lyrics** and every model using django admin
- A user can then create his own **Playlist**.
- A user can then add a **Song** to his **favorites** folder.
- A user can also write a **comment** on an Album or a Song.
- 


This text you see here is *actually- written in Markdown! To get a feel
for Markdown's syntax, type some text into the left window and
watch the results in the right.

## Technologies used in this project
- Python 3
- Html & CSS
- Javascript + JQuery
- Bootstrap


## Installation

After cloning this project, open the folder with manage.py in it.
then open CMD and run

```sh
python manage.py runserver
```

is the only command you need to run as the folder already contains a sqlite database file.

