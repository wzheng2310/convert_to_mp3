#!"c:\Python\Python37\python.exe"

import mimetypes
import platform
import os
import shutil
import sys

from argparse import ArgumentParser
from mutagen.mp3 import EasyMP3
from mutagen.asf import ASF
from pydub import AudioSegment

print('Using Python ' + platform.python_version())


def is_audio(src):
    types = mimetypes.guess_type(src)[0]
    if types is not None:
        return types.split('/')[0] == 'audio'
        # possible media type values: 'audio', 'video', 'image'

def get_asf_tag(asf_src, tag_name):
    try:
        return [asf_src.tags[tag_name][0].__str__()]
    except:
        return []

def copy_tags(src, dest):
    default_album_name = None
    path_comps =  src.split(os.path.sep)
    if len(path_comps) >= 2:
        default_album_name = path_comps[-2]

    audio_src = ASF(src)
    audio_dest = EasyMP3(dest)
    audio_dest['title'] = get_asf_tag(audio_src, 'Title')
    audio_dest['artist'] = get_asf_tag(audio_src, 'Author')
    audio_dest['albumartist'] = get_asf_tag(audio_src, 'WM/AlbumArtist')
    if not audio_dest['albumartist']:
        audio_dest['albumartist'] = audio_dest['artist']
    audio_dest['album'] = get_asf_tag(audio_src, 'WM/AlbumTitle')
    if not audio_dest['album']:
        audio_dest['album'] = default_album_name
    audio_dest['date'] = get_asf_tag(audio_src, 'WM/Year')
    audio_dest['composer'] = get_asf_tag(audio_src, 'WM/Composer')
    audio_dest['genre'] = get_asf_tag(audio_src, 'WM/Genre')
    audio_dest['tracknumber'] = get_asf_tag(audio_src, 'WM/TrackNumber')

    audio_dest.save()

def convert_one_file(src, dest_dir, check_dir, log=False):
    try:
        if check_dir and not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        
        fullname = src.split(os.path.sep)[-1]
        idx = fullname.rindex('.')
        name = fullname[0:idx]
        ext = fullname[idx + 1:]

        dest_file = os.path.join(dest_dir, name + '.mp3')
        if os.path.exists(dest_file):
            if log:
                print('"%s" is already converted' % src)
            return

        if ext.lower() == 'mp3':
            if log:
                print('Copying to %s' % dest_file)
            shutil.copy(src, dest_file)
            if log:
                print('Done')
        else:
            if log:
                print('Converting %s to %s' % (src, dest_file))
            audio = AudioSegment.from_file(src)
            audio.export(dest_file, format='mp3', bitrate='320k')
            copy_tags(src, dest_file)

            if log:
                print('Done')
    except ValueError as ve:
        print(ve)

def convert_one_dir(src_dir, dest_dir, log=False):
    print("Working on directory %s ..." % src_dir)
    check_dir = True
    for entry in os.listdir(src_dir):
        src_path = os.path.join(src_dir, entry)
        if os.path.isfile(src_path):
            if not is_audio(src_path):
                continue
            convert_one_file(src_path, dest_dir, check_dir, log)
            check_dir = False
        else:
            convert_one_dir(os.path.join(src_dir, entry), os.path.join(dest_dir, entry), log)

if __name__ == "__main__":
    #parser = ArgumentParser(os.path.basename(__file__))
    parser = ArgumentParser(os.path.basename(sys.argv[0]))
    parser.add_argument('-o', '--dest-dir',
                        dest='dest_dir',
                        metavar="dest_dir",
                        help='Destination directory')
    parser.add_argument('-s', '--src-dirs',
                        dest='src_dirs',
                        nargs='+',
                        metavar="SRC_DIR",
                        help='List of directories containing audio files '
                          'to be converted to MP3')
    parser.add_argument('-f', '--src-files',
                        dest='src_files',
                        nargs='+',
                        metavar="SRC_FILE",
                        help='List of audio files to be converted to MP3')
    parser.add_argument('-l', '--log',
                        dest='log',
                        type=bool,
                        default=False,
                        help='Whether to log each converted file')

    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    if args.src_dirs is None and args.src_files is None or args.dest_dir is None:
        parser.print_help()
        sys.exit(0)

    mimetypes.init()

    check_dir = True
    if args.src_files != None:
        for f in args.src_files:
            convert_one_file(f, args.dest_dir, check_dir, args.log)
            check_dir = False

    if args.src_dirs != None:
        for d in args.src_dirs:
            convert_one_dir(d, args.dest_dir, args.log)
