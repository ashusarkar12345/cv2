import streamlit as st
import numpy as np 
import pandas as pd
import cv2 
import os 
from PIL import Image
import sqlite3
import face_recognition
import datetime as dt 
from datetime import datetime
from matplotlib import pyplot as plt
import io
import base64
#functions
#---------------------------------------------------------------------------------------------------------------------------------
#function to click picture for new user 
def clic_pic(f_name,l_name):
    cam = cv2.VideoCapture(0)
    
    cv2.namedWindow("Smile Please")

    img_counter = 0

    while True:
        ret, frame = cam.read()
        frames = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.putText(frame,"Press SPACE to click picture and ESC to exit",(10,20),cv2.FONT_HERSHEY_SIMPLEX,0.8,(150,0,255),2)
        if not ret:
            print("failed to grab frame")
            break
        #faceloc=face_recognition.face_locations(frames)
        #cv2.rectangle(frames,(faceloc[3],faceloc[0]),(faceloc[1],faceloc[2]),(255,0,255),2)
        cv2.imshow("Smile Please", frame)

        k = cv2.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k%256 == 32:
            # SPACE pressed
            img_name = "opencv_frame_{}".format(img_counter)
            cropped=frame[25:,:]
            cv2.imwrite(r"\attendance members\{}_{}.png".format(f_name,l_name),cropped)
            print("{} written!".format(img_name))
            img_counter += 1

    cam.release()

    cv2.destroyAllWindows()
    return frame
#---------------------------------------------------------------------------------------------------------------------------------
# function to click picture to mark attendance
def Mark_attendance():
    cam = cv2.VideoCapture(0)
    
    cv2.namedWindow("test")

    img_counter = 0

    while True:
        ret, frame = cam.read()
        frames = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.putText(frame,"Press SPACE to click picture and ESC to exit",(10,20),cv2.FONT_HERSHEY_SIMPLEX,0.8,(150,0,255),2)
        if not ret:
            print("failed to grab frame")
            break
        #faceloc=face_recognition.face_locations(frames)
        #cv2.rectangle(frames,(faceloc[3],faceloc[0]),(faceloc[1],faceloc[2]),(255,0,255),2)
        cv2.imshow("test", frame)

        k = cv2.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k%256 == 32:
            # SPACE pressed
            img_name = "opencv_frame_{}".format(img_counter)
            cropped=frames[25:,:]
            print("{} written!".format(img_name))
            img_counter += 1

    cam.release()

    cv2.destroyAllWindows()
    return cropped   
#---------------------------------------------------------------------------------------------------------------------------------------------
def att_marker(ima):
    path=r"\attendance members"
    files=os.listdir(path)
    images=[]
    encodes=[]
    names=[]
    #Read images from folder in list
    for i in files:
        im=face_recognition.load_image_file("{}\{}".format(path,i))
        images.append(im)
    #Convert images to encodes
    for i in range(0,len(images)):
        ec=face_recognition.face_encodings(images[i])[0]
        encodes.append(ec)
    #Pulling names of candidates from filenames
    for i in range(0,len(files)):
        nm=files[i].split(".")[0]
        names.append(nm)
    ee=face_recognition.face_encodings(ima)[0]
    #finding match position
    position=[]
    for i in range(0,len(encodes)):
        matcher=face_recognition.compare_faces([encodes[i]],ee)
        if matcher[0]==True:
            position.append(i)

    #frames = cv2.cvtColor(ima, cv2.COLOR_BGR2RGB)
    frames=ima
    faceloc=face_recognition.face_locations(frames)
    for top, right, bottom, left in faceloc:
            # Draw a box around the face
            cv2.rectangle(frames, (left, top), (right, bottom), (0, 0, 255), 2)
    cv2.putText(frames,"Hello {} attendance is marked for Date: {} ".format(names[position[0]],dt.date.today()),(10,20),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,0,0),2)
    with open(('attendance1.csv'),'r+') as f:
        myDataList = f.readlines()
        nameList = []
        dat=[]
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
            curdt=dt.date.today()
            dat.append(curdt)
        if names[position[0]] not in nameList and dt!=dt.date.today():
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            z=1
            f.writelines('\n{},{},{},{}'.format(z,names[position[0]],dtString,dt.date.today()))
            z+=1
        return frames 
        
   
#---------------------------------------------------------------------------------------------------------------------------------------------
#function 
def showattendance():
        df=pd.read_csv("attendance1.csv",header=None)
        df.columns=["S.no","Name","Time","Date"]
        x=[i+1 for i in range(len(df.Date))]
        df["S.no"]=x
        df.set_index("S.no",inplace=True)
        return df       
#---------------------------------------------------------------------------------------------------------------------------------
#Database management
conn = sqlite3.connect('data.db')
c = conn.cursor()
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(first_name TEXT,last_name TEXT,username TEXT,password TEXT)')
def add_userdata(first_name,last_name,username,password):
	c.execute('INSERT INTO userstable(first_name,last_name,username,password) VALUES (?,?,?,?)',(first_name,last_name,username,password))
	conn.commit()
def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data
#----------------------------------------------------------------------------------------------------------------------------------
def download_link(object_to_download, download_filename, download_link_text):
    if isinstance(object_to_download,pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False)

    # some strings <-> bytes conversions necessary here
    b64 = base64.b64encode(object_to_download.encode()).decode()
    return b64        
#----------------------------------------------------------------------------------------------------------------------------------
st.image("clipart1417167.png")

"""# Attendance marker app """
"""### This is an attempt to simplify the attendance marking procedure during the online classes."""
"""By:-Ashish Chandra Sarkar"""
'''DF-2002-CM'''
menu = ["Home","Login","SignUp"]
choice = st.sidebar.selectbox("Menu",menu)
if choice == "Home":
		st.subheader("Home")
elif choice == "Login":
        st.subheader("Login")
        user=st.sidebar.text_input("Username")
        passw=st.sidebar.text_input("Password",type="password")
        if st.sidebar.button("Login"):
            result=login_user(user,passw)
            if result:
                st.success("Logged in as {}".format(user))
                menu2 = ['Mark Attendance', 'Current Attendance']
                attribute = st.selectbox('Choose attribute', menu2)
                if attribute == 'Mark Attendance':
                    ima=Mark_attendance()
                    imu=att_marker(ima)
                    st.image(imu, caption="Catured image")
                    st.success("You have successfully Marked your attendance")
                #elif attribute == 'Current Attendance':
                'Attendance Sheet:',showattendance()
                download_link(showattendance(), 'attendance_df.csv', 'Click here to download data!')
            else:
                danger_html="""  <div style="background-color:#F08080;padding:10px ><h2 style="color:black ;text-align:center;">Incorrect Username/Password</h2></div>""" 
                st.warning("Incorrect username/password")              




elif choice == "SignUp":
        st.subheader("SignUp")
        f_name=st.text_input("First name")
        l_name=st.text_input("Last name")
        username=st.text_input("Username")
        password=st.text_input("Password",type='password')
        
        st.markdown('''### To take your picture click hit me''')
        
        if st.button("Hit me"):
            click=clic_pic(f_name,l_name)
            create_usertable()
            add_userdata(f_name,l_name,username,password)
        
        html='''<p style="color:blue">Check Smile please window for picture, will open as a new window</p>'''
        st.markdown(html,unsafe_allow_html=True)
        
        st.markdown('''#### Do you want to check your final picture ?''')
        
        if st.button("Yes"):
            image = Image.open(r"\attendance members\{}_{}.png".format(f_name,l_name))
            st.image(image, caption="{}_{}.png".format(f_name,l_name))
            st.success("You have successfully created an account.Go to the Login Menu to login")
        
