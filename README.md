This is a simple tool to convert audio files to mp3 format.

It will recrusively process the source directory and its
sub-directory and convert the audio files to mp3 format, 
and the mp3 files will be saved at your specified destination
directories, using the same directory structure as your
source directory.

I simply made it to suit my own particular one-time need, so
the featuer of this tool is very limited, and I only tested
converting wma files to mp3 files. But I thought it could be
useful to other people as well, you just need to customize it
to fit your own need.

If it is not working for the format you want to convert, 
you should take a look at `convert_one_file(...)` function,
looking at the following line. Customize it to make it open the 
audio file type you want.

```Use Python
def convert_one_file(src, dest_dir, check_dir, log=False):
    ...
                audio = AudioSegment.from_file(src)

```
## Requirements

* You need to have `ffmpeg` available in %PATH%.
* You need to have mutagen. To install it, run: `python -m pip install mutagen`
* You need to have pydub. To install it, run: `python -m pip install pydub`

## Usage

```
usage: convert_to_mp3.py [-h] [-o dest_dir] [-s SRC_DIR [SRC_DIR ...]]
                         [-f SRC_FILE [SRC_FILE ...]] [-l LOG]

optional arguments:
  -h, --help            show this help message and exit
  -o dest_dir, --dest-dir dest_dir
                        Destination directory
  -s SRC_DIR [SRC_DIR ...], --src-dirs SRC_DIR [SRC_DIR ...]
                        List of directories containing audio files to be
                        converted to MP3
  -f SRC_FILE [SRC_FILE ...], --src-files SRC_FILE [SRC_FILE ...]
                        List of audio files to be converted to MP3
  -l LOG, --log LOG     Whether to log each converted file
```

Example:
```
convert_to_mp3.py -o D:\output_dir -s C:\my_music
```