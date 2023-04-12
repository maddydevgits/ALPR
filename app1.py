import streamlit as st
from PIL import Image
import cv2
import pytesseract
import pandas as pd
from pymongo import MongoClient
import boto3

client=MongoClient('localhost',27017)
db=client['HugsforBugs']
c=db['alpr']

def image(img): # to read image in pixel format 
    return Image.open(img)

def readText():
    results=[]
    imageSource=open('test.jpg','rb')
    client=boto3.client('textract')
    response=client.detect_document_text(Document={'Bytes':imageSource.read()})
    for item in response['Blocks']:
        if item['BlockType']=='LINE':
            lp=item['Text']
            results.append(lp)
    try:
        lens=[]
        print(results)
        for i in results:
            lens.append(len(i))
        return (results[lens.index(max(lens))])
    except:
        return None

def app():
    st.header('ALPR Training')
    img_file=st.file_uploader('Upload Image', type=['png','jpg','jpeg'])

    if img_file is not None: # when someone uploads a file 
        file_details={} # to store the details of file 
        file_details['type']=img_file.type
        file_details['size']=img_file.size
        file_details['name']=img_file.name
        st.write(file_details)
        st.image(image(img_file)) # show image on web app 
    
        with open('test.jpg','wb') as f: # save the image 
            f.write(img_file.getbuffer())

        vehicleno=readText()
        st.success(vehicleno)
        ownername=st.text_input('Enter Owner Name')
        address=st.text_input('Enter Address')
        mobileno=st.text_input('Enter MobileNo')
        if st.button('Register Vehicle'):
            k={}
            k['vehicleno']=vehicleno
            k['ownername']=ownername
            k['address']=address
            k['mobileno']=mobileno
            c.insert_one(k)
            st.success('Vehicle Data Registerd')
    