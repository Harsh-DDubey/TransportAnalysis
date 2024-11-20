import tkinter as tk
from tkinter import ttk
import pymysql
import pyttsx3
from PIL import ImageTk
from datetime import date
from datetime import timedelta
from datetime import datetime
from geopy import Nominatim
from geopy import distance
# Initialize text-to-speech engine
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

#-----------------------------------------------------------------------------------------------

# Database connection
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='sammy',
        password='mukund',
        database='mydatabase'
    )

#------------------------------------------------------------------------------------------------

# Function to create pass table
def create_pass_table(cursor):
    query = '''
    CREATE TABLE IF NOT EXISTS pass (
        sr_no INT AUTO_INCREMENT PRIMARY KEY,
        Username VARCHAR(20),
        Password VARCHAR(20)
    );
    '''
    cursor.execute(query)
    print("Password table created (if it didn't exist)")
    print(cursor.execute("SELECT * FROM pass"))

#------------------------------------------------------------------------------------------------

# Function to add a user
def add_user(username, password):
    query = '''INSERT INTO pass(Username, Password) VALUES (%s, %s)'''
    cursor.execute(query, (username, password))
    mycon.commit()

#-------------------------------------------------------------------------------------------------

# Function to create userdata table
def create_userdata_table(cursor):
    query = '''
    CREATE TABLE IF NOT EXISTS userdata (
        sr_no INT AUTO_INCREMENT PRIMARY KEY,
        Username VARCHAR(20),
        Travelling_mode VARCHAR(20),
        Distance_to_be_travelled INT,
        Total_Tour_cost INT
    );
    '''
    cursor.execute(query)

# Function to print the userdata table
def print_whole_table(cursor):
    query = "SELECT * FROM userdata"
    cursor.execute(query)
    rows = cursor.fetchall()
    print("Complete userdata:")
    print("sr No | Username        | Travelling_mode | Distance_to_be_travelled | Total_tour_cost")
    print("------------------------------------------------------------------------------------")
    for row in rows:
        print(f"{row[0]:<6} | {row[1]:<12}  | {row[2]:<15} | {row[3]:<25} | {row[4]:<10}")

#Defining the admin user
def admin_user():
    username=username_entry.get().strip()
    if username=="Harsh":
        print("What you want to access")
        print("Enter User data To access userdata table")
        Accessibility=input("Please enter data to be accessed")
        if Accessibility=="userdata":
            print_whole_table(cursor)
            NextStep=input("Enter Next Step")
            if NextStep=="Continue":
                print("Continuing")
            else:
                print("Exiting the program")
        else:
            print("No data entered")
#Defining personal schedule table
def create_personal_table(cursor):
    query='''CREATE TABLE IF NOT EXISTS personaldata(
        Sr_no INT AUTO_INCREMENT PRIMARY KEY,
        Username VARCHAR(20),
        Travelling_mode VARCHAR(20),
        Total_Journey_cost VARCHAR(20)
    );
    '''
    cursor.execute(query)
def add_personal_data(name,TravellingMode,JourneyCost):
    query='''INSERT INTO personaldata(Username,Travelling_mode,Total_Journey_cost)VALUES(%s,%s,%s)'''
    cursor.execute(query,(name,TravellingMode,JourneyCost))
    mycon.commit()
#Function to print the personal userdata schedule table
def print_whole_personaltable(cursor):
    query = "SELECT * FROM personaldata"
    cursor.execute(query)
    rows = cursor.fetchall()
    print("Complete PersonalUserDATA:")
    print("Sr No | Username        | Travelling mode | Total Journey cost")
    print("------------------------------------------------------------------------------------")
    for row in rows:
        print(f"{row[0]:<6} | {row[1]:<12}  | {row[2]:<15} | {row[3]:<25}")
        

# Initialize the database connection
mycon = get_db_connection()
cursor = mycon.cursor()
create_pass_table(cursor)

# User choice handling
print("If you are a Pre-existing user press 1")
print("If you are a new user press 2")
speak("Please Enter Choice")
choice = int(input("Enter choice: "))

if choice == 1:
    speak("choice accepted")
    speak("redirected")
    window = tk.Tk()
    window.geometry('800x500')
    window.configure(background='#31363b')

    tk.Label(window, text="Enter Username:", bg='#31363b', fg='white').grid(row=0, column=0, padx=10, pady=10, stick='w')
    username_entry = tk.Entry(window)
    username_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(window, text="Enter Password:", bg='#31363b', fg='white').grid(row=1, column=0, padx=10, pady=10, sticky='w')
    password_entry = tk.Entry(window, show='*')
    password_entry.grid(row=1, column=1, padx=10, pady=10)

    def show():
        hide_button=tk.Button(window,image=hide_image,command=hide,relief="flat",activebackground='white',bd=0,background='white',width=30,height=25)
        hide_button.place(x=375,y=50)
        password_entry.config(show='')

    def hide():
        show_button=tk.Button(window,image=show_image,command=show,relief="flat",activebackground='white',bd=0,background='white',width=30,height=25) 
        show_button.place(x=370, y=60)
        password_entry.config(show='*')
    
    show_image=ImageTk.PhotoImage(file='show.png')
    hide_image=ImageTk.PhotoImage(file='hide.png')
    show_button=tk.Button(window,image=show_image,command=show,relief="flat",activebackground='white',bd=0,background='white',width=30,height=25) 
    show_button.place(x=370, y=60)
    hide_button=tk.Button(window,image=hide_image,command=hide,relief="flat",activebackground='white',bd=0,background='white',width=30,height=25)
    hide_button.place(x=370,y=60)
    def check_user_exists(username):
        cursor = mycon.cursor()
        query = "SELECT * FROM pass WHERE Username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()  # Fetch one record
        cursor.close()
        return result is not None  # Returns True if the user exists
    global attempts
    attempts=3
    global flag
    flag=False

    def access_granted():
        #A three time counter before exiting the program 
        global attempts
        username = username_entry.get().strip()
        password=password_entry.get().strip()
        if username=="" or password=="":
            speak("Please enter data")
        else:
           if check_user_exists(username):
            if username=="Harsh" and password=="123456789":
                print("Admin Access Granted")
                speak("Welcome Admin")
                admin_user()
            else:
               global flag
               speak("Access Granted")
               flag=True
               print("Access Granted")
           else:
            attempts=attempts-1
            if attempts>0:
             print(f"Incorrect username Tries Remaining.{attempts}")
             print("Try again")
            else:
             print("Incorrect username")
             speak("User doesnt exist")
             window.destroy()
               
        
    tk.Button(window, text="Check Access", command=access_granted).grid(row=2, columnspan=1, pady=20)
    tk.Button(window,text="Close",command=window.destroy).grid(row=2,columnspan=2,pady=20)
    window.mainloop()
    
    if flag==True:
        print("You are welcomed to our travel agency we are delighted to have you have a wonderful and safe travelling ^_^")
        print("Enter your mode of travelling")
        Mode=input("Enter Mode of Travelling")
        if Mode=="Railways":
            
            print("Welcome to our Rail facility")
            print("Please use BLOCK LETTERS for futher communication")
            print("RAIL SERVICE IS AVAILABLE FOR NEW DELHI,MUMBAI,GORAKHPUR")
            #INITIAL JOURNEY DETAILS
            from datetime import date
            from datetime import timedelta
            from datetime import datetime
            def journeydetails():
                username=username_entry.get().strip() 
                password=password_entry.get().strip() 
                print(username)
                global aadharnumber
                aadharnumber=input("Enter Aadhar Number")
                if len(aadharnumber)>12:
                    print("Incorrect aadhar number")
                else:
                  pass
                global stlo
                stlo=str(input("Enter Source Station="))
                while stlo not in ['NEW DELHI','MUMBAI','GORAKHPUR']:
                    print('INVALID DATA')
                    stlo=str(input("Enter Source Station="))
                global enlo
                enlo=str(input("Enter end station="))
                while enlo not in ['NEW DELHI','MUMBAI','GORAKHPUR']:
                    print('INVALID DATA')
                    enlo=str(input("Enter Source Station="))
                global clas
                clas=str(input("Enter class(eg AC2 for AC second tier)"))
                global stdate
                STDATE=str(input('ENTER DATE FOR BOOKING(USE FORMAT YYYY-MM-DD)'))
                stdate=date.fromisoformat(STDATE)
                while stdate<date.today():
                    print('INVALID DATE')
                    STDATE=str(input('ENTER DATE FOR BOOKING(USE FORMAT YYYY-MM-DD)'))
                    stdate=date.fromisoformat(STDATE)
                
                global nopassenger
                nopassenger=int(input("NO OF PASSENGERS"))
            
                #CHECK FOR BOOKING
                global stlo
                stlo=str(input("Enter Source Station="))
                while stlo not in ['NEW DELHI','MUMBAI','GORAKHPUR']:
                    print('INVALID DATA')
                    stlo=str(input("Enter Source Station="))
                global enlo
                enlo=str(input("Enter end station="))
                while enlo not in ['NEW DELHI','MUMBAI','GORAKHPUR']:
                    print('INVALID DATA')
                    enlo=str(input("Enter Source Station="))
                global clas
                clas=str(input("Enter class(eg AC2 for AC second tier)"))
                global stdate
                STDATE=str(input('ENTER DATE FOR BOOKING(USE FORMAT YYYY-MM-DD)'))
                stdate=date.fromisoformat(STDATE)
                while stdate<date.today():
                    print('INVALID DATE')
                    STDATE=str(input('ENTER DATE FOR BOOKING(USE FORMAT YYYY-MM-DD)'))
                    stdate=date.fromisoformat(STDATE)
                
                global nopassenger
                nopassenger=int(input("NO OF PASSENGERS"))

            #CHECK FOR BOOKING
            def furtheroption():   
                print('press 1 to continue booking further')
                print('press 2 to cancel booking ')
                print('press 3 to exit booking')
                global option
                option=int(input('NUMBER='))
            
            #FUNCTION USED TO BOOK TICKETS
            #TOTAL SEATS IN AC2 TIER IN GORAKHDAHM GKP->DELHI
            gorakhdham_gkpdelhi_seatac2=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40]
            #TOTAL SEATS IN AC3 TIER IN GORAKHDHAM GKP->DELHI
            gorakhdham_gkpdelhi_seatac3=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40]
            #TOTAL SEATS IN AC2 TIER IN GORAKHDHAM DELHI->GKP
            gorakhdham_delhigkp_seatac2=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40]
            #TOTAL SEATS IN AC3 TIER IN GORAKHDHAM DELHI->GKP
            gorakhdham_delhigkp_seatac3=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40]
            #TOTAL SEATS IN AC2 TIER IN GKP LTT SF GKP->MUMBAI
            gorakhdham_gkpmumbai_seatac2=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40]
            #TOTAL SEATS IN AC3 TIER IN GKP LTT SF GKP->MUMBAI
            gorakhdham_gkpmumbai_seatac3=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40]
            #TOTAL SEATS IN AC2 TIER GKP LTT SF MUMBAI->GKP
            gorakhdham_mumbaigkp_seatac2=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40]
            #TOTAL SEATS IN AC3 TIER GKP LTT SF MUMBAI->GKP
            gorakhdham_mumbaigkp_seatac3=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40]
            #TOTAL SEATS IN AC2 TIER MMCT TEJAS RAJ DELHI->MUMBAI
            gorakhdham_delhimumbai_seatac2=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40]
            #TOTAL SEATS IN AC3 TIER MMCT TEJAS RAJ DELHI->MUMBAI
            gorakhdham_delhimumbai_seatac3=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40]
            #TOTAL SEATS IN AC2 TIER NDLS TEJAS RAJ MUMBAI->DELHI 
            gorakhdham_mumbaidelhi_seatac2=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40]
            #TOTAL SEATS IN AC3 TIER NDLS  TEJAS RAJ MUMBAI->DELHI
            gorakhdham_mumbaidelhi_seatac3=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40]
            
            
            
            #LISTS OF BOOKED SEATS ACCORDING TO TRAIN AND TIER
            gorakhdham_gkpdelhi_seatac2_bookedseat=[]
            gorakhdham_gkpdelhi_seatac3_bookedseat=[]
            gorakhdham_delhigkp_seatac2_bookedseat=[]
            gorakhdham_delhigkp_seatac3_bookedseat=[]
            gorakhdham_gkpmumbai_seatac2_bookedseat=[]
            gorakhdham_gkpmumbai_seatac3_bookedseat=[]
            gorakhdham_mumbaigkp_seatac2_bookedseat=[]
            gorakhdham_mumbaigkp_seatac3_bookedseat=[]
            gorakhdham_delhimumbai_seatac2_bookedseat=[]
            gorakhdham_delhimumbai_seatac3_bookedseat=[]
            gorakhdham_mumbaidelhi_seatac2_bookedseat=[]
            gorakhdham_mumbaidelhi_seatac3_bookedseat=[]
            
            
            
            #FUNCTION TO PRINT DETAILS ON TICKET
            
            #GORAKHDHAM TRAIN GKP->DELHI
            def details_gorakhdham_gkpdelhi():
                teem=timedelta(days=1)
                print()
                print()
                print(datetime.today())
                print('||--->GORAKHDHAM EXP<---||')
                print('FROM GORAKHPUR JN ---->TO NEW DELHI')
                print('DEPARTURE ',stdate,'16:35-----ARRIVAL',(stdate+teem),' 05:15')
                print('JOURNEY DURATION--12HRS 40MIN')
                print('FREQUENCY-----EVERYDAY')
                print('AC2 TICKET COST PER HEAD-Rs.1645',end='/n'
                      'AC3 TICKET COST PER HEAD-Rs.1165')
                print()
                print()
            
            #GORAKHDHAM TRAIN DELHI->GKP
            def details_gorakhdham_delhigkp():
                teem=timedelta(days=1)
                print()
                print()
                print(datetime.today())
                print('||--->GORAKHDHAM EXP<---||')
                print('FROM NEW DELHI ---->TO GORAKHPUR JN')
                print('DEPARTURE',stdate,' 21:25-----ARRIVAL',(stdate+teem),' 09:45')
                print('JOURNEY DURATION--12HRS 20MIN')
                print('FREQUENCY-----EVERYDAY')
                print('AC2 TICKET COST PER HEAD-Rs.1645'
                      'AC3 TICKET COST PER HEAD-Rs.1165')
                print()
                print()
            
            #GKP LTT SF TRAIN GKP->MUMBAI
            def details_gkpltt_gkpmumbai():
                teem=timedelta(days=2)
                print()
                print()
                print(datetime.today())
                print('||--->GKP LTT SF EXP<---||')
                print('FROM GORAKHPUR JN ---->TO LOKMANYATILAK T')
                print('DEPARTURE',stdate,' 22:30-----ARRIVAL',(stdate+teem),' 04:35')
                print('JOURNEY DURATION--30HRS 05MIN')
                print('FREQUENCY-----EVERYDAY')
                print('AC2 TICKET COST PER HEAD-Rs.2645',end='/n'
                      'AC3 TICKET COST PER HEAD-Rs.1840')
                print()
                print()
            #GKP LTT SF TRAIN MUMBAI->GKP
            def details_gkpltt_mumbaigkp():
                teem=timedelta(days=2)
                print()
                print()
                print(datetime.today())
                print('||--->GKP LTT SF EXP<---||')
                print('FROM LOKMANYATILAK T ---->TO GORAKHPUR JN')
                print('DEPARTURE',stdate,' 05:23-----ARRIVAL',(stdate+teem),' 11:45')
                print('JOURNEY DURATION--30HRS 22MIN')
                print('FREQUENCY-----EVERYDAY')
                print('AC2 TICKET COST PER HEAD-Rs.2645',end='/n'
                      'AC3 TICKET COST PER HEAD-Rs.1840')
                print()
                print()
            
            #MMCT TEJAS RAJ TRAIN DELHI->MUMBAI
            def details_mmcttejasraj_delhimumbai():
                teem=timedelta(days=1)
                print()
                print()
                print(datetime.today())
                print('||--->MMCT TEJAS RAJ<---||')
                print('FROM NEW DELHI ---->TO LOKMANYATILAK T')
                print('DEPARTURE',stdate,' 16:55-----ARRIVAL',(stdate+teem),' 08:35')
                print('JOURNEY DURATION--15HRS 40MIN')
                print('FREQUENCY-----EVERYDAY')
                print('AC2 TICKET COST PER HEAD-Rs.4245',end='/n'
                      'AC3 TICKET COST PER HEAD-Rs.3085')
                print()
                print()
            
            #NDLS TEJAS RAJ TRAIN MUMBAI->DELHI
            def details_ndlstejasraj_mumbaidelhi():
                teem=timedelta(days=1)
                print()
                print()
                print(datetime.today())
                print('||--->NDLS TEJAS RAJ<---||')
                print('FROM MUMBAI CENTRAL ---->TO NEW DELHI')
                print('DEPARTURE',stdate,' 17:00-----ARRIVAL',(stdate+teem),' 08:32')
                print('JOURNEY DURATION--15HRS 32MIN')
                print('FREQUENCY-----EVERYDAY')
                print('AC2 TICKET COST PER HEAD-Rs.4245',end='/n'
                      'AC3 TICKET COST PER HEAD-Rs.3085')
                print()
                print()
            # BOOKING COST
            cost_booking_gorakhdham_ac2=0
            cost_booking_gorakhdham_ac3=0
            cost_booking_gkplttsf_ac2=0
            cost_booking_gkplttsf_ac3=0
            cost_booking_mmcttejas_ac2=0
            cost_booking_mmcttejas_ac3=0
            cost_booking_ndlstejas_ac2=0
            cost_booking_ndlstejas_ac3=0
            #FUNCTION TO INITIATE BOOKING GORAKHDHAM GKP->DELHI AC2
            def gorakhdham_gkpdelhi_ac2_book():
                global gorakhdham_gkpdelhi_ac2_bookedseat
                print('booking ticket')
                i=1
                global cost_booking_gorakhdham_ac2
                
                while i<=nopassenger:
                    gorakhdham_gkpdelhi_ac2_seattobebooked=gorakhdham_gkpdelhi_seatac2.pop()
                    gorakhdham_gkpdelhi_seatac2_bookedseat.append(gorakhdham_gkpdelhi_ac2_seattobebooked)
                    cost_booking_gorakhdham_ac2=cost_booking_gorakhdham_ac2+1645+1645*0.05
                    # GST INCLUDED IN CALCULATION
                    details_gorakhdham_gkpdelhi()
                    print('SEAT NUMBER',gorakhdham_gkpdelhi_ac2_seattobebooked,'HAS BEEN SUCESSFULLY BOOKED IN AC2 TIER')
                    print()      
                    i=i+1
                
            #FUNCTION TO INITIATE BOOKING GORAKHDHAM GKP->DELHI AC3
            def gorakhdham_gkpdelhi_ac3_book():
                global gorakhdham_gkpdelhi_ac3_bookedseat
                print('booking ticket')
                i=1
                global cost_booking_gorakhdham_ac3
                
                while i<=nopassenger:
                    gorakhdham_gkpdelhi_ac3_seattobebooked=gorakhdham_gkpdelhi_seatac3.pop()
                    gorakhdham_gkpdelhi_seatac3_bookedseat.append(gorakhdham_gkpdelhi_ac3_seattobebooked)
                    details_gorakhdham_gkpdelhi()
                    cost_booking_gorakhdham_ac3=cost_booking_gorakhdham_ac3+1165+1165*0.05
                    print('SEAT NUMBER',gorakhdham_gkpdelhi_ac3_seattobebooked,'HAS BEEN SUCESSFULLY BOOKED IN AC3 TIER')
                    print()
                    i=i+1
                 
            #FUNCTION TO INITIATE BOOKING GORAKHDHAM DELHI->GKP AC2
            def gorakhdham_delhigkp_ac2_book():
                global gorakhdham_delhigkp_ac2_bookedseat
                print('booking ticket')
                i=1
                global cost_booking_gorakhdham_ac2
                
                while i<=nopassenger:
                    gorakhdham_delhigkp_ac2_seattobebooked=gorakhdham_delhigkp_seatac2.pop()
                    gorakhdham_delhigkp_seatac2_bookedseat.append(gorakhdham_delhigkp_ac2_seattobebooked)
                    cost_booking_gorakhdham_ac2=cost_booking_gorakhdham_ac2+1645+1645*0.05
                    details_gorakhdham_delhigkp()
                    print('SEAT NUMBER',gorakhdham_delhigkp_ac2_seattobebooked,'HAS BEEN SUCESSFULLY BOOKED IN AC2 TIER')
                    print()
                    i=i+1
                
            
            #FUNCTION TO INITIATE BOOKING GORAKHDHAM DELHI->GKP AC3
            def gorakhdham_delhigkp_ac3_book():
                global gorakhdham_delhigkp_ac3_bookedseat
                print('booking ticket')
                i=1
                global cost_booking_gorakhdham_ac3
                
                while i<=nopassenger:
                    gorakhdham_delhigkp_ac3_seattobebooked=gorakhdham_delhigkp_seatac3.pop()
                    gorakhdham_delhigkp_seatac3_bookedseat.append(gorakhdham_delhigkp_ac3_seattobebooked)
                    cost_booking_gorakhdham_ac3=cost_booking_gorakhdham_ac3+1165+1165*0.05
                    details_gorakhdham_delhigkp()
                    print('SEAT NUMBER',gorakhdham_delhigkp_ac3_seattobebooked,'HAS BEEN SUCESSFULLY BOOKED IN AC3 TIER')
                    print()
                    i=i+1
                
                      
            #FUNCTION TO INITIATE BOOKING GKP LTT SF GKP->MUMBAI AC2
            def gorakhdham_gkpmumbai_ac2_book():
                global gorakhdham_gkpmumbai_ac2_bookedseat
                print('booking ticket')
                i=1
                global cost_booking_gkplttsf_ac2
                
                while i<=nopassenger:
                    gorakhdham_gkpmumbai_ac2_seattobebooked=gorakhdham_gkpmumbai_seatac2.pop()
                    gorakhdham_gkpmumbai_seatac2_bookedseat.append(gorakhdham_gkpmumbai_ac2_seattobebooked)
                    cost_booking_gkplttsf_ac2=cost_booking_gkplttsf_ac2+2645+2645*0.05
                    details_gkpltt_gkpmumbai()        
                    print('SEAT NUMBER',gorakhdham_gkpmumbai_ac2_seattobebooked,'HAS BEEN SUCESSFULLY BOOKED IN AC2 TIER')
                    print()
                    i=i+1
                
            
            #FUNCTION TO INITIATE BOOKING GKP LTT SF GKP->MUMBAI AC3
            def gorakhdham_gkpmumbai_ac3_book():
                global gorakhdham_gkpmumbai_ac3_bookedseat
                print('booking ticket')
                i=1
                global cost_booking_gkplttsf_ac3
                
                while i<=nopassenger:
                    gorakhdham_gkpmumbai_ac3_seattobebooked=gorakhdham_gkpmumbai_seatac3.pop()
                    gorakhdham_gkpmumbai_seatac3_bookedseat.append(gorakhdham_gkpmumbai_ac3_seattobebooked)
                    cost_booking_gkplttsf_ac3=cost_booking_gkplttsf_ac3+1840+1840*0.05
                    details_gkpltt_gkpmumbai()
                    print('SEAT NUMBER',gorakhdham_gkpmumbai_ac3_seattobebooked,'HAS BEEN SUCESSFULLY BOOKED IN AC3 TIER')
                    print()
                    i=i+1
                
            #FUNCTION TO INITIATE BOOKING GKP LTT SF MUMBAI->GKP AC2
            def gorakhdham_mumbaigkp_ac2_book():
                global gorakhdham_mumbaigkp_ac2_bookedseat
                print('booking ticket')
                i=1
                global cost_booking_gkplttsf_ac2
                
                while i<=nopassenger:
                    gorakhdham_mumbaigkp_ac2_seattobebooked=gorakhdham_mumbaigkp_seatac2.pop()
                    gorakhdham_mumbaigkp_seatac2_bookedseat.append(gorakhdham_mumbaigkp_ac2_seattobebooked)
                    cost_booking_gkplttsf_ac2=cost_booking_gkplttsf_ac2+2645+2645*0.05
                    details_gkpltt_mumbaigkp()
                    print('SEAT NUMBER',gorakhdham_mumbaigkp_ac2_seattobebooked,'HAS BEEN SUCESSFULLY BOOKED IN AC2 TIER')
                    print()
                    i=i+1
                 
                 
            #FUNCTION TO INITIATE BOOKING GKP LTT SF MUMBAI->GKP AC3
            def gorakhdham_mumbaigkp_ac3_book():
                global gorakhdham_mumbaigkp_ac3_bookedseat
                print('booking ticket')
                i=1
                global cost_booking_gkplttsf_ac3
                
                while i<=nopassenger:
                    gorakhdham_mumbaigkp_ac3_seattobebooked=gorakhdham_mumbaigkp_seatac3.pop()
                    gorakhdham_mumbaigkp_seatac3_bookedseat.append(gorakhdham_mumbaigkp_ac3_seattobebooked)
                    cost_booking_gkplttsf_ac3=cost_booking_gkplttsf_ac3+1840+1840*0.05
                    details_gkpltt_mumbaigkp()
                    print('SEAT NUMBER',gorakhdham_mumbaigkp_ac3_seattobebooked,'HAS BEEN SUCESSFULLY BOOKED IN AC3 TIER')
                    print()
                    i=i+1
                    
            #FUNCTION TO INITIATE BOOKING MMCT TEJAS RAJ DELHI->MUMBAI AC2
            def gorakhdham_delhimumbai_ac2_book():
                global gorakhdham_delhimumbai_ac2_bookedseat
                print('booking ticket')
                i=1
                global cost_booking_mmcttejas_ac2
                
                while i<=nopassenger:
                    gorakhdham_delhimumbai_ac2_seattobebooked=gorakhdham_delhimumbai_seatac2.pop()
                    gorakhdham_delhimumbai_seatac2_bookedseat.append(gorakhdham_delhimumbai_ac2_seattobebooked)
                    cost_booking_mmcttejas_ac2=cost_booking_mmcttejas_ac2+4245+4245*0.05
                    details_mmcttejasraj_delhimumbai()
                    print('SEAT NUMBER',gorakhdham_delhimumbai_ac2_seattobebooked,'HAS BEEN SUCESSFULLY BOOKED IN AC2 TIER')
                    print()
                    i=i+1
                    
            #FUNCTION TO INITIATE BOOKING MMTC TEJAS RAJ DELHI->MUMBAI AC3
            def gorakhdham_delhimumbai_ac3_book():
                global gorakhdham_delhimumbai_ac3_bookedseat
                print('booking ticket')
                i=1
                global cost_booking_mmcttejas_ac3
                
                while i<=nopassenger:
                    gorakhdham_delhimumbai_ac3_seattobebooked=gorakhdham_delhimumbai_seatac3.pop()
                    gorakhdham_delhimumbai_seatac3_bookedseat.append(gorakhdham_delhimumbai_ac3_seattobebooked)
                    cost_booking_mmcttejas_ac3=cost_booking_mmcttejas_ac3+3085+3085*0.05
                    details_mmcttejasraj_delhimumbai()
                    print('SEAT NUMBER',gorakhdham_delhimumbai_ac3_seattobebooked,'HAS BEEN SUCESSFULLY BOOKED IN AC3 TIER')
                    print()
                    i=i+1
                
                    
            #FUNCTION TO INITIATE BOOKING NDLS TEJAS RAJ MUMBAI->DELHI AC2
            def gorakhdham_mumbaidelhi_ac2_book():
                global gorakhdham_mumbaigkp_ac2_bookedseat
                print('booking ticket')
                i=1
                global cost_booking_ndlstejas_ac2
                
                while i<=nopassenger:
                    gorakhdham_mumbaidelhi_ac2_seattobebooked=gorakhdham_mumbaidelhi_seatac2.pop()
                    gorakhdham_mumbaidelhi_seatac2_bookedseat.append(gorakhdham_mumbaidelhi_ac2_seattobebooked)
                    cost_booking_ndlstejas_ac2=cost_booking_ndlstejas_ac2+4245+4245*0.05
                    details_ndlstejasraj_mumbaidelhi()
                    print('SEAT NUMBER',gorakhdham_mumbaidelhi_ac2_seattobebooked,'HAS BEEN SUCESSFULLY BOOKED IN AC2 TIER')
                    print()
                    i=i+1
                     
            #FUNCTION TO INITIATE BOOKING NDLS TEJAS RAJ MUMBAI->DELHI AC3
            def gorakhdham_mumbaidelhi_ac3_book():
                global gorakhdham_mumbaidelhi_ac3_bookedseat
                print('booking ticket')
                i=1
                global cost_booking_ndlstejas_ac3
                
                while i<=nopassenger:
                    gorakhdham_mumbaidelhi_ac3_seattobebooked=gorakhdham_mumbaidelhi_seatac3.pop()
                    gorakhdham_mumbaidelhi_seatac3_bookedseat.append(gorakhdham_mumbaidelhi_ac3_seattobebooked)
                    cost_booking_ndlstejas_ac3=cost_booking_ndlstejas_ac3+3085+3085*0.05
                    details_ndlstejasraj_mumbaidelhi()
                    print('SEAT NUMBER',gorakhdham_mumbaidelhi_ac3_seattobebooked,'HAS BEEN SUCESSFULLY BOOKED IN AC3 TIER')
                    print()
                    i=i+1 
                           
            #TRAIN FOR DELHI AND GORAKHPUR ROUTE
            def gkpdelhitrains(stlo):
                global clas
                global nopassenger
                global cost_booking_gorakhdham_ac2
                global cost_booking_gorakhdham_ac3
            #GORAKHPUR--->DELHI TRAIN
                if stlo=='GORAKHPUR':
                    #DETAILS OF TRAIN
                    details_gorakhdham_gkpdelhi()
                    CLASSAVAIL=['AC2','AC3']
                    if clas in CLASSAVAIL:
                        print('REQUIRED CLASS AVAILABLE')
                        if clas=='AC2':
                            gorakhdham_gkpdelhi_ac2_book()
                            furtheroption()
                            while option!=3:
                                if option==1: 
                                    nopassenger=int(input('no of passenger'))
                                    if (len(gorakhdham_gkpdelhi_seatac2)-nopassenger)>=0:
                                     gorakhdham_gkpdelhi_ac2_book()
                                    else :
                                        print('SEATS NOT AVAILABLE')
                                else :
                                    print('CANCELLING BOOKING')
                                    gorakhdham_gkpdelhi_ac2_seattoberemoved=int(input('PRINT SEAT NUMBER TO BE CANCELED'))
                                    if gorakhdham_gkpdelhi_ac2_seattoberemoved in gorakhdham_gkpdelhi_seatac2_bookedseat:
                                        gorakhdham_gkpdelhi_seatac2_bookedseat.remove(gorakhdham_gkpdelhi_ac2_seattoberemoved)
                                        gorakhdham_gkpdelhi_seatac2.append(gorakhdham_gkpdelhi_ac2_seattoberemoved)
                                        details_gorakhdham_gkpdelhi()
                                        print('SEAT NUMBER',gorakhdham_gkpdelhi_ac2_seattoberemoved,'HAS BEEN SUCESSFULL CANCELED')
                                        cost_booking_gorakhdham_ac2=cost_booking_gorakhdham_ac2-1645
                                    else:
                                        print('invalid')
                                furtheroption()
                            print('TOTAL COST OF BOOKING Rs',cost_booking_gorakhdham_ac2)
                            print('ALL THE PRICES ARE SUBJECTED TO 5% GST,ACCORDING TO GOVERNMENT OF INDIA RULES AND REGULATIONS')
                        elif clas=='AC3':
                            gorakhdham_gkpdelhi_ac3_book()
                            furtheroption()
                            while option!=3:
                                if option==1: 
                                    nopassenger=int(input('no of passenger'))
                                    if (len(gorakhdham_gkpdelhi_seatac3)-nopassenger)>=0:
                                     gorakhdham_gkpdelhi_ac3_book()
                                    else :
                                        print('SEATS NOT AVAILABLE')
                                else :
                                    print('CANCELLING BOOKING')
                                    gorakhdham_gkpdelhi_ac3_seattoberemoved=int(input('PRINT SEAT NUMBER TO BE CANCELED'))
                                    if gorakhdham_gkpdelhi_ac3_seattoberemoved in gorakhdham_gkpdelhi_seatac3_bookedseat:
                                        gorakhdham_gkpdelhi_seatac3_bookedseat.remove(gorakhdham_gkpdelhi_ac3_seattoberemoved)
                                        gorakhdham_gkpdelhi_seatac3.append(gorakhdham_gkpdelhi_ac3_seattoberemoved)
                                        details_gorakhdham_gkpdelhi()
                                        print('SEAT NUMBER',gorakhdham_gkpdelhi_ac3_seattoberemoved,'HAS BEEN SUCESSFULL CANCELED')
                                        cost_booking_gorakhdham_ac3=cost_booking_gorakhdham_ac3-1165
                                    else:
                                        print('invalid')
                                furtheroption()
                            print('TOTAL COST OF BOOKING Rs',cost_booking_gorakhdham_ac3)
                            print('ALL THE PRICES ARE SUBJECTED TO 5% GST,ACCORDING TO GOVERNMENT OF INDIA RULES AND REGULATIONS')
                        else:
                            pass
                        
                    else :
                        print('SORRY,THE REQUESTED CLASS IS NOT AVAILABLE')
                        print('PRESS 1 TO CHANGE CLASS ')
                        print('PRESS 2 TO TERMINATE BOOKING')
                        classoption=int(input('CHOICE='))
                        if classoption==1:
                            clas=str(input("Enter class(eg AC2 for AC second tier)"))
                            gkpdelhitrains(stlo)
                        elif classoption==2:
                            pass
                        else:
                            print('INVALID DATA ENTRY')
                elif stlo=='NEW DELHI':
            
            #TRAIN FROM DELHI TO GORAKHPUR
                    details_gorakhdham_delhigkp()      
                    CLASSAVAIL=['AC2','AC3']
                    if clas in CLASSAVAIL:
                        print('REQUIRED CLASS AVAILABLE')
                        if clas=='AC2':
                                
                            gorakhdham_delhigkp_ac2_book()
                            furtheroption()
                            while option!=3:
                                if option==1: 
                                    nopassenger=int(input('no of passenger'))
                                    if (len(gorakhdham_delhigkp_seatac2)-nopassenger)>=0:
                                     gorakhdham_delhigkp_ac2_book()
                                    else :
                                        print('SEATS NOT AVAILABLE')
                                else :
                                    print('CANCELLING BOOKING')
                                    gorakhdham_delhigkp_ac2_seattoberemoved=int(input('PRINT SEAT NUMBER TO BE CANCELED'))
                                    if gorakhdham_delhigkp_ac2_seattoberemoved in gorakhdham_delhigkp_seatac2_bookedseat:
                                        gorakhdham_delhigkp_seatac2_bookedseat.remove(gorakhdham_delhigkp_ac2_seattoberemoved)
                                        gorakhdham_delhigkp_seatac2.append(gorakhdham_delhigkp_ac2_seattoberemoved)
                                        details_gorakhdham_delhigkp()
                                        print('SEAT NUMBER',gorakhdham_delhigkp_ac2_seattoberemoved,'HAS BEEN SUCESSFULL CANCELED')
                                        cost_booking_gorakhdham_ac2=cost_booking_gorakhdham_ac2-1645
                                    else:
                                        print('invalid')
                                furtheroption()
                            print('TOTAL COST OF BOOKING Rs',cost_booking_gorakhdham_ac2)
                            print('ALL THE PRICES ARE SUBJECTED TO 5% GST,ACCORDING TO GOVERNMENT OF INDIA RULES AND REGULATIONS')
                        elif clas=='AC3':
                            gorakhdham_delhigkp_ac3_book()
                            furtheroption()
                            while option!=3:
                                if option==1: 
                                    nopassenger=int(input('no of passenger'))
                                    if (len(gorakhdham_delhigkp_seatac3)-nopassenger)>=0:
                                     gorakhdham_delhigkp_ac3_book()
                                    else :
                                        print('SEATS NOT AVAILABLE')
                                else :
                                    print('CANCELLING BOOKING')
                                    gorakhdham_delhigkp_ac3_seattoberemoved=int(input('PRINT SEAT NUMBER TO BE CANCELED'))
                                    if gorakhdham_delhigkp_ac3_seattoberemoved in gorakhdham_delhigkp_seatac3_bookedseat:
                                        gorakhdham_delhigkp_seatac3_bookedseat.remove(gorakhdham_delhigkp_ac3_seattoberemoved)
                                        gorakhdham_delhigkp_seatac3.append(gorakhdham_delhigkp_ac3_seattoberemoved)
                                        details_gorakhdham_delhigkp()
                                        print('SEAT NUMBER',gorakhdham_delhigkp_ac3_seattoberemoved,'HAS BEEN SUCESSFULL CANCELED')
                                        cost_booking_gorakhdham_ac3=cost_booking_gorakhdham_ac2-1165
                                    else:
                                        print('invalid')
                                furtheroption()
                            print('TOTAL COST OF BOOKING Rs',cost_booking_gorakhdham_ac3)
                            print('ALL THE PRICES ARE SUBJECTED TO 5% GST,ACCORDING TO GOVERNMENT OF INDIA RULES AND REGULATIONS')
                        else:
                            pass
                        
                    
                    else :
                        print('SORRY,THE REQUESTED CLASS IS NOT AVAILABLE')
                        print('PRESS 1 TO CHANGE CLASS ')
                        print('PRESS 2 TO TERMINATE BOOKING')
                        classoption=int(input('CHOICE='))
                        if classoption==1:
                            clas=str(input("Enter class(eg AC2 for AC second tier)"))
                            gkpdelhitrains(stlo)
                        elif classoption==2:
                            pass
                        else:
                            print('INVALID DATA ENTRY')
            
            #TRAINS ON GORAKHPUR MUMBAI ROUTE
                    
            def gkpmumbaitrains(stlo):
                global cost_booking_gkplttsf_ac2
                global cost_booking_gkplttsf_ac3
                global nopassenger
                global clas
                if stlo=='GORAKHPUR':
                    details_gkpltt_gkpmumbai()
                    CLASSAVAIL=['AC2','AC3']
                    if clas in CLASSAVAIL:
                        print('REQUIRED CLASS AVAILABLE')
                        if clas=='AC2':
                            
                            gorakhdham_gkpmumbai_ac2_book()
                            furtheroption()
                            while option!=3:
                                if option==1: 
                                    nopassenger=int(input('no of passenger'))
                                    if (len(gorakhdham_gkpmumbai_seatac2)-nopassenger)>=0:
                                     gorakhdham_gkpmumbai_ac2_book()
                                    else :
                                        print('SEATS NOT AVAILABLE')
                                elif option==2 :
                                    print('CANCELLING BOOKING')
                                    gorakhdham_gkpmumbai_ac2_seattoberemoved=int(input('PRINT SEAT NUMBER TO BE CANCELED'))
                                    if gorakhdham_gkpmumbai_ac2_seattoberemoved in gorakhdham_gkpmumbai_seatac2_bookedseat:
                                        gorakhdham_gkpmumbai_seatac2_bookedseat.remove(gorakhdham_gkpmumbai_ac2_seattoberemoved)
                                        gorakhdham_gkpmumbai_seatac2.append(gorakhdham_gkpmumbai_ac2_seattoberemoved)
                                        details_gkpltt_gkpmumbai()
                                        print('SEAT NUMBER',gorakhdham_gkpmumbai_ac2_seattoberemoved,'HAS BEEN SUCESSFULL CANCELED')
                                        cost_booking_gkplttsf_ac2=cost_booking_gkplttsf_ac2-2645
                                    else:
                                        print('invalid')
                                else:
                                    print('INVALID')
                                    break                       
                                furtheroption()
                            print('TOTAL COST OF BOOKING Rs',cost_booking_gkplttsf_ac2)
                            print('ALL THE PRICES ARE SUBJECTED TO 5% GST,ACCORDING TO GOVERNMENT OF INDIA RULES AND REGULATIONS')
                        elif clas=='AC3':
                            gorakhdham_gkpmumbai_ac3_book()
                            furtheroption()
                            while option!=3:
                                if option==1: 
                                    nopassenger=int(input('no of passenger'))
                                    if (len(gorakhdham_gkpmumbai_seatac3)-nopassenger)>=0:
                                     gorakhdham_gkpmumbai_ac3_book()
                                    else :
                                        print('SEATS NOT AVAILABLE')
                                elif option==2 :
                                    print('CANCELLING BOOKING')
                                    gorakhdham_gkpmumbai_ac3_seattoberemoved=int(input('PRINT SEAT NUMBER TO BE CANCELED'))
                                    if gorakhdham_gkpmumbai_ac3_seattoberemoved in gorakhdham_gkpmumbai_seatac3_bookedseat:
                                        gorakhdham_gkpmumbai_seatac3_bookedseat.remove(gorakhdham_gkpmumbai_ac3_seattoberemoved)
                                        gorakhdham_gkpmumbai_seatac3.append(gorakhdham_gkpmumbai_ac3_seattoberemoved)
                                        details_gkpltt_gkpmumbai()
                                        print('SEAT NUMBER',gorakhdham_gkpmumbai_ac3_seattoberemoved,'HAS BEEN SUCESSFULL CANCELED')
                                        cost_booking_gkplttsf_ac3=cost_booking_gkplttsf_ac3-1840
                                    else:
                                        print('invalid')
                                else:
                                    print('INVALID')
                                    break
                                furtheroption()
                            print('TOTAL COST OF BOOKING Rs',cost_booking_gkplttsf_ac3)
                            print('ALL THE PRICES ARE SUBJECTED TO 5% GST,ACCORDING TO GOVERNMENT OF INDIA RULES AND REGULATIONS')
                        else:
                            pass
                        
                       
                    else :
                        print('SORRY,THE REQUESTED CLASS IS NOT AVAILABLE')
                        print('PRESS 1 TO CHANGE CLASS ')
                        print('PRESS 2 TO TERMINATE BOOKING')
                        classoption=int(input('CHOICE='))
                        if classoption==1:
                            clas=str(input("Enter class(eg AC2 for AC second tier)"))
                            gkpmumbaitrains(stlo)
                        elif classoption==2 :
                            pass
                        else:
                            print('INVALID DATA ENTRY')
                elif stlo=='MUMBAI':
            #TRAIN FROM MUMBAI TO GKP
                    details_gkpltt_mumbaigkp()
                    CLASSAVAIL=['AC2','AC3']
                    if clas in CLASSAVAIL:
                        print('REQUIRED CLASS AVAILABLE')
                        if clas=='AC2':   
                                gorakhdham_mumbaigkp_ac2_book()
                                furtheroption()
                                while option!=3:
                                    if option==1: 
                                        nopassenger=int(input('no of passenger'))
                                        if (len(gorakhdham_mumbaigkp_seatac2)-nopassenger)>=0:
                                         gorakhdham_mumbaigkp_ac2_book()
                                        else :
                                            print('SEATS NOT AVAILABLE')
                                    elif option==2 :
                                        print('CANCELLING BOOKING')
                                        gorakhdham_mumbaigkp_ac2_seattoberemoved=int(input('PRINT SEAT NUMBER TO BE CANCELED'))
                                        if gorakhdham_mumbaigkp_ac2_seattoberemoved in gorakhdham_mumbaigkp_seatac2_bookedseat:
                                            gorakhdham_mumbaigkp_seatac2_bookedseat.remove(gorakhdham_mumbaigkp_ac2_seattoberemoved)
                                            gorakhdham_mumbaigkp_seatac2.append(gorakhdham_mumbaigkp_ac2_seattoberemoved)
                                            details_gkpltt_mumbaigkp()
                                            print('SEAT NUMBER',gorakhdham_mumbaigkp_ac2_seattoberemoved,'HAS BEEN SUCESSFULL CANCELED')
                                            cost_booking_gkplttsf_ac2=cost_booking_gkplttsf_ac2-2645
                                        else:
                                            print('invalid')
                                    else:
                                        print('INVALID')
                                        break
                                    furtheroption()
                                print('TOTAL COST OF BOOKING Rs',cost_booking_gkplttsf_ac2)
                                print('ALL THE PRICES ARE SUBJECTED TO 5% GST,ACCORDING TO GOVERNMENT OF INDIA RULES AND REGULATIONS')
                        elif clas=='AC3':
                                gorakhdham_mumbaigkp_ac3_book()
                                furtheroption()
                                while option!=3:
                                    if option==1: 
                                        nopassenger=int(input('no of passenger'))
                                        if (len(gorakhdham_mumbaigkp_seatac3)-nopassenger)>=0:
                                         gorakhdham_mumbaigkp_ac3_book()
                                        else :
                                            print('SEATS NOT AVAILABLE')
                                    elif option==2 :
                                        print('CANCELLING BOOKING')
                                        gorakhdham_mumbaigkp_ac3_seattoberemoved=int(input('PRINT SEAT NUMBER TO BE CANCELED'))
                                        if gorakhdham_mumbaigkp_ac3_seattoberemoved in gorakhdham_mumbaigkp_seatac3_bookedseat:
                                            gorakhdham_mumbaigkp_seatac3_bookedseat.remove(gorakhdham_mumbaigkp_ac3_seattoberemoved)
                                            gorakhdham_mumbaigkp_seatac3.append(gorakhdham_mumbaigkp_ac3_seattoberemoved)
                                            details_gkpltt_mumbaigkp()
                                            print('SEAT NUMBER',gorakhdham_mumbaigkp_ac3_seattoberemoved,'HAS BEEN SUCESSFULL CANCELED')
                                            cost_booking_gkplttsf_ac3=cost_booking_gkplttsf_ac3-1840
                                        else:
                                            print('invalid')
                                    else:
                                        print('INVALID')
                                        break
                                    furtheroption()
                                print('TOTAL COST OF BOOKING Rs',cost_booking_gkplttsf_ac3)
                                print('ALL THE PRICES ARE SUBJECTED TO 5% GST,ACCORDING TO GOVERNMENT OF INDIA RULES AND REGULATIONS')
                        else:
                            pass            
                    else :
                        print('SORRY,THE REQUESTED CLASS IS NOT AVAILABLE')
                        print('PRESS 1 TO CHANGE CLASS ')
                        print('PRESS 2 TO TERMINATE BOOKING')
                        classoption=int(input('CHOICE='))
                        if classoption==1:
                            clas=str(input("Enter class(eg AC2 for AC second tier)"))
                            gkpmumbaitrains(stlo)
                        elif classoption==2:
                            pass
                        else:
                            print('INVALID DATA ENTRY')
            
            #TRAIN ON NEW DELHI MUMBAI ROUTE
            
            def delhimumbaitrains(stlo):
                global nopassenger
                global cost_booking_mmcttejas_ac3
                global cost_booking_mmcttejas_ac2
                global cost_booking_ndlstejas_ac2
                global cost_booking_ndlstejas_ac3
                global clas
                if stlo=='NEW DELHI':
                    details_mmcttejasraj_delhimumbai()
                    CLASSAVAIL=['AC2','AC3']
                    if clas in CLASSAVAIL:
                        print('REQUIRED CLASS AVAILABLE')
                        if clas=='AC2': 
                            gorakhdham_delhimumbai_ac2_book()
                            furtheroption()
                            while option!=3:
                                if option==1: 
                                    nopassenger=int(input('no of passenger'))
                                    if (len(gorakhdham_delhimumbai_seatac2)-nopassenger)>=0:
                                     gorakhdham_delhimumbai_ac2_book()
                                    else :
                                        print('SEATS NOT AVAILABLE')
                                elif option==2 :
                                    print('CANCELLING BOOKING')
                                    gorakhdham_delhimumbai_ac2_seattoberemoved=int(input('PRINT SEAT NUMBER TO BE CANCELED'))
                                    if gorakhdham_delhimumbai_ac2_seattoberemoved in gorakhdham_delhimumbai_seatac2_bookedseat:
                                        gorakhdham_delhimumbai_seatac2_bookedseat.remove(gorakhdham_delhimumbai_ac2_seattoberemoved)
                                        gorakhdham_delhimumbai_seatac2.append(gorakhdham_delhimumbai_ac2_seattoberemoved)
                                        details_mmcttejasraj_delhimumbai()
                                        print('SEAT NUMBER',gorakhdham_delhimumbai_ac2_seattoberemoved,'HAS BEEN SUCESSFULL CANCELED')
                                        cost_booking_mmcttejas_ac2=cost_booking_mmcttejas_ac2-4245
                                    else:
                                        print('invalid')
                                else:
                                    print('INVALID')
                                    break
                                furtheroption()
                            print('TOTAL COST OF BOOKING Rs',cost_booking_mmcttejas_ac2)
                            print('ALL THE PRICES ARE SUBJECTED TO 5% GST,ACCORDING TO GOVERNMENT OF INDIA RULES AND REGULATIONS')
                                
                        elif clas=='AC3':
                            gorakhdham_delhimumbai_ac3_book()
                            furtheroption()
                            while option!=3:
                                if option==1: 
                                    nopassenger=int(input('no of passenger'))
                                    if (len(gorakhdham_delhimumbai_seatac3)-nopassenger)>=0:
                                     gorakhdham_delhimumbai_ac3_book()
                                    else :
                                        print('SEATS NOT AVAILABLE')
                                elif option==2 :
                                    print('CANCELLING BOOKING')
                                    gorakhdham_delhimumbai_ac3_seattoberemoved=int(input('PRINT SEAT NUMBER TO BE CANCELED'))
                                    if gorakhdham_delhimumbai_ac3_seattoberemoved in gorakhdham_delhimumbai_seatac3_bookedseat:
                                        gorakhdham_delhimumbai_seatac3_bookedseat.remove(gorakhdham_delhimumbai_ac3_seattoberemoved)
                                        gorakhdham_delhimumbai_seatac3.append(gorakhdham_delhimumbai_ac3_seattoberemoved)
                                        details_mmcttejasraj_delhimumbai()
                                        print('SEAT NUMBER',gorakhdham_delhimumbai_ac3_seattoberemoved,'HAS BEEN SUCESSFULL CANCELED')
                                        cost_booking_mmcttejas_ac3=cost_booking_mmcttejas_ac3-3085
                                    else:
                                        print('invalid')
                                else:
                                    print('INVALID')
                                    break
                                furtheroption()
                            print('TOTAL COST OF BOOKING Rs',cost_booking_mmcttejas_ac3)
                            print('ALL THE PRICES ARE SUBJECTED TO 5% GST,ACCORDING TO GOVERNMENT OF INDIA RULES AND REGULATIONS')
                        else:
                            pass           
                    else :
                        print('SORRY,THE REQUESTED CLASS IS NOT AVAILABLE')
                        print('PRESS 1 TO CHANGE CLASS ')
                        print('PRESS 2 TO TERMINATE BOOKING')
                        classoption=int(input('CHOICE='))
                        if classoption==1:
                            clas=str(input("Enter class(eg AC2 for AC second tier)"))
                            delhimumbaitrains(stlo)
                        elif classoption==2:
                            pass
                        else:
                            print('INVALID DATA ENTRY')
                            
                elif stlo=='MUMBAI':               
            #TRAIN ON MUMBAI DELHI ROUTE                       
                    details_ndlstejasraj_mumbaidelhi()
                    CLASSAVAIL=['AC2','AC3']
                    if clas in CLASSAVAIL:
                        print('REQUIRED CLASS AVAILABLE')
                        if clas=='AC2':            
                            gorakhdham_mumbaidelhi_ac2_book()
                            furtheroption()
                            while option!=3:
                                if option==1: 
                                    nopassenger=int(input('no of passenger'))
                                    if (len(gorakhdham_mumbaidelhi_seatac2)-nopassenger)>=0:
                                        gorakhdham_mumbaidelhi_ac2_book()
                                    else :
                                        print('SEATS NOT AVAILABLE')
                                elif option==2 :
                                    print('CANCELLING BOOKING')
                                    gorakhdham_mumbaidelhi_ac2_seattoberemoved=int(input('PRINT SEAT NUMBER TO BE CANCELED'))
                                    if gorakhdham_mumbaidelhi_ac2_seattoberemoved in gorakhdham_mumbaidelhi_seatac2_bookedseat:
                                        gorakhdham_mumbaidelhi_seatac2_bookedseat.remove(gorakhdham_mumbaidelhi_ac2_seattoberemoved)
                                        gorakhdham_mumbaidelhi_seatac2.append(gorakhdham_mumbaidelhi_ac2_seattoberemoved)
                                        details_ndlstejasraj_mumbaidelhi()
                                        print('SEAT NUMBER',gorakhdham_mumbaidelhi_ac2_seattoberemoved,'HAS BEEN SUCESSFULL CANCELED')
                                        cost_booking_ndlstejas_ac2=cost_booking_ndlstejas_ac2-4245
                                    else:
                                        print('invalid')
                                else:
                                    print('INVALID')
                                    break
                                furtheroption()
                            print('TOTAL COST OF BOOKING Rs',cost_booking_ndlstejas_ac2)
                            print('ALL THE PRICES ARE SUBJECTED TO 5% GST,ACCORDING TO GOVERNMENT OF INDIA RULES AND REGULATIONS')
                                    
                        elif clas=='AC3':
                                gorakhdham_mumbaidelhi_ac3_book()
                                furtheroption()
                                while option!=3:
                                    if option==1: 
                                        nopassenger=int(input('no of passenger'))
                                        if (len(gorakhdham_mumbaidelhi_seatac3)-nopassenger)>=0:
                                         gorakhdham_mumbaidelhi_ac3_book()
                                        else :
                                            print('SEATS NOT AVAILABLE')
                                    elif option==2 :
                                        print('CANCELLING BOOKING')
                                        gorakhdham_mumbaidelhi_ac3_seattoberemoved=int(input('PRINT SEAT NUMBER TO BE CANCELED'))
                                        if gorakhdham_mumbaidelhi_ac3_seattoberemoved in gorakhdham_mumbaidelhi_seatac3_bookedseat:
                                            gorakhdham_mumbaidelhi_seatac3_bookedseat.remove(gorakhdham_mumbaidelhi_ac3_seattoberemoved)
                                            gorakhdham_mumbaidelhi_seatac3.append(gorakhdham_mumbaidelhi_ac3_seattoberemoved)
                                            details_ndlstejasraj_mumbaidelhi()
                                            print('SEAT NUMBER',gorakhdham_mumbaidelhi_ac3_seattoberemoved,'HAS BEEN SUCESSFULL CANCELED')
                                            cost_booking_ndlstejas_ac3=cost_booking_ndlstejas_ac3-3085
                                        else:
                                            print('invalid')
                                    else:
                                        print('INVALID')
                                        break
                                    furtheroption()
                                print('TOTAL COST OF BOOKING Rs',cost_booking_ndlstejas_ac3,)
                                print('ALL THE PRICES ARE SUBJECTED TO 5% GST,ACCORDING TO GOVERNMENT OF INDIA RULES AND REGULATIONS')
            
                        else:
                            pass               
                else :
                    print('SORRY,THE REQUESTED CLASS IS NOT AVAILABLE')
                    print('PRESS 1 TO CHANGE CLASS ')
                    print('PRESS 2 TO TERMINATE BOOKING')
                    classoption=int(input('CHOICE='))
                    if classoption==1:
                        clas=str(input("Enter class(eg AC2 for AC second tier)"))
                        delhimumbaitrains(stlo)
                    elif classoption==2:
                        pass
                    else:
                        print('INVALID DATA ENTRY')
            # FUNCTION TO GIVE RESULTS ACCORDING TO STATIONS SPECIFIED BY USER
            def bookinginitial():
                journeydetails()
                if stlo in ['NEW DELHI','GORAKHPUR'] and enlo in ['NEW DELHI','GORAKHPUR'] :
                    gkpdelhitrains(stlo)
                elif stlo in ['NEW DELHI','MUMBAI'] and enlo in ['NEW DELHI','MUMBAI']:
                    delhimumbaitrains(stlo)
                elif stlo in ['MUMBAI','GORAKHPUR'] and enlo in ['MUMBAI','GORAKHPUR']:
                    gkpmumbaitrains(stlo)
                else:
                    print('invalid')
            #MAIN PROGRAM
            bookinginitial()

            create_railways_table(cursor)
            if (stlo=="GORAKHPUR" and enlo=="NEW DELHI") or (stlo=="NEW DELHI" and enlo=="GORAKHPUR"):
                if clas=='AC2':
                    add_railuser(username,"Railways",DisGkpdel,clas,cost_booking_gorakhdham_ac2)
                elif clas=='AC3':
                    add_railuser(username,"Railways",DisGkpdel,clas,cost_booking_gorakhdham_ac3)                   
            if (stlo=="MUMBAI" and enlo=="GORAKHPUR" and stlo=="GORAKHPUR" or enlo=="MUMBAI"):
                if clas=='AC2':
                    add_railuser(username,"Railways",DisGkpmum,clas,cost_booking_gkplttsf_ac2)
                elif clas=='AC3':
                    add_railuser(username,"Railways",DisGkpmum,clas,cost_booking_gkplttsf_ac3)
            if (enlo=="MUMBAI" and stlo=="NEW DELHI"):
                if clas=='AC2':
                    add_railuser(username,"Railways",DisDelmum,clas,cost_booking_mmcttejas_ac2)
                elif clas=='AC3':
                    add_railuser(username,"Railways",DisDelmum,clas,cost_booking_mmcttejas_ac3)
            else(stlo=='MUMBAI' and enlo=='NEW DELHI'):
                if clas=='AC2':
                    add_railuser(username,"Railways",DisMumdel,clas,cost_booking_ndlstejas_ac2)
                elif clas=='AC3':
                    add_railuser(username,"Railways",DisMumdel,clas,cost_booking_ndlstejas_ac3)
               
        if Mode=="Bus":
            def distane():                              #calculate distance between the source and final location
                lo1=str(input('Starting Location='))
                lo2=str(input('End Location='))
                geocoder=Nominatim(user_agent='test code')
                coordi1=geocoder.geocode(lo1)
                coordi2=geocoder.geocode(lo2)
                lat1,long1=(coordi1.latitude),(coordi2.longitude)
                lat2,long2=(coordi2.latitude),(coordi2.longitude)
                place1=(lat1,long1)
                place2=(lat2,long2)
                aa=(distance.distance(place1,place2))
                aa=str(aa)
                aa=aa.replace('km','')
                aa=int(float(aa))
                return aa
            def passenger():                            #func to count no of passenger
                passe=int(input("No. of passengers"))
                return(passe)
            buss={1:'AC2x2',2:'AC2x2',3:'AC3x2',4:'AC3x2',5:'ACsleeper',6:'NONAC2x2',7:'NONAC3x2',8:'Traveller35',9:'Traveller30'}  #Bus garage
            buscharge={'AC2x2':3000,'AC3x2':5000,'ACsleeper':5000,'NONAC2x2':2500,'NONAC3x2':3000,'Traveller35':2100,'Traveller30':2000}    #fixed maintainence cost
            def upbus(b):                               #update bus availability
                length=len(buss)
                for i in range(1,length+1):
                    if buss[i]==b:
                        buss[i]=''
                        return('Yes,bus',b,'is available')
                    else:
                        return('Sorry, bus',b,' is not available')    
            def luxor():                                #to check luxory requirements of customer
                print('Press 1 to avail AC Buses')
                print('Press 2 to avail NONAC Buses')
                checkac=int(input('option='))
                return(checkac)

            def availbuses():                     #func to determine requirement of buses according to no. of passengers 
                num=luxor()
                nop=passenger()
                global maintainence
                if nop<=35:
                    print("suggestive options: press 1 for Traveller35 ")
                    print("press 2 for Traveller30")
                    cuso= int(input("option (GIVE INTEGRAL INPUT ONLY )"))
                    if cuso==1:
                        upbus('Travller35')
                        maintainence=buscharge['Traveller35']
                    else:
                        upbus('Traveller30')
                        maintainence=buscharge['Traveller30']
                elif nop>35 and nop<=45:
                    if num==1:
                        print("suggestive options: press 1 for Traveller35 and Traveller30 ")
                        print("press 2 for AC2x2")
                        print('press 3 for ACsleeper')
                        cuso= int(input("option"))
                        if cuso==1:
                            upbus('Traveller35')
                            upbus('Traveller30')
                            maintainence=buscharge['Traveller35']+buscharge['Traveeller30']
                        elif cuso==2:
                            upbus('AC2x2')
                            maintainence=buscharge['AC2x2']
                        else:
                            upbus('ACsleeper')
                            maintainence=buscharge['ACsleeper']
                    elif num==2:
                        print('suggestive options: NONAC2x2 buses')
                        upbus('NONAC2x2')
                        maintainence=buscharge['NONAC2x2']
                elif nop>45 and nop<=50:
                    if num==1:
                        print("suggestive options:Press 1 for AC3x2")
                        print('Press 2 for ACsleeper')
                        print('Press 3 for Traveller35 and Traveller30')
                        cuso= int(input("option"))
                        if cuso==1:
                            upbus('AC3x2')
                            maintainence=buscharge['AC3x2']
                        elif cuso==2:
                            upbus('ACsleeper')
                            maintainence=buscharge['ACsleeper']
                        else :
                            upbus('Traveller35')
                            upbus('Traveller30')
                            maintainence=buscharge['Traveller35']+buscharge['Traveller30']
                    else :
                        print('suggestive options: NONAC3x2 buses')
                        upbus('NONAC3x2')
                        maintainence=buscharge['NONAC3x2']
                elif nop>50 and nop<=90:
                    if num==1:
                        print("suggestive options:Press 1 for AC3x2 and AC3x2")
                        print("press 2 for AC2x2 and AC2x2")
                        cuso= int(input("option"))
                        if cuso==1:
                            upbus('AC3x2')
                            upbus('AC3x2')
                            maintainence=buscharge['AC3x2']+buscharge['AC3x2']
                        else :
                            upbus('AC2x2')
                            upbus('AC2x2')
                            maintainence=buscharge['AC2x2']+buscharge['AC2x2']
                    else :
                        print('suggestive options: NONAC3x2 and NONAC2x2 buses')
                        upbus('NONAC3x2')
                        upbus('NONAC2x2')
                        maintainence=buscharge['NONAC2x2']+buscharge['NONAC3x2']
                else:
                    print("No,bus available for",nop,"passengers")
                    maintainence=None
            def tourcost(distancetravelled):                        #calculation of total cost 
                if maintainence==None:
                    totalcost=0
                else:
                    ab=(nodays*(0.5)*maintainence)
                    aab=(distancetravelled)
                    totalcost=ab+(aab*15)
                return(totalcost)      
            print('Welcome to our RoadTravel Facility')             #main program
            stdat=eval(input('Starting Date='))
            ltdat=eval(input('End Date='))
            nodays=int(input('No. of days='))
            dis=distane()
            print("TOTAL DISTANCE TRAVELLED=",dis,"km")
            vary=availbuses()
            charge=tourcost(dis)
            from math import ceil
            if maintainence==None:
                pass
            else:
                print("Total tour expense=Rs",ceil(charge))
            name=input("Enter name")
            TravellingMode=Mode
            JourneyCost=1000
            create_personal_table(cursor)
            add_personal_data(name,TravellingMode,JourneyCost)
            print("If you want to see your total bookings Enter Show")
            wish=input("Enter data")
            if wish=="Show":
                print_whole_personaltable(cursor)
            else:
                print("Thank you for registering")            
# Here you would typically check the username and password
elif choice == 2:
    speak("Choice Accepted")
    window = tk.Tk()
    window.geometry('800x500')
    window.configure(background='#31363b')

    tk.Label(window, text="Enter Username:", bg='#31363b', fg='white').grid(row=0, column=0, padx=10, pady=10, stick='w')
    username_entry = tk.Entry(window)
    username_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(window, text="Enter Password:", bg='#31363b', fg='white').grid(row=1, column=0, padx=10, pady=10, sticky='w')
    password_entry = tk.Entry(window, show='*')
    password_entry.grid(row=1, column=1, padx=10, pady=10)

    def show():
        hide_button=tk.Button(window,image=hide_image,command=hide,relief="flat",activebackground='white',bd=0,background='white',width=30,height=25)
        hide_button.place(x=370,y=60)
        password_entry.config(show='')

    def hide():
        show_button=tk.Button(window,image=show_image,command=show,relief="flat",activebackground='white',bd=0,background='white',width=30,height=25) 
        show_button.place(x=370, y=60)
        password_entry.config(show='*')
    
    show_image=ImageTk.PhotoImage(file='show.png')
    hide_image=ImageTk.PhotoImage(file='hide.png')
    show_button=tk.Button(window,image=show_image,command=show,relief="flat",activebackground='white',bd=0,background='white',width=30,height=25) 
    show_button.place(x=370, y=60)
    hide_button=tk.Button(window,image=hide_image,command=hide,relief="flat",activebackground='white',bd=0,background='white',width=30,height=25)
    hide_button.place(x=370,y=60)

    

    def save_user():
        username = username_entry.get().strip()
        password = password_entry.get().strip()

        add_user(username, password)
        if username=="" or password=="":
            speak("please enter data")
        else:
           speak("Profile created")
           print(f"User {username} created successfully!")
           print("Login again to Access the Profile")
           print(cursor.execute("SELECT * FROM pass"))

    tk.Button(window, text="Create Profile", command=save_user).grid(row=2, columnspan=1, pady=20)
    tk.Button(window,text="Close",command=window.destroy).grid(row=2,columnspan=4,pady=10)
    window.mainloop()
else:
    speak("choice aint accepted")
