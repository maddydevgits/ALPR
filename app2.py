import streamlit as st
from pymongo import MongoClient
import pandas as pd

client=MongoClient('localhost',27017)
db=client['HugsforBugs']
c=db['chalans']
def app():
    st.header('Check Chalans')
    mobileno=st.text_input('Enter Mobile No')
    if st.button('Get Chlalans'):
        st.warning('Loading...')
        data=[]
        for i in c.find():
            if mobileno==i['mobileno']:
                dummy=[]
                dummy.append(i['vehicleno'])
                dummy.append(i['timestamp'])
                dummy.append(i['amount'])
                dummy.append(i['mobileno'])
                data.append(dummy)
        if(len(data)==0):
            st.success('Data Loaded')
            st.success('No Chalans')
        else:
            st.success('Data Loaded')
            dataframe=pd.DataFrame(data)
            dataframe.columns=['Vehicle No','Date','Amount','Mobile No']
            st.dataframe(dataframe)
        