import os
import sys
import shutil
import datetime

source = "C:\\Data\\Bitbucket\\Test1"
destination = "C:\\Data\\Bitbucket\\Test2"
dt = str(datetime.datetime.now().strftime("%Y%m%d%H%M"))
target = destination + "\\" + dt
print(f"Copy files from {source} to {target}")
try:
  shutil.copytree(source, target)
except OSError as e:
  print("Error while trying to copy files")
  print(f"Windows {e.winerror} Error:\t{e.strerror}")
  print(f"File1:\t{e.filename}\nFile2:\t{e.filename2}")
