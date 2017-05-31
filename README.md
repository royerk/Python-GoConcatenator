# Python-GoConcatenator
Python script to concatenate go files into a single file.

On several AI platform you need to upload code in a single file. This is a simple script that concatenate all go files from a repository into a single file:
- imports are handled
- the file with the *main()* method will appear first in the final file
- it only handles single package project (`package main`)

No library required.

## How to
You can run the script with `python3 Go_concatenator.py path/to/file/ path/output file_name` or just `python3 Go_concatenator.py` after editing paths in the script (somewhere at the end).

## Codingame
I use this script mainly for [Codingame](codingames.com) challenges. This platform has an integrated IDE, to copy paste my code quickly I am using [xsel](https://linux.die.net/man/1/xsel) to copy the code to the clipbloard.

Install xsel: `sudo apt-get install xsel`

Run the script + copy to clipbloard: `python3 Go_concatenator.py | xsel -b` (*-b* copies to the clipboard), and then ctrl-V in the IDE.

After pasting the text you will have a blank line between each line of code, I haven't looked into that yet.
