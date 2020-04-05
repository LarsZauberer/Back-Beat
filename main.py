import os
import sys
import shutil
import datetime
import json
import argparse
from pathlib import Path


def read_config() -> dict:
    """
    read_config
    Read the JSON config file.

    Returns:
        dict: dictionary object of the config settings
    """
    configInfo = {}
    try:
        with open("config.json", 'r') as readFile:
            data = json.load(readFile)
    except Exception:
        print("Can't open config file")
        sys.exit()
    finally:
        configInfo = data
        return configInfo


def write_config(path1: str, path2: str) -> None:
    """
    write_config
    Write to the config file the configuration settings. Paths and Backuplist.

    Args:
        path1 (string): Beat Saber Path
        path2 (string): Path to Backuplocation
    """
    configInfo = {}
    configInfo['beatSaberPath'] = path1
    configInfo['backupPath'] = path2
    configInfo['backups'] = findOldBackups(path2)
    with open("config.json", "w") as writeFile:
        json.dump(configInfo, writeFile)


def verify_backup_path(backupPath: str) -> None:
    """
    verify_backup_path
    Verifies that the path to backup location exists and if not creates it.

    Args:
        backupPath (string): Path to Backuplocation
    """
    if not os.path.exists(backupPath):
        os.mkdir(backupPath)


def findOldBackups(backupPath: str) -> dict:
    """
    findOldBackups
    Look up for existing folders in the Backuplocation

    Args:
        backupPath (string): Path to Backuplocation

    Returns:
        dict: dictionary listing of existing Backups
    """
    backupList = {}
    # List all subdirectory using pathlib
    basepath = Path(backupPath + "/")
    i = 0
    for entry in basepath.iterdir():
        if entry.is_dir():
            i += 1
            folderName = backupPath + "/" + entry.name
            backupList[str(i)] = folderName
    return backupList


def copyFolders(source: str, destination: str) -> None:
    """
    copyFolders
    Filelevel copy from the Source directory to the Destination directory

    Args:
        source (string): Source directory path
        destination (string): Destination directory path
    """
    print(f"Copy files from {source} to {destination}")
    try:
        shutil.copytree(source, destination)
    except OSError as e:
        print("Error while trying to copy files")
        print(f"Windows {e.winerror} Error:\t{e.strerror}")
        print(f"File1:\t{e.filename}\nFile2:\t{e.filename2}")
    return None


def push() -> None:
    """
    push
    Creates a backup for Beat Saber in the configured location with the actual date

    Returns:
        None: -
    """
    print("Startin PUSH")
    backup_count = 0
    cfg = read_config()
    source = cfg['beatSaberPath']
    destination = cfg['backupPath']
    dt = str(datetime.datetime.now().strftime("%Y%m%d%H%M"))
    target = destination + "/" + dt
    copyFolders(source, target)
    backups = findOldBackups(destination)
    backup_count = len(backups)
    print(f"You have now {backup_count} backups.")
    write_config(source, destination)
    return None


def pull() -> None:
    """
    pull
    Restore a selected backup for Beat Saber

    Returns:
        None: -
    """
    print("Startin PULL")
    backup_count = 0
    cfg = read_config()
    beat_saber_loc = cfg['beatSaberPath']
    backup_loc = cfg['backupPath']
    backups = findOldBackups(backup_loc)
    backup_count = len(backups)
    while backup_count > 0:
        for entry in backups:
            print(f"{entry}\t{backups[entry]}")
        try:
            selection = int(input("Which one do you like to pull from (select number 1-x) or 0 for exit: "))
        except Exception:
            print("Invalid selection, please numbers only")
            sys.exit()
        if selection <= backup_count:
            if os.path.exists(beat_saber_loc):
                shutil.rmtree(beat_saber_loc)
            source = backups[selection]
            shutil.copytree(source, beat_saber_loc)
            print("Restore successfull")
            backup_count = 0
        elif selection == 0:
            sys.exit()
        else:
            print("Invalid selection, please only listed numbers")
    write_config(beat_saber_loc, backup_loc)
    return None


def main() -> None:
    """
    main
    Program to pars the parameters and run it through
    """
    # Parsing parameters
    parser = argparse.ArgumentParser(description='Backup Beat Saber',
                                     epilog='Thanks for using this backup tool')
    parser.version = '1.1'
    parser.add_argument('-i', '--importtype', dest='importtype', type=int,
                        action='append', nargs='+', choices=range(1, 2),
                        help='Typ of backup')
    parser.add_argument('-o', '--out', '--push', dest='importtype',
                        action='append_const', const=1,
                        help='create a new backup')
    parser.add_argument('-p', '--pull', dest='importtype',
                        action='append_const', const=2,
                        help='restore from a backup')
    parser.add_argument('-d', '--debug', action='store_true', help='activate debug')
    parser.add_argument('-l', '--log', action='store_true', help='activate logging')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='logging and debug is activated')
    parser.add_argument('--version', action='version')
    args = parser.parse_args()
    # checking the logging options
    """ if args.debug:
        DEBUG = True
        print("Commandline switches Debugging ON")
    if args.log:
        LOG = True
        print("Commandline switches Logging ON")
    if args.verbose:
        DEBUG = True
        LOG = True
        print("Commandline switches Logging and Debugging ON") """
    # Doing the actual work
    for task in args.importtype:
        dispatch[task]()
    return None


# Variable definition
task = 0
dispatch = {
    1: push,
    2: pull
}

# Here start the real code for this program to run
time_start = datetime.datetime.now()
print(f'===== START ===== [{time_start}]')
try:
    main()
except SystemExit:
    print("")
except KeyError:
    print("")
except Exception:
    txt = "An Error occurred!\n"
    txt += str(sys.exc_info()[0])
    txt += "\nDetails:\n"
    txt += str(sys.exc_info()[2])
    print(txt)
finally:
    time_end = datetime.datetime.now()
    print(f'===== STOP ===== [{time_end}]')
    duration = time_end - time_start
    print(f'Duration = [{duration}]')
