import paho.mqtt.client as mqtt
import time
import serial
import string
import pynmea2
from threading import *
import tkinter as tk
import tkintermapview

marker_1 = None

direc = "up"
ava_flag = 1
emer_flag = 1
lat = 0
lng = 0
marker_flag = 2

my_label = None
label_flag = 0

def Btn_1_Action():
    global direc
    direc = "up"

def Btn_2_Action():
    global direc
    direc = "left"

def Btn_3_Action():
    global direc
    direc = "right"

def Radio_Action():
    global selected_Radio_Btn
    global ava_flag

    selected_value = selected_Radio_Btn.get()
    
    if selected_value == 1:
        ava_flag = 1
        
        
    elif selected_value == 2:
        ava_flag = 0
        
    else:
        ava_flag = 1
    
        
        
        

def show_frame(frame):
    frame.tkraise()


my_id ='10'
my_topic = "myTopic"
traffic_light="green"
split0=[]
message=str()

def on_message(client, userdata, msg):
    global message
    global split0
    global my_topic
    global traffic_light
    global c_red
    global filename_red
    global my_label
    global label_flag
    message = str(msg.payload.decode('utf-8'))
    split0=message.split(",")
    if split0[0]== my_id:
        if split0[1]== '1':
            if split0[2]!= my_topic:
                if label_flag == 1:
                    my_label.destroy()
                client.unsubscribe(my_topic)
                my_topic=split0[2]
                print(my_topic)
                client.subscribe(my_topic)
    elif (split0[0]== "emergency"):
        my_label = tk.Label(frame1, bg = "white",text = "Emergency on the road")
        my_label.place(x=350,y=20)
        label_flag = 1
    elif (split0[0]== "traffic"):                
        if (direc == "up"):            
            traffic_light= split0[1]
            
            if (traffic_light == "red"):
                filename_red=tk.PhotoImage(file="//home//pi//rpi//MQTT//ahmar.png")    
                
            elif (traffic_light == "yellow"):
                filename_red=tk.PhotoImage(file="//home//pi//rpi//MQTT//asfar.png")    
            
            elif (traffic_light == "green"):
                filename_red=tk.PhotoImage(file="//home//pi//rpi//MQTT//akhdar.png")    
            
            c_red.destroy()
            c_red=tk.Canvas(frame1,bg="gray16",height=200,width=200)
            background_label_red=tk.Label(frame1,image=filename_red)
            background_label_red.place(x=270,y=60)

        if (direc == "right" or direc == "left"):            
            traffic_light= split0[2]
            
            if (traffic_light == "red"):
                filename_red=tk.PhotoImage(file="//home//pi//rpi//MQTT//ahmar.png")    
                
            elif (traffic_light == "yellow"):
                filename_red=tk.PhotoImage(file="//home//pi//rpi//MQTT//asfar.png")    
            
            elif (traffic_light == "green"):
                filename_red=tk.PhotoImage(file="//home//pi//rpi//MQTT//akhdar.png")    
            
            c_red.destroy()
            c_red=tk.Canvas(frame1,bg="gray16",height=200,width=200)
            background_label_red=tk.Label(frame1,image=filename_red)
            background_label_red.place(x=270,y=60)
        
    
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(my_topic)

def timerinterrupt():
    global ava_flag
    global emer_flag
    global direc
    global my_id
    global lat
    global lng
    global map1
    global marker_flag
    global marker_1
    
    port="/dev/ttyAMA0"
    ser=serial.Serial(port, baudrate=9600, timeout=0.5)
    dataout = pynmea2.NMEAStreamReader()
    newdata=ser.readline()
    newdata= str(newdata,"ISO8859-1")
    
    gps = str(my_id)+ "," + str(lng) + "," + str(lat) + "," + str(direc) + "," + str(emer_flag) + "," + str(ava_flag)
    
    if lat != 0:
        client.publish(my_topic, payload= gps, qos=0, retain=False)        
        marker_flag = marker_flag + 1
        if marker_flag == 3:
            marker_1.delete()
            marker_1 = map1.set_position(lat, lng, marker=True)
            marker_1.set_text("Your location")
            marker_flag = 0
            
#     marker_1 = map1.set_position(lat, lng, marker=True)
        #    marker_1.set_text("Your location")
            
    if (newdata[0:6] == "$GPRMC"):
        newmsg=pynmea2.parse(newdata)
        lat=newmsg.latitude
        lng=newmsg.longitude
        #gps = "Latitude=" + str(lat) + " and Longitude=" + str(lng)
        #gps =  str(ava_flag)+ "," +str(lng) + "," + str(lat)
        #gps = str(my_id)+ "," + str(ava_flag) + "," + str(lng) + "," + str(lat) + "," + str(direc) + "," + str(emer_flag)
#        gps = str(my_id)+ "," + str(lng) + "," + str(lat) + "," + str(direc) + "," + str(emer_flag) + "," + str(ava_flag)

#        client.publish(my_topic, payload= gps, qos=0, retain=False)
#        print("ana")
        
    t=Timer(1,timerinterrupt)
    t.start()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("broker.emqx.io", 1883, 60)

client.loop_start()
timerinterrupt()

window = tk.Tk()
#window.state('zoomed')
#window.wm_state('zoomed')
window.attributes('-zoomed', True)

window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)

frame1 = tk.Frame(window)
frame2 = tk.Frame(window)
frame3 = tk.Frame(window)

for frame in (frame1, frame3,):
    frame.grid(row=0,column=0,sticky='nsew')

    
#==================Frame 1 code
frame1_title=  tk.Label(frame1)
frame1_title.pack(fill='both', expand=True)



c=tk.Canvas(frame1,bg="gray16",height=200,width=200  )
filename=tk.PhotoImage(file="//home//pi//rpi//MQTT//navy.png")
background_label=tk.Label(frame1,image=filename)
background_label.place(x=0,y=0,relwidth=1,relheight=1)






c_red=tk.Canvas(frame1,bg="gray16",height=200,width=200)
filename_red=tk.PhotoImage(file="//home//pi//rpi//MQTT//akhdar.png")    
background_label_red=tk.Label(frame1,image=filename_red)
background_label_red.place(x=270,y=60)




#creating buttons
Btn_1 = tk.Button(frame1,text="FORWARD", bg = "white", width = 5, height = 3, command = Btn_1_Action)
Btn_2 = tk.Button(frame1,text="LEFT", bg = "white", width = 5, height = 3, command = Btn_2_Action)
Btn_3 = tk.Button(frame1,text="RIGHT", bg = "white" , width = 5, height = 3, command = Btn_3_Action)



selected_Radio_Btn = tk.IntVar()
selected_Radio_Btn.set("1")

myRadioBtn_1 = tk.Radiobutton(frame1,width = 8,bg = "white", text = "Active  ", value = 1, variable = selected_Radio_Btn, command = Radio_Action )
myRadioBtn_2 = tk.Radiobutton(frame1,width = 8,bg = "white", text = "Inactive", value = 2, variable = selected_Radio_Btn, command = Radio_Action )




#Displaying buttons

Btn_1.place(x=80,y=162)
Btn_2.place(x=40,y=230)
Btn_3.place(x=115,y=230)



myRadioBtn_1.place(x = 70, y = 20)
myRadioBtn_2.place(x = 70, y = 50)


frame1_btn = tk.Button(frame1, text='View Map',width = 10, height = 5, bg = "white",command=lambda:show_frame(frame3))
frame1_btn.place(x=650,y=160)

#==================Frame 2 code
frame2_title=  tk.Label(frame2, text='Page 2', font='times 35', bg='yellow')
frame2_title.pack(fill='both', expand=True)


c2=tk.Canvas(frame2,bg="gray16",height=200,width=200)
filename2=tk.PhotoImage(file="//home//pi//rpi//MQTT//navy.png")
background_label2=tk.Label(frame2,image=filename2)
background_label2.place(x=0,y=0,relwidth=1,relheight=1)


                #Frame 3 code
#frame3_title=  tk.Label(frame3, bg='blue')
#frame3_title.pack(fill='x', expand=True)

frame3_btn = tk.Button(frame3, text = "View Traffic Light Status", bg="lightblue", command=lambda:show_frame(frame1))
frame3_btn.pack(fill ='x', ipady = 10)


#############
#webpage

map1 = tkintermapview.TkinterMapView(frame3, width=800, height=600, corner_radius=0)
map1.pack()

marker_1 = map1.set_position(30.000804666666667, 31.197149833333334, marker=True)


#############






show_frame(frame1)

window.mainloop()
