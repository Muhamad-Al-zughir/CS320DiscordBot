# Discord Bot

## Members:
    - Muhamad Al-zughir
    - Joe Hernandez
    - Alex Kochenkov
    - Shawyan Tabari
    - Judah Tanninen
    

## Description
Custom discord bot, features and functionalities to be determined as the project continues

## Possible Features
    - API connection with libgen
    - API connection with openai GPT3

## Procedure for making code changes
    - Make sure you have no code changes on your current branch
        - If you do, commit it or remove it with git reset --hard HEAD
    - run a git fetch --all
    - If editing a branch:
        - git checkout <branchname> (should be dbot_n)
        - git merge origin/main (will bring in the most recent changes from main)
    - Creating a new branch:
        - Copy the id of the trello card (the number in the url)
        - run the following "git checkout -b <branchname> (dbot_{the number}) origin/main"
        - This will create a new branch, based on the most recent changes in main

    - During development, add and commit code frequently, with decent commit messages
    - When you are done, or just wish to see your code in github, do the following:
        - Make sure all your code is commited
        - git push origin <branchname>
        - In github, go to the "pull request" tab - and create a new pull request, making the PR name the branch name
    - Code will then be reviewed by team members, tested, and merged into main if it is considered good.

## Installers
```
(Make sure python 3 has been installed and is in PATH)
apt install python3-pip
apt install python-dotenv
pip install libgen-api
pip install youtube-dl
pip install PyNaCl
pip install ffmpeg
pip install spotipy
pip install apscheduler
pip install lyricsgenius
pip install pydub
pip install selenium
pip install Pillow
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
pip install discord.py
```

## FFMPEG Installation Notes
```
pip install 
import module
download ffmpeg-git.full.7z from https://www.gyan.dev/ffmpeg/builds/
Extract or unzip folder
add Extracted Folder\ffpmeg\bin to PATH
```

