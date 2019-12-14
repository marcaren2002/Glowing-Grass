import datetime

customer_details_csv = open('contact_details.csv', 'r').read()

day = int(input("Input day: "))
month = int(input("Input month: "))
year = int(input("Input year: "))
date = str(datetime.date(year,month,day))
print(date)

if date in customer_details_csv:
    print("Date used")
else:
    print("Date not used")

#'%B' used to refer to month name e.g. December
#'%m' used to refer to month number e.g. 12
