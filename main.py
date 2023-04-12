import serial
import cv2
import boto3
from pymongo import MongoClient
from datetime import datetime
import telebot

bot=telebot.TeleBot('5987561335:AAFXnO75YidOHEfML3GkKM5qBRxpHUrnDew')


client=MongoClient('localhost',27017)
db=client['HugsforBugs']
c=db['alpr']
c1=db['chalans']

camera=cv2.VideoCapture(2)
ser=serial.Serial('COM3',9600,timeout=0.5)
ser.close()
ser.open()

def readText():
    results=[]
    imageSource=open('test1.jpg','rb')
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

while True:
    if(ser.inWaiting()>0):
        data=ser.readline()
        data=data.decode('utf-8')
        print(data)
        if data.startswith('#'):
            print('Invoking Camera')
            _,frame=camera.read()
            frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)    
            cv2.imwrite('test1.jpg',frame)
            vehiclename=readText()
            data={}
            for i in c.find():
                if i['vehicleno']==vehiclename:
                    data['vehicleno']=vehiclename
                    data['timestamp']=str(datetime.now())
                    data['amount']=1000
                    data['mobileno']=i['mobileno']
                    c1.insert_one(data)
                    print('Chalan Fined')
                    bot.send_message(data['mobileno'],'You have fined a chalan, check dashboard')
                    print('Bot Send a message')
                    bot.send_document(chat_id=data['mobileno'], document=open('test1.jpg', 'rb'))


            