# app.py
from flask import Flask, render_template, request, send_file, flash, redirect, url_for
import os
import cv2
import re
import requests
import io
import base64
import shutil
import time
from requests.exceptions import RequestException, SSLError
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
app = Flask(__name__)
def drawRectangle(filename,li):
    image = cv2.imread(filename)
    if(len(li)>0):
        for x in li:
            boundingBox=x["boundingBox"]
            print(boundingBox)
            cal=int(boundingBox[6])+(int((int(boundingBox[2])-int(boundingBox[6]))/3)*2)
            start_point = (int(boundingBox[6]),int(boundingBox[7]))
            end_point = (cal,int(boundingBox[3]))
            

            print(start_point)
            print(end_point)

            color = (0, 0, 0)
            thickness = -1
            image = cv2.rectangle(image, start_point, end_point, color, thickness)
        # cv2.imwrite("masked_images"+"\\"+filename, image)
        filename=filename.split("\\")[-1]
        print(destination_path+"\\"+filename)
        cv2.imwrite(destination_path+"\\"+filename, image)
    else:
        shutil.copy(filename,nonMasked)
    
def getText(source_path,returnflag):
    try:
        with open(source_path, 'rb') as f:
            data = f.read()
        headers = {
            'Ocp-Apim-Subscription-Key': '7c8fbff85843414185d62ebdf01c8f1d',
            'Content-Type': 'application/octet-stream',
        }
        # data = "{'url':'https://learn.microsoft.com/azure/cognitive-services/computer-vision/media/quickstarts/presentation.png'}"
        response = requests.post(
            'https://computer-ocr-vision.cognitiveservices.azure.com/computervision/imageanalysis:analyze?features=tags,read&model-version=latest&language=en&api-version=2023-02-01-preview',
            headers=headers,
            data=data,
            verify=False,
        )
        r=response.json()
        # print(r)
        text=((((r["readResult"])["pages"])[0])["lines"])
        angle=((((r["readResult"])["pages"])[0])["angle"])
        # print(text)
        if(abs(angle)>30):
            print("ANGLE: "+str(angle))
            shutil.copy(source_path,rotated)
            return 1
        else:
            li=[]
            for x in text:
                p=re.findall('\d{4} \d{4} \d{4}', x["content"])
                if(len(p)>0):
                    li.append(x)
            drawRectangle(source_path,li)
            return 0
    except RequestException as req_ex:
        if isinstance(req_ex, SSLError):
            print("SSL Error:", req_ex)
            shutil.copy(source_path, dump)
        else:
            print("Request Exception:", req_ex)
            shutil.copy(source_path,dump)
        return returnflag+1
    except Exception as e:
        print(e)
        shutil.copy(source_path,dump)
        return 1

source_dir=r"C:\Users\32020\Pictures\Camera Roll"
destination_path=r"D:\Masking Utility\dest"
nonMasked=r"D:\Masking Utility\non aadhaar"
dump=r"D:\Masking Utility\error"
rotated=r"D:\Masking Utility\rotated"
count=0
x=0
for folder, subfolders, files in os.walk(source_dir):
    for file in files:
        # pNo=folder.split("\\")[-1]
        # x=file.split(".")[0]+"_"+pNo+"."+file.split(".")[-1]
        filee = os.path.join(folder, file)
        print(file)
        # if(pNo not in file):
        #     orginalfile= os.path.join(folder, file)
        #     x=file.split(".")[0]+"_"+pNo+"."+file.split(".")[-1]
        #     file = os.path.join(folder, x)
        #     print(orginalfile)
        #     os.rename(orginalfile,file)
        count+=1
        if(file in os.listdir(destination_path) or file in os.listdir(dump)):
            print(str(count)+". "+file+"-->Already processed")
        elif(file in os.listdir(nonMasked)):
            print(str(count)+". "+file+"-->Already processed")
        elif(file in os.listdir(rotated)):
            print(str(count)+". "+file+"-->Already processed")
            
        else:
            
            if(x!=4):
                print(str(count)+". "+filee+"-->Masking in progress")
                x=getText(filee,x)
            else:
                print("Wait for 5 mins...")
                x=0
                time.sleep(300)  
