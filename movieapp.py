from re import M, search
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from turtle import back
import random
import csv

import mysql.connector
import smtplib
import ssl


# Connects database
mydb = mysql.connector.connect(
    host="localhost", user="root", password="Password1!",  auth_plugin='mysql_native_password', database='movies_and_shows')
mycursor = mydb.cursor()
print(mydb)


# Global variables to store the user's information for writing emails easier
userEmail = ""
user_name = ""
time = ""
date = ""
recipients = ()


# Unneeded, to show how the columnds are made and with what data types each column is.
def createTables():
    mycursor.execute(
        "CREATE TABLE movie(movieID VARCHAR(25), name VARCHAR(100), year SMALLINT, PRIMARY KEY(movieID))")
    mycursor.execute(
        "CREATE TABLE genre(genreID SMALLINT, name VARCHAR(15), PRIMARY KEY(genreID))")
    mycursor.execute(
        "CREATE TABLE movie_genre(movieID VARCHAR(25), genreID SMALLINT, FOREIGN KEY(movieID) REFERENCES movie(movieID), FOREIGN KEY(genreID) REFERENCES genre(genreID))")
    mycursor.execute(
        "CREATE TABLE user(name VARCHAR(15), email VARCHAR(50), password VARCHAR(15), PRIMARY KEY(email))")
    mycursor.execute("ALTER TABLE user ADD UNIQUE (email)")
    mydb.commit()


# adds movies into the db from the csv file
def movieintodb():
    with open("movies.csv") as file:
        csv_file = csv.reader(file, delimiter="\t")
        sql = "INSERT INTO movie (movieID, name, year) VALUES (%s, %s, %s)"
        for line in csv_file:
            nline = line[0].split("|")
            if nline[0] != 'tt0011801':
                print(nline)
                vals = (nline[0].strip(','), nline[1].strip(
                    ','), int(((str(nline[2]).strip(',')).strip("\"")).strip("'").strip(",")))
                mycursor.execute(sql, vals)
                mydb.commit()
    print("done")


def generateRandomMovie(window):
    # pick a random movie
    mycursor.execute("SELECT name FROM movie")
    names = mycursor.fetchall()
    movie_ind = random.randrange(len(names))
    movie_label = tk.Label(window, text=names[movie_ind],
                           fg="black", bg='#AF8FE9', width=50)
    movie_label.pack(side='top')


def random_movie(window):
    window.destroy()
    random_window = tk.Tk()
    random_window.title('Movie App Database: Random')
    window_width = 1200
    window_height = 750
    random_window.configure(bg="#AF8FE9")

    # get the screen dimension
    screen_width = random_window.winfo_screenwidth()
    screen_height = random_window.winfo_screenheight()

    # find the center point
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)

    # set the position of the window to the center of the screen
    random_window.geometry(
        f'{window_width}x{window_height}+{center_x}+{center_y}')
    random_window.minsize(600, 400)
    random_window.maxsize(1200, 750)

    random_button = tk.Button(random_window, text='Generate Random Movie',
                              bg='#ACD1AF', height=2, width=15, command=lambda: generateRandomMovie(random_window))
    random_button.pack(side='top')
    back_button = tk.Button(
        random_window, text='Back', bg='#ACD1AF', height=2, width=15, command=lambda: main_menu(random_window))
    back_button.pack(side='bottom')

    random_window.mainloop()


def searchentry(window, sentry):
    title = sentry.get()
    mycursor.execute(f"SELECT name, year FROM movie WHERE name = \'{title}\'")
    titles_tuple = mycursor.fetchall()
    for i in titles_tuple:
        newLabel = tk.Label(window, text=i,
                            fg="black", bg='#AF8FE9', width=50)
        newLabel.grid(row=4, column=1)


def search_movies(main_window):
    main_window.destroy()
    search_window = tk.Tk()
    search_window.title('Movie App Database: View Movies')
    window_width = 1200
    window_height = 750
    search_window.configure(bg="#AF8FE9")

    # get the screen dimension
    screen_width = search_window.winfo_screenwidth()
    screen_height = search_window.winfo_screenheight()

    # find the center point
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)

    # set the position of the window to the center of the screen
    search_window.geometry(
        f'{window_width}x{window_height}+{center_x}+{center_y}')
    search_window.minsize(600, 400)
    search_window.maxsize(1200, 750)

    search_label = tk.Label(search_window, text='Search: ',
                            fg="black", bg='#AF8FE9', width=50)
    search_entry = tk.Entry(search_window, fg="black",
                            bg="white", width=25)
    search_label.grid(row=0, column=0)
    search_entry.grid(row=0, column=1)
    search_button = tk.Button(search_window, text='Submit',
                              bg='#ACD1AF', height=2, width=15, command=lambda: searchentry(search_window, search_entry))
    search_button.grid(row=1, column=1)
    back_button = tk.Button(
        search_window, text='Back', bg='#ACD1AF', height=2, width=15, command=lambda: main_menu(search_window))
    back_button.grid(row=6, column=1)

    search_window.mainloop()


def add_movie(main_window):
    main_window.destroy()
    add_window = tk.Tk()
    add_window.title('Movie App Database: Add Movie')
    window_width = 1200
    window_height = 750
    add_window.configure(bg="#AF8FE9")

    # get the screen dimension
    screen_width = add_window.winfo_screenwidth()
    screen_height = add_window.winfo_screenheight()

    # find the center point
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)

    # set the position of the window to the center of the screen
    add_window.geometry(
        f'{window_width}x{window_height}+{center_x}+{center_y}')
    add_window.minsize(600, 400)
    add_window.maxsize(1200, 750)
    # place code here

    add_window.mainloop()


def remove_movie(main_window):
    main_window.destroy()
    remove_window = tk.Tk()
    remove_window.title('Movie App Database: Remove Movie')
    window_width = 1200
    window_height = 750
    remove_window.configure(bg="#AF8FE9")

    # get the screen dimension
    screen_width = remove_window.winfo_screenwidth()
    screen_height = remove_window.winfo_screenheight()

    # find the center point
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)

    # set the position of the window to the center of the screen
    remove_window.geometry(
        f'{window_width}x{window_height}+{center_x}+{center_y}')
    remove_window.minsize(600, 400)
    remove_window.maxsize(1200, 750)

    remove_window.mainloop()


def send_entry(window, entry1, entry2, entry3, entry4, date_entry, time_entry):
    r1 = entry1.get()
    r2 = entry2.get()
    r3 = entry3.get()
    r4 = entry4.get()
    date = date_entry
    time = time_entry
    recipients = (r1, r2, r3, r4)
    port = 465  # For SSL
    sender_email = "norepy.moviedatabase409@gmail.com"
    password = 'CPSC408!'

    for rEmail in recipients:
        print(rEmail)
        print(type(rEmail))
        reciever_email = rEmail
        message = f"""\
        You have been invited to a movie event by {user_name}!\n{user_name} would like to watch the movie on {date} at {time}!
        """

        # Create a secure SSL context
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login("norepy.moviedatabase409@gmail.com", password)

            # Send email here
            server.sendmail(sender_email, reciever_email, message)


def send_invitation(main_window):
    main_window.destroy()
    send_window = tk.Tk()
    send_window.title('Movie App Database: Send Invitation')
    window_width = 1200
    window_height = 750
    send_window.configure(bg='#AF8FE9')

    # get the screen dimension
    screen_width = send_window.winfo_screenwidth()
    screen_height = send_window.winfo_screenheight()

    # find the center point
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)

    # set the position of the window to the center of the screen
    send_window.geometry(
        f'{window_width}x{window_height}+{center_x}+{center_y}')
    send_window.minsize(600, 400)
    send_window.maxsize(1200, 750)

    # Creates and places all labels for the entry boxes
    rEntry1_label = tk.Label(send_window, text='Recipient: ',
                             fg="black", bg='#AF8FE9', width=50)
    rEntry2_label = tk.Label(send_window, text='Recipient: ',
                             fg="black", bg='#AF8FE9', width=50)
    rEntry3_label = tk.Label(send_window, text='Recipient: ',
                             fg="black", bg='#AF8FE9', width=50)
    rEntry4_label = tk.Label(send_window, text='Recipient: ',
                             fg="black", bg='#AF8FE9', width=50)
    rEntry2_label.grid(row=0, column=0)
    rEntry3_label.grid(row=1, column=0)
    rEntry1_label.grid(row=2, column=0)
    rEntry4_label.grid(row=3, column=0)
    rEntry1 = tk.Entry(send_window, fg="black", bg="white", width=50)
    rEntry2 = tk.Entry(send_window, fg="black", bg="white", width=50)
    rEntry3 = tk.Entry(send_window, fg="black", bg="white", width=50)
    rEntry4 = tk.Entry(send_window, fg="black", bg="white", width=50)
    rEntry1.grid(row=0, column=1)
    rEntry2.grid(row=1, column=1)
    rEntry3.grid(row=2, column=1)
    rEntry4.grid(row=3, column=1)

    # Time label and entry box
    movie_label = tk.Label(send_window, text='Movie: ',
                           fg="black", bg='#AF8FE9', width=50)
    movie_entry = tk.Entry(send_window, fg="black", bg="white", width=25)
    time_label = tk.Label(send_window, text='Time: ',
                          fg="black", bg='#AF8FE9', width=50)
    date_label = tk.Label(send_window, text='Date: ',
                          fg="black", bg='#AF8FE9', width=50)
    time_entry = tk.Entry(send_window, fg="black", bg="white", width=25)
    date_entry = tk.Entry(send_window, fg="black", bg="white", width=25)
    time_entry.grid(row=4, column=1)
    time_label.grid(row=4, column=0)
    date_label.grid(row=5, column=0)
    date_entry.grid(row=5, column=1)
    movie_label.grid(row=6, column=0)
    movie_entry.grid(row=6, column=1)
    submit_button = tk.Button(
        send_window, text='Submit', bg='#ACD1AF', height=2, width=15, command=lambda: send_entry(send_window, rEntry1, rEntry2, rEntry3, rEntry4, date_entry, time_entry))
    submit_button.grid(row=7, column=1)
    back_button = tk.Button(
        send_window, text='Back', bg='#ACD1AF', height=2, width=15, command=lambda: main_menu(send_window))
    back_button.grid(row=8, column=1)

    send_window.mainloop()


def main_menu(window):
    window.destroy()
    mainmenu_window = tk.Tk()
    mainmenu_window.title('Movie App Database: Main Menu')
    window_width = 1200
    window_height = 750
    mainmenu_window.configure(bg='#AF8FE9')

    # get the screen dimension
    screen_width = mainmenu_window.winfo_screenwidth()
    screen_height = mainmenu_window.winfo_screenheight()

    # find the center point
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)

    # set the position of the window to the center of the screen
    mainmenu_window.geometry(
        f'{window_width}x{window_height}+{center_x}+{center_y}')
    mainmenu_window.minsize(600, 400)
    mainmenu_window.maxsize(1200, 750)

    # If clicked, will go to the Random Movie window
    pick_button = tk.Button(mainmenu_window, text='Pick a Random Movie',
                            bg='#ACD1AF', height=2, width=15, command=lambda: random_movie(mainmenu_window))
    pick_button.pack(side='top')

    # If clicked, goes tot he view movies window
    view_button = tk.Button(
        mainmenu_window, text='View All Movies', bg='#ACD1AF', height=2, width=15, command=lambda: search_movies(mainmenu_window))
    view_button.pack(side='top')

    # If Clicked, goes to the add movie window
    add_button = tk.Button(
        mainmenu_window, text='Add a Movie', bg='#ACD1AF', height=2, width=15, command=lambda: add_movie(mainmenu_window))
    add_button.pack(side='top')

    # If clicked, goes to the delete movie window
    delete_button = tk.Button(
        mainmenu_window, text='Remove a Movie', bg='#ACD1AF', height=2, width=15, command=lambda: remove_movie(mainmenu_window))
    delete_button.pack(side='top')

    # If clicked, goes to the send invite window
    send_button = tk.Button(
        mainmenu_window, text='Send Invitation', bg='#ACD1AF', height=2, width=15, command=lambda: send_invitation(mainmenu_window))
    send_button.pack(side='top')

    # If cliked, destroys the window and quits the application
    quit_button = tk.Button(
        mainmenu_window, text='Quit', bg='#ACD1AF', height=2, width=15, command=mainmenu_window.destroy)
    quit_button.pack(side='top')
    mainmenu_window.mainloop()


# Grabs the text from the entry box and adds the data to database
def newUser_getEntry(newuser_window, entry1, entry2, entry3):

    # Grabs the text from the entry boxes
    name = entry1.get()
    email = entry2.get()
    password = entry3.get()

    # Sets global variable for ease of use
    userEmail = email
    user_name = name

    # Inserts the user data into the database
    sql = "INSERT INTO user (name, email, password) VALUES (%s, %s, %s)"
    vals = (name, email, password)
    mycursor.execute(sql, vals)
    mydb.commit()
    print("Successfully added the new user to the database.")

    # Destroys the window and goes to the main_menu
    main_menu(newuser_window)


# Creates entry boxes for user to enter name, email, and password
def new_user(login_window):
    login_window.destroy()
    newuser_window = tk.Tk()
    newuser_window.title('Movie App Database: New User')
    window_width = 1200
    window_height = 750
    newuser_window.configure(bg='#AF8FE9')

    # get the screen dimension
    screen_width = newuser_window.winfo_screenwidth()
    screen_height = newuser_window.winfo_screenheight()

    # find the center point
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)

    # set the position of the window to the center of the screen
    newuser_window.geometry(
        f'{window_width}x{window_height}+{center_x}+{center_y}')
    newuser_window.minsize(600, 400)
    newuser_window.maxsize(1200, 750)

    name_label = tk.Label(newuser_window, text='Name: ',
                          fg="black", bg='#AF8FE9', width=50)
    name_entry = tk.Entry(newuser_window, fg="black", bg="white", width=50)
    email_label = tk.Label(newuser_window, text='Email: ',
                           fg="black", bg='#AF8FE9', width=50)
    email_entry = tk.Entry(newuser_window, fg="black", bg="white", width=50)
    password_label = tk.Label(newuser_window, text='Password: ',
                              fg="black", bg='#AF8FE9', width=50)
    password_entry = tk.Entry(newuser_window, fg="black", bg="white", width=50)

    submit_button = tk.Button(newuser_window, text='Submit',
                              bg='#ACD1AF', height=2, width=15, command=lambda: newUser_getEntry(newuser_window, name_entry, email_entry, password_entry))
    name_label.grid(row=0, column=0)
    name_entry.grid(row=0, column=1)
    email_label.grid(row=1, column=0)
    email_entry.grid(row=1, column=1)
    password_label.grid(row=2, column=0)
    password_entry.grid(row=2, column=1)
    submit_button.grid(row=3, column=1)

    back_button = tk.Button(newuser_window, text='Back',
                            bg='#ACD1AF', height=2, width=15, command=lambda: login(newuser_window))
    back_button.grid(row=4, column=1)
    newuser_window.mainloop()


# Grabs the text entries and checks if they match stored entried in database
def login_entry(window, email_entry, password_entry):
    # Grabs the text from the text box
    email = email_entry.get()
    password = password_entry.get()

    # Sets global variable for ease of use
    userEmail = email

    # Creates a dict for the execute function to use
    emailDict = [email]

    # Checks if the given user is in the database
    s = "SELECT * FROM user WHERE email = %s"
    mycursor.execute(s, emailDict)
    e = mycursor.fetchall()
    for l in e:

        # Sets global variable for ease of access
        user_name = l[2]

        for k in l:
            if k == '':
                incorrect_label = tk.Label(
                    window, text='Incorrect Email', fg="red", bg='#AF8FE9', width=50)
                incorrect_label.grid(row=3, column=0)

    # Grabs the password stored for the given email
    sql = "SELECT password FROM user WHERE email = %s"
    mycursor.execute(sql, emailDict)
    p = mycursor.fetchall()
    for i in p:
        for j in i:
            # Checks if the given password matches with the stored password
            if (str(j) != password):
                # IF WRONG, create a label saying 'incorrect 'password'
                incorrect_label = tk.Label(
                    window, text='Incorrect Password', fg="red", bg='#AF8FE9', width=50)
                incorrect_label.grid(row=3, column=0)
            else:
                # Correct go to the main menu window
                main_menu(window)


def login(window):
    window.destroy()
    login_window = tk.Tk()
    login_window.title('Movie Database App: Log In')
    window_width = 1200
    window_height = 750
    login_window.configure(bg='#AF8FE9')
    # get the screen dimension
    screen_width = login_window.winfo_screenwidth()
    screen_height = login_window.winfo_screenheight()

    # find the center point
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)

    # set the position of the window to the center of the screen
    login_window.geometry(
        f'{window_width}x{window_height}+{center_x}+{center_y}')
    login_window.minsize(600, 400)
    login_window.maxsize(1200, 750)

    # Creates the login buttons and labels
    email_label = tk.Label(
        login_window, text='Email: ', fg="black", bg='#AF8FE9', width=50)
    email_entry = tk.Entry(login_window, fg="black", bg="white", width=50)
    password_label = tk.Label(
        login_window, text='Password: ',  fg="black", bg='#AF8FE9', width=50)
    password_entry = tk.Entry(login_window, fg='black',
                              bg="white", width=50, show='*')

    # Places the buttons and labels
    email_label.grid(row=0, column=0)
    email_entry.grid(row=0, column=1)
    password_label.grid(row=1, column=0)
    password_entry.grid(row=1, column=1)

    # This button calls the login_entry function when clicked
    login_button = tk.Button(login_window,
                             text="Log In", width=25, height=2, bg="white", fg='black', command=lambda: login_entry(login_window, email_entry, password_entry))
    login_button.grid(row=3, column=1)

    # This button calls the new_user function when clicked
    new_user_button = tk.Button(login_window,
                                text="New User?", width=25, height=2, bg="white", fg='black', command=lambda: new_user(login_window))
    new_user_button.grid(row=4, column=1)

    login_window.mainloop()


window = tk.Tk()
login(window)

mydb.close()
# "#AF8FE9"


def default_window():
    window = tk.Tk()
    window.title('Movie App Database')
    window_width = 1200
    window_height = 750
    window.configure(bg="#AF8FE9")

    # get the screen dimension
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # find the center point
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)

    # set the position of the window to the center of the screen
    window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    window.minsize(600, 400)
    window.maxsize(1200, 750)
    # place code here
    window.mainloop()
