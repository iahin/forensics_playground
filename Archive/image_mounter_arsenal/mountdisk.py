import os

image = ".\\Slade-B1-hda.img"
arsenalmount = ".\\tools\\Arsenal-Image-Mounter\\aim_cli.exe"
os.system(arsenalmount + " /mount /filename=" + image)
