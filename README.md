# Back-Beat

## Installation and Usage
Download the latest version of Back-Beat: https://github.com/LarsZauberer/Back-Beat/releases
<br>
Unzip the file and start the init.bat file.
Now you can use the other files to create or restore backups

## main.py
Recreated the script with modules/functions and command line arguments
Usage is shown with the '--help' parameter.

``` bash
usage: main.py [-h] [-i {1} [{1} ...]] [-o] [-p] [-d] [-l] [-v] [--version]

Backup Beat Saber

optional arguments:
  -h, --help            show this help message and exit
  -i {1} [{1} ...], --importtype {1} [{1} ...]
                        Typ of backup
  -o, --out, --push     create a new backup
  -p, --pull            restore from a backup
  -d, --debug           activate debug
  --version             show program version number and exit
```
Thanks for using this backup tool
