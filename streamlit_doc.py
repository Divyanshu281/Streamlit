import streamlit as st
import pandas as pd
import time
st.title('Startup Dashboard')
st.header('This is my first code in streamlit')
st.subheader('I am lola') 

st.write('Ye ekk normal text h bas isme itna jada kuch khaas likha nahui hai')
st.markdown(""" 

### My fvrt movies
- Kanka
- Halka
- Salka
            """)

st.code("""
def sqrt(num):
        return num**2

""")
st.latex('12^x4+95^12-45 ')

df = pd.DataFrame({
    'Name': ['Divyanshu',' divyanshu lala', 'lala dovyanshu'],
    'Marks': [45, 90, 1000],
    'Package':['40LPA', '70LPA', '1.2CR']



})

st.dataframe(df)
st.metric('Revenue', '3L', '50%')
st.json(
    {
    'Name': ['Divyanshu',' divyanshu lala', 'lala dovyanshu'],
    'Marks': [45, 90, 1000],
    'Package':['40LPA', '70LPA', '1.2CR']



    }

)

st.sidebar.title("Mera lola")

col1, col2 = st.columns(2)

with col1:
    st.button("Mjhe dabao na")

with col2:
    st.title('Kaka lola')

st.error("Lola Error")
st.success("           Lola Pass          ")
st.info("Kaam Ki cheex ha")
st.warning("Mat  kat lala Mat kr ")

bar  = st.progress(0)
for i in range(1,100):
    time.sleep(0.1)
    bar.progress(i)

email = st.text_input('Enter Email')
number = st.number_input("Enter age")
date = st.date_input("Lola Date daal")

email = st.text_input("Enter Email")
password = st.text_input("Enter your password")
btn = st.button("Login")
gender = st.selectbox('Select Gender', ['Male', 'Female', 'Others'])

if btn:
    if email=='divyanshubindal76@gmail.com' and password == '328026':
        st.success("Login Successful")
        st.balloons()
        st.write(gender)
    else: 
        st.error('Login Failed')   
file = st.file_uploader('Upload a csv File')
if file is not None:
    df = pd.read_csv(file)
    st.dataframe(df.describe())