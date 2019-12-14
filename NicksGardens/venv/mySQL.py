import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="password",
    database="upcomingAppointments")

mycursor = mydb.cursor() # initialises cursor in database, allows me to execute database commands

mycursor.execute("DELETE FROM customercontactdetails;")
mydb.commit()


