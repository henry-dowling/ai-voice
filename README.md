# How to run

## Setup services

Create a pg db wherever you like, and grab an openai api key

Your .env should look like

```
OPENAI_API_KEY=
PGDATABASE=
PGUSER=
PGPASSWORD=
PGHOST=
PGPORT=
```

## setup your corpus

Dump a bunch of text files of your own writing samples that you like into /corpus

**choosing what files to upload is the most important determinant of how well this will work**

run add_to_rag.py; this will clean, embed, and write your the resultant vectors (including text) to the db

## Use it
1. Upload something you're writing to to_edit
2. run compose.py and ask it to write something. Longer outlines are better






