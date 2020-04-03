import os
import sys
import shutil
import datetime
import pickle

try:
    with open("config.txt", 'r') as f:
        content = f.read()
        beat_saber_loc = content.split(", ")[0]
        backup_loc = content.split(", ")[1]
except:
    print("Can't open config file")

if not os.path.exists(backup_loc):
    os.mkdir(backup_loc)

try:
    with open(backup_loc+"\\backups.txt", 'rb') as f:
        dates = pickle.load(f)
except:
    with open(backup_loc+"\\backups.txt", 'wb') as f:
        dates = []

BE = input("Push/Pull: ")
if BE == "Push":
    backup_count = []
    for i in dates:
        if str(datetime.date.today()) in i:
            backup_count.append(i)
    shutil.copytree(beat_saber_loc, backup_loc+"\\"+ str(datetime.date.today()) + "_" + str(int(len(backup_count)+1)))
    dates.append(str(datetime.date.today()) + "_" + str(int(len(backup_count)+1)))
elif BE == "Pull":
    for i in dates:
        print (i)
    date = input("Which one do you like to pull from: ")
    if date in dates:
        if os.path.exists(beat_saber_loc):
            shutil.rmtree(beat_saber_loc)
        shutil.copytree(backup_loc+"\\"+date, beat_saber_loc)
    else:
        print("Invalid Date")

with open(backup_loc+"\\backups.txt", 'wb') as f:
    pickle.dump(dates, f)
