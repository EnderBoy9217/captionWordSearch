### Imports

import requests
import os
from bs4 import BeautifulSoup
from pytube import Playlist
from youtube_transcript_api import YouTubeTranscriptApi

### Video Functions

def getVideoTitle(videoUrl: str) -> str:
    # Send a GET request to the video URL
    response = requests.get(videoUrl)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the title in the <title> tag
        title_tag = soup.find('title')
        
        if title_tag:
            return title_tag.text.strip()  # The title is in the <title> tag
        else:
            return "Title not found"
    else:
        return f"Error: {response.status_code}"


def getTranscript(videoId: str) -> str:
    try:
        # Retrieve the transcript
        transcript = YouTubeTranscriptApi.get_transcript(videoId)
        
        # Convert transcript to a single string
        transcript_text = " ".join([entry['text'] for entry in transcript])
        return transcript_text
    except Exception as e:
        return f"An error occurred: {e}"
    

### User Inputs

def getPlaylist() -> Playlist:
    playlistLink = input("Enter Playlist Link: ")
    playlist = Playlist(playlistLink)
    try:
        print( f"Getting Videos from: {playlist.title}\n" )
    except Exception as e:
        print( "Error: Unable to find Playlist." )
        return getPlaylist()
    return playlist

def getWordList() -> list:
    wordList = []

    while True: # I hate this but it works and no edge cases so why not
        response = input("Enter a word to search for or \"$\" to finish: ")

        if (response == "$"):
            break
        wordList.append(response)

    if ( len(wordList) > 0 ):
        return wordList
    else:
        print("You must enter at least one word!")
        return getWordList()

def getWriteInput() -> bool:
    inWrite = input("Should the results be written to a file? (Y/N): ")
    if (inWrite.upper() == "Y" ):
        return True
    elif (inWrite.upper() == "N"):
        return False
    else:
        return getWriteInput()
    
def getPathInput() -> str:
    filePath = input("Please enter the file path: ")

    # Check if the path's directory exists
    directory = os.path.dirname(filePath)

    if not os.path.exists(directory):
        print(f"Error: The directory '{directory}' does not exist.")
        return getPathInput()
    else:
        try:
            # Try opening the file to create/overwrite it
            with open(filePath, 'w') as file:
                file.write("")  # Write empty content
            print("Valid Path!")
            return filePath
        except Exception as e:
            print(f"Error: Could not create or overwrite the file. Details: {e}")
            return getPathInput()
    
def writeToFile(filePath: str, playlist: Playlist, wordList: list) -> None:
    with open(filePath, "w", encoding="utf-8") as file:
        file.write("# Playlist Word Analysis\n\n")

        file.write(f"Getting Videos from: {playlist.title}\n\n")
        #print(f"Getting Videos from: {playlist.title}\n\n") # Already printed

        totalCounts = [0] * len(wordList)

        for videoIndex, video in enumerate(playlist.videos):
            title = getVideoTitle(video.watch_url)
            didPrint = False
            file.write(f"\n{title}:\n")
            transcript = getTranscript(video.video_id).lower()
            videoCounts = [0] * len(wordList)
            for index, word in enumerate(wordList):
                videoCounts[index] += transcript.count(word.lower())
                totalCounts[index] += transcript.count(word.lower())
                if videoCounts[index] != 0:
                    file.write(f"{word} appears {videoCounts[index]} times\n")
                    didPrint = True
            if not didPrint:
                file.write("No keywords found\n")
            print(f"\nCompleted Video #{videoIndex+1} of {str(len(playlist.videos))}: {title}\n")

        file.write("\nTotal Counts:\n\n")
        for index, word in enumerate(wordList):
            file.write(f"{word} appears {totalCounts[index]} times\n")

    print("Saved to wordAnalysis.txt")

def onlyPrint( playlist: Playlist, wordList: list ) -> None:
    print("# Playlist Word Analysis\n\n")

    totalCounts = [0] * len(wordList)

    for videoIndex, video in enumerate(playlist.videos):
        title = getVideoTitle(video.watch_url)
        didPrint = False
        print(f"{title}:\n")
        transcript = getTranscript(video.video_id).lower()
        videoCounts = [0] * len(wordList)
        for index, word in enumerate(wordList):
            videoCounts[index] += transcript.count(word.lower())
            totalCounts[index] += transcript.count(word.lower())
            if videoCounts[index] != 0:
                print(f"{word} appears {videoCounts[index]} times")
                didPrint = True
        if not didPrint:
            print("No keywords found\n")
        print(f"\nCompleted Video {videoIndex+1} of {str(len(playlist.videos))}: {title}\n")

    print("\nTotal Counts:\n")
    for index, word in enumerate(wordList):
        print(f"{word} appears {totalCounts[index]} times")

    print("\nOperation Complete")

def main():
    
    playlist = getPlaylist()
    wordList = getWordList()
    shouldWrite = getWriteInput()

    if (shouldWrite):
        filePath = getPathInput()
        writeToFile( filePath, playlist, wordList )
    else:
        onlyPrint( playlist, wordList )

    return

main()
