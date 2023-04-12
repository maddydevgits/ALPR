import streamlit as st
import cv2
import boto3

st.title('Test')
run=st.checkbox('Run Camera')

FRAME_WINDOW=st.image([])
camera=cv2.VideoCapture(0)

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


while run:
    _,frame=camera.read()
    frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    FRAME_WINDOW.image(frame)
    
    cv2.imwrite('test.jpg',frame)
    st.success(readText())
    break
