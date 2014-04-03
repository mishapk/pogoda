#!/usr/bin/env python
#-*- coding: utf-8 -*-
import ftplib
import re
import os
import sys
import lxml.html

IP="192.168.1.101"
path="/root/spark/directfb-ui"
filename="startpage.html"
rtext="http://sinoptik.ua/погода-кривой-рог/10-дней"
#rtext="http://yandex.ru"

#download file
ftp=ftplib.FTP(IP)
ftp.login("root","root")
ftp.cwd(path)

print "start download file: %s%s%s" %(IP,path,filename)
try:
	ftp.retrbinary("RETR " +filename,open(filename,"wb").write)
	print "Download OK!"
except:
	print "Error Download!"
	os.remove(filename)
	sys.exit()


#Find and replise
try:
	os.rename(filename,filename +".bak")
except:
	print "Error Rename File"
	sys.exit()

data = open(filename+".bak").read()
doc = lxml.html.document_fromstring(data)

for item in doc.xpath("//script"):
	ftext= item.text
ftext= ftext[ftext.find("'")+1:ftext.rfind("'")]	
print "Replace text:"
print ftext
print "to:"
print rtext

#ftext = ftext.decode("UTF-8")
if type(ftext)==unicode:
	data = data.decode("UTF-8")
	rtext = rtext.decode("UTF-8")
print "data: ",type(data)
print "ftext: ",type(ftext), ftext
print "rtext: ",type(rtext), rtext
if type(ftext)==unicode:
	ntext = data.replace(ftext,ftext)
else:
	ntext = re.sub(ftext,rtext,data)
print "ntext: ",type(ntext)
file_w = open(filename, 'w')
file_w.write( ntext )
file_w.close()

#upload file back

def progress():
    def callback(block):
        callback.uploaded += len(block)
        print('Uploaded %d bytes' % callback.uploaded)
    callback.uploaded = 0
    return callback
try:
	ftp.storbinary("STOR " + filename, open(filename, "rb"), 1024, progress())
	print "uploadfile ok"
except:
	print "Error Upload!"

ftp.quit()
print "----------------------"
#-------------------------------------------------------------------------------------


	
	



