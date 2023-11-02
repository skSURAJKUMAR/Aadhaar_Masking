""" All Package imports"""
from asyncio.windows_events import NULL
import shutil
import os
import cv2
from PIL import Image
import pytesseract;
import numpy;
import cv2
import numpy as np
import matplotlib.pyplot as plt
import regex as re
from PIL import Image
import pytesseract as ocr
from ISR.models import RRDN
import pdf2image
import img2pdf
from PyPDF2 import PdfFileWriter, PdfFileReader,PdfFileMerger
from pdf2image import convert_from_path
import tifftools
import PIL.Image
PIL.Image.MAX_IMAGE_PIXELS = 933120000
pytesseract.pytesseract.tesseract_cmd =r'C:\Program Files\Tesseract-OCR\tesseract.exe'
Suraj = []
counter=0
def total_pages(file):
  img = Image.open(file)
  return img.n_frames
def find_text(text):
  n=len(text);
  if(n<12):
    return 0;
  for i in range(14,n):
    s=text[i-14:i];
    if(s[4]==" " and s[9]==" "):
      s=s.replace(" ","");
      n1=len(s);
      s1=s[n1-12:n1];
      if(i==125):
        pass;
      if(s1.isnumeric() and len(s1)>=12):
        return 1;
  return 0;
#-------------------------------------------------------------------------------------------------------#
def addhar_check(file_name):
  img = Image.open(file_name)
  u=0;
  for i in range(25):
    try:
        img.seek(i)
        u=u+1;
        array=numpy.array(img);
        # print(array)
        # print(array.shape)
        # print(type(array.shape))
        c=len(array.shape);
        if(c==2):
          if(array[0][0]==True or array[0][0]==False):
             array=array*255;
             img10 = array.astype(numpy.uint8)
             array=numpy.array(img10)

        elif(c==3):
          if(array[0][0][0]==True or array[0][0][0]==False):
             array=array*255;
             img10 = array.astype(numpy.uint8)
             array=numpy.array(img10)     
        text=pytesseract.image_to_string(array);
        v=find_text(text);
        if(v):
                break;
        else:
                gaussianBlur = cv2.GaussianBlur(array,(5,5),cv2.BORDER_DEFAULT)
                text=pytesseract.image_to_string(gaussianBlur);
                v=find_text(text);
                if(v):
                    break;
                else:
                    pass;
    except EOFError:
        u=0;
        break
  return u;


#addhar_check("/content/pdf2img.jpg")
#----------------------------------------------------------------------------------------------------#
def mergeAll(x,y):
    merger = PdfFileMerger()
    for pdf in x:
        merger.append(pdf)
    merger.write(y)
    merger.close()

#----------------------------------------------------------------------------------------------------#

"""Remove the unmasked aadhar page from a pdf file and add a new page of masked aadhar into the pdf file."""
def merger(original,masked,page_no,flag):
  infile = PdfFileReader(original)
  x=infile.getNumPages()
  output = PdfFileWriter()

  for i in range(x):
    if(i!=page_no):
      p = infile.getPage(i)
      output.addPage(p)

  with open('newfile.pdf', 'wb') as f:
    output.write(f)
  merger = PdfFileMerger()
  merger.append('newfile.pdf')
  merger.append(masked)
  merger.write("result.pdf")
  merger.close()
  if(flag==1):
    pdf2tiff("result.pdf")

"""Split a pdf into multiple pages and merge them all to a single TIF file."""
def pdf2tiff(pdf_path):
# Store Pdf with convert_from_path function
  images = pdf2image.convert_from_path(pdf_path,300,poppler_path=r'C:\Program Files\poppler-0.68.0\bin')
  #images.save('gg'+'.tif','TIFF')
  li=[] 
  for i in range(len(images)):
        # Save pages as images in the pdf
      images[i].save(str(i)+".tif", 'TIFF')
      li.append(str(i)+'.tif')
  tifftools.tiff_merge(li,'final.tif')

multiplication_table = (
    (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
    (1, 2, 3, 4, 0, 6, 7, 8, 9, 5),
    (2, 3, 4, 0, 1, 7, 8, 9, 5, 6),
    (3, 4, 0, 1, 2, 8, 9, 5, 6, 7),
    (4, 0, 1, 2, 3, 9, 5, 6, 7, 8),
    (5, 9, 8, 7, 6, 0, 4, 3, 2, 1),
    (6, 5, 9, 8, 7, 1, 0, 4, 3, 2),
    (7, 6, 5, 9, 8, 2, 1, 0, 4, 3),
    (8, 7, 6, 5, 9, 3, 2, 1, 0, 4),
    (9, 8, 7, 6, 5, 4, 3, 2, 1, 0))

permutation_table = (
    (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
    (1, 5, 7, 6, 2, 8, 3, 0, 9, 4),
    (5, 8, 0, 3, 7, 9, 6, 1, 4, 2),
    (8, 9, 1, 6, 0, 4, 3, 5, 2, 7),
    (9, 4, 5, 3, 1, 2, 6, 8, 7, 0),
    (4, 2, 8, 6, 5, 7, 3, 9, 0, 1),
    (2, 7, 9, 3, 8, 0, 6, 4, 1, 5),
    (7, 0, 4, 6, 9, 1, 3, 2, 5, 8))

#---------------------------------------------------------------------------------------------------------#

def compute_checksum(number):
    
    """Calculate the Verhoeff checksum over the provided number. The checksum
    is returned as an int. Valid numbers should have a checksum of 0."""
    
    # transform number list
    number = tuple(int(n) for n in reversed(str(number)))
    #print(number)
    
    # calculate checksum
    checksum = 0
    
    for i, n in enumerate(number):
        checksum = multiplication_table[checksum][permutation_table[i % 8][n]]
    
    #print(checksum)
    return checksum

#---------------------------------------------------------------------------------------------------------#

# Search Possible UIDs with Bounding Boxes

def Regex_Search(bounding_boxes):
  possible_UIDs =[] 
  Result = ""

  for character in range(len(bounding_boxes)):
    if len(bounding_boxes[character])!=0:
      Result += bounding_boxes[character][0]
    else:
      Result += '?'

  print(Result)
  # file1 = open("Errorreport.txt", "a")  # append mode
  # file1.write(f+":\n"+Result+"\n")
  # file1.close()

  matches = [match.span() for match in re.finditer(r'\d{12}',Result,overlapped=True)]

  #print(matches)

  for match in matches :

    UID = int(Result[match[0]:match[1]])
    print(UID)
    
    if compute_checksum(UID)==0 and UID%10000!=1947:
       possible_UIDs.append([UID,match[0]])

  possible_UIDs = np.array(possible_UIDs)
  return possible_UIDs

#---------------------------------------------------------------------------------------------------------#

def Mask_UIDs (image_path,possible_UIDs,bounding_boxes,rtype,SR=False,SR_Ratio=[1,1]):

  img = cv2.imread(image_path)

  if rtype==2:
    img = cv2.rotate(img,cv2.ROTATE_90_COUNTERCLOCKWISE)
  elif rtype==3:
    img = cv2.rotate(img,cv2.ROTATE_180)
  elif rtype==4:
    img = cv2.rotate(img,cv2.ROTATE_90_CLOCKWISE)

  height = img.shape[0]

  if SR==True:
    height*=SR_Ratio[1]

  for UID in possible_UIDs:

    digit1 = bounding_boxes[UID[1]].split()
    digit8 = bounding_boxes[UID[1] + 7].split()

    h1 = min(height-int(digit1[4]),height-int(digit8[4]))
    h2 = max(height-int(digit1[2]),height-int(digit8[2]))

    if SR==False:
      top_left_corner = (int(digit1[1]),h1)
      bottom_right_corner = (int(digit8[3]),h2)
      botton_left_corner=(int(digit1[1]),h2-3)
      thickness=h1-h2

    else:
      top_left_corner = (int(int(digit1[1])/SR_Ratio[0]),int((h1)/SR_Ratio[1]))
      bottom_right_corner = (int(int(digit8[3])/SR_Ratio[0]),int((h2)/SR_Ratio[1]))
      botton_left_corner=(int(int(digit1[1])/SR_Ratio[0]),int((h2)/SR_Ratio[1]-3))
      thickness=int((h1)/SR_Ratio[1])-int((h2)/SR_Ratio[1])
    

    #print(thickness)
    img = cv2.rectangle(img,top_left_corner,bottom_right_corner,(0,0,0),-1)
    #img= cv2.putText(img,'xxxx xxxx',botton_left_corner,cv2.FONT_HERSHEY_SIMPLEX,(thickness/-24),(0,0,0),2,cv2.LINE_AA)
    
  if rtype==2:
    img = cv2.rotate(img,cv2.ROTATE_90_CLOCKWISE)
  elif rtype==3:
    img = cv2.rotate(img,cv2.ROTATE_180)
  elif rtype==4:
    img = cv2.rotate(img,cv2.ROTATE_90_COUNTERCLOCKWISE)

  file_name = image_path.split('/')[-1].split('.')[0]+"_masked"+"."+image_path.split('.')[-1]
  cv2.imwrite(file_name,img)
  return file_name

#---------------------------------------------------------------------------------------------------------#

def Extract_and_Mask_UIDs (image_path,SR=False,sr_image_path=None,SR_Ratio=[1,1]):

  if SR==False:
    img = cv2.imread(image_path)
  else:
    img = cv2.imread(sr_image_path)

  noise = cv2.fastNlMeansDenoisingColored(img,None,20,20,7,21) 
  gray = cv2.cvtColor(noise,cv2.COLOR_BGR2GRAY)
  
  #gray=img
  #print("Step1: Gray Image")
#   cv2_imshow(gray)

  rotations = [[gray,1],
               [cv2.rotate(gray,cv2.ROTATE_90_COUNTERCLOCKWISE),2],
               [cv2.rotate(gray,cv2.ROTATE_180),3],
               [cv2.rotate(gray,cv2.ROTATE_90_CLOCKWISE),4],
               [cv2.GaussianBlur(gray,(5,5),0),1],
               [cv2.GaussianBlur(cv2.rotate(gray,cv2.ROTATE_90_COUNTERCLOCKWISE),(5,5),0),2],
               [cv2.GaussianBlur(cv2.rotate(gray,cv2.ROTATE_180),(5,5),0),3],
               [cv2.GaussianBlur(cv2.rotate(gray,cv2.ROTATE_90_CLOCKWISE),(5,5),0),4]]

#   print("All rotated Gray Scale Images:")
#   cv2_imshow(rotations[0][0])
#   cv2_imshow(rotations[1][0])
#   cv2_imshow(rotations[2][0])
#   cv2_imshow(rotations[3][0])
#   print("All rotated blur grayscale Images")
#   cv2_imshow(rotations[4][0])
#   cv2_imshow(rotations[5][0])
#   cv2_imshow(rotations[6][0])
#   cv2_imshow(rotations[7][0])

  settings = ('-l eng --oem 3 --psm 11')

  for rotation in rotations :

    ret, thresh2 = cv2.threshold(rotation[0], 120, 255, cv2.THRESH_BINARY_INV)
    
    cv2.imwrite('rotated_grayscale.png', thresh2)


    bounding_boxes = pytesseract.image_to_boxes(Image.open('rotated_grayscale.png'),config=settings).split(" 0\n")
    #print(bounding_boxes)
    possible_UIDs = Regex_Search(bounding_boxes)

    if len(possible_UIDs)==0:
      continue
    else:

      if SR==False:
        masked_img = Mask_UIDs (image_path,possible_UIDs,bounding_boxes,rotation[1])
      else:
        masked_img = Mask_UIDs (image_path,possible_UIDs,bounding_boxes,rotation[1],True,SR_Ratio)
      
      #cv2_imshow(masked_img)

      return (masked_img,possible_UIDs)

  return (None,None)


#--------------------------------------------------------------------------------------------------------
def masking_file(input_path):
  k=0
  output="result.pdf"
  #input_path = "/content/e.jpg"   # Path to the Input Image/PDF
  if input_path.split('.')[-1]=="pdf":    
    pages = pdf2image.convert_from_path(input_path, 300,poppler_path=r'C:\Program Files\poppler-0.68.0\bin')
    for i in pages:
      i.save('pdf2img.jpg', 'JPEG')
      print("Page No:-"+str(k))
      #print(k)
      k+=1
      flag=addhar_check('pdf2img.jpg')
      print(flag)
      if(flag!=0):
        masked_img,possible_UIDs = Extract_and_Mask_UIDs('pdf2img.jpg')
        if masked_img!=None and input_path.split('.')[-1]=="pdf" :    
          image = Image.open(masked_img) 
          pdf_bytes = img2pdf.convert(image.filename) 
          file = open("2"+".pdf", "wb")
          masked_img = "2"+".pdf" 
          file.write(pdf_bytes) 
          image.close() 
          file.close()
          merger(input_path,"2.pdf",k-1,0)
          break
  # if input_path.split('.')[-1]=="TIF":

  elif input_path.split('.')[-1]=="TIF" or input_path.split('.')[-1]=="tif":
    try:
      x=Image.open(input_path)
    except PIL.UnidentifiedImageError:
      print("Error Occured")
      return
    li=[]
    page_no=addhar_check(input_path)
    try:
      y=img2pdf.convert(x.filename)
    except img2pdf.AlphaChannelError:
      return
    totalPages=total_pages(input_path)
    #print("Suraj"+str(totalPages))
    file = open("1"+".pdf", "wb")
    dup_img = "1"+".pdf"
    #print(dup_img) 
    file.write(y) 
    x.close() 
    file.close()
    p=pdf2image.convert_from_path(dup_img, 300,poppler_path=r'C:\Program Files\poppler-0.68.0\bin')
    for i in range(totalPages):
      
      p[i].save('dup.jpg','JPEG')
      masked_img,possible_UIDs = Extract_and_Mask_UIDs('dup.jpg')
      if masked_img!=None:
        global counter
        counter+=1
        image = Image.open(masked_img) 
        pdf_bytes = img2pdf.convert(image.filename) 
        file = open(str(i)+".pdf", "wb")
        masked_img = str(i)+".pdf" 
        file.write(pdf_bytes) 
        image.close() 
        file.close()
        #print(list(possible_UIDs[0])[0])
        #merger("1.pdf","2.pdf",page_no-1,1) 
        global Suraj
        Suraj.append(list(possible_UIDs[0])[0])
    
      else:
        image = Image.open('dup.jpg') 
        pdf_bytes = img2pdf.convert(image.filename) 
        file = open(str(i)+".pdf", "wb")
        masked_imgx = str(i)+".pdf" 
        file.write(pdf_bytes) 
        image.close() 
        file.close()
      li.append(str(i)+".pdf")
    #print(list(Suraj[0])[0])
    
  else:
    masked_img,possible_UIDs = Extract_and_Mask_UIDs(input_path)


  # if masked_img!=None and input_path.split('.')[-1]=="pdf" :    
  #   image = Image.open(masked_img) 
  #   pdf_bytes = img2pdf.convert(image.filename) 
  #   file = open(input_path.split('/')[-1].split('.')[0]+"_masked"+".pdf", "wb")
  #   masked_img = input_path.split('/')[-1].split('.')[0]+"_masked"+".pdf" 
  #   file.write(pdf_bytes) 
  #   image.close() 
  #   file.close() 


  # if masked_img!=None and (input_path.split('.')[-1]=="TIF" or input_path.split('.')[-1]=="tif" ):
  #   image = Image.open(masked_img) 
  #   pdf_bytes = img2pdf.convert(image.filename) 
  #   file = open("2"+".pdf", "wb")
  #   masked_img = "2"+".pdf" 
  #   file.write(pdf_bytes) 
  #   image.close() 
  #   file.close()
  #   merger("1.pdf","2.pdf",page_no-1,1) 

  # if counter>0:
  #   mergeAll(li,"result.pdf")
  # else:
  #   Suraj.clear()
  #   counter=0
  #   return NULL


  if masked_img==None and counter==0:
    s="Can't find any UID!"
    print("Can't find any UID!")
    # continue
  else:
    mergeAll(li,"result.pdf")
    #print("Found UIDs : "+str(possible_UIDs[:,0]))
    s="Found UIDs :"+str(Suraj)
    print("Found UIDs :"+str(Suraj))
    Suraj.clear()
    counter=0
  return s
#----------------------------------------------------------------------------------------------------
# def Suraj(filename):
#//*[@id="Done"]/label[1] //*[@id="Done"]

#----------------------------------------------------------------------------------------------------

# s=masking_file(r'Restart\Address_Proof_LA_13892944.tif')
# print(s)

#-------------------------------------------------------------------------------------------------------#
count=1
path=r'C:\Users\32020\Documents\19000\5555'
ppath=r'C:\Users\32020\Documents\19000\5555OUT'
filenaame=""
x=""
oldpdf1=""
newpdf1=""
oldpdf2=""
newpdf2=""
files=[]
for r,d,f in os.walk(path,topdown=True):
    for file in f:
        if ('.TIF' in file or '.tif' in file):
            files.append(os.path.join(r,file))
li=[]
for f in files:
    filename=f.split('\\')[-1]  #filename with extension
    filenaame=filename.split('.')[-2]+".pdf"   #filename without extension required for pdf
    
    print(str(count)+") "+f+": masking in progress.")
    if('Address_Proof' in filename or 'Age_Proof' in filename or 'Identity_Proof' in filename):
      li.append(f.split('\\')[-2])
      x=os.path.join(ppath,f.split('\\')[-2])
      old=os.path.join(x,'final.tif')
      new=os.path.join(x,filename)
      oldpdf1=os.path.join(x,'result.pdf')
      newpdf1=os.path.join(x,filenaame)
      oldpdf2=os.path.join(x,'2.pdf')
      newpdf2=os.path.join(x,filenaame)
      
      #print(old+"\t"+new)
      try:
        os.mkdir(x)
      except FileExistsError:
        print("folder already exist")
      finally:
        s=masking_file(f)
        try:
          if(s!="Can't find any UID!"):
            dest=shutil.move('result.pdf',x)
            os.rename(oldpdf1,newpdf1)
            file1 = open("rr.txt", "a")  # append mode
            file1.write(f+":\t"+s+"\n")
            file1.close()
          else:
            file1 = open("rr.txt", "a")  # append mode
            file1.write(f+":\t"+"Can't find any UID!"+"\n")
            file1.close()
        except (FileNotFoundError,PermissionError,shutil.Error):
          print("Error!!!!")
        #print(s) 
        
    count+=1
