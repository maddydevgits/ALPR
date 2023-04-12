import app1 
import app2
import streamlit as st

st.title('Automatic License Plate Recognition System')
PAGES = {
    "ALPR Registration": app1,
    "Check Challan": app2
}
st.sidebar.title('Dashboard')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()