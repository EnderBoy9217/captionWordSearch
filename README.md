# YouTube Playlist Word Analysis Tool

## Overview
This program analyzes YouTube video transcripts within a given playlist to count occurrences of user-specified words. The results can be printed to the console or saved to a file.

## Features
- Retrieves the titles of videos in a YouTube playlist.
- Fetches transcripts of videos (if available).
- Searches transcripts for user-defined words.
- Displays the word count for each video and totals across the playlist.
- Optionally saves the results to a file.

## Dependencies
The program requires the following Python libraries:
- `requests`
- `os`
- `BeautifulSoup` (from `bs4`)
- `pytube` (for playlist processing)
- `youtube_transcript_api`

Ensure these dependencies are installed before running the program.


## Usage
1. Run the script.
2. Enter a YouTube playlist URL.
3. Enter words to search for in video transcripts.
4. Choose whether to save results to a file.
5. If saving, enter a valid file path.
6. The program will process the playlist and display/save the results.

## Example Output
```
# Playlist Word Analysis

Getting Videos from: Sample Playlist

Video Title 1:
word1 appears 3 times
word2 appears 5 times

Video Title 2:
No keywords found

Total Counts:
word1 appears 3 times
word2 appears 5 times
```

## Notes
- If a transcript is unavailable for a video, it is skipped.
- The program converts all text to lowercase to ensure case-insensitive word matching.

## Functions

### `getVideoTitle(videoUrl: str) -> str`
Fetches the title of a YouTube video by sending a request to the video's URL and parsing the page title.

### `getTranscript(videoId: str) -> str`
Retrieves the transcript of a video using the `youtube_transcript_api` library and returns it as a string. If the transcript is unavailable, an error message is returned.

### `getPlaylist() -> Playlist`
Prompts the user to enter a YouTube playlist URL, retrieves the playlist, and returns a `Playlist` object. If retrieval fails, the user is prompted again.

### `getWordList() -> list`
Prompts the user to input words to search for in video transcripts. Users enter words one by one and type `$` to finish. At least one word is required.

### `getWriteInput() -> bool`
Asks the user whether to save the results to a file. Returns `True` if the user selects Yes (`Y`), otherwise returns `False`.

### `getPathInput() -> str`
Prompts the user for a file path to save the results. Verifies the directory exists and attempts to create or overwrite the file before returning the validated path.

### `writeToFile(filePath: str, playlist: Playlist, wordList: list) -> None`
Writes the word analysis results to the specified file, including:
- Playlist title
- Video titles
- Word occurrences per video
- Total occurrences across all videos

### `onlyPrint(playlist: Playlist, wordList: list) -> None`
Displays the word analysis results in the console instead of writing to a file.

### `main()`
Coordinates user input and calls appropriate functions. Determines whether to print results or write them to a file.
