import random,csv,uuid,pygame,datetime,mysql.connector

pygame.init() # setting colour variables
darkGreen = (159,232,63)
green = (0,200,0)
red = (200,0,0)
black = (0,0,0)
white = (255,255,255)
grey = (10,10,10)

# setting up the window
font_colour = red
screen = pygame.display.set_mode((750, 590))
pygame.display.set_caption("Customer details")
button_inactive_colour = green
button_active_colour = red
inputBox_inactive_colour = black
inputBox_active_colour = black
FONT = pygame.font.Font(None, 32)

class Input_textBox: # creates a class for a text box so I can easily create multiple textboxes.
    def __init__(self, x, y, w, h, text='',): # this sets the required parameters for the instance.
        self.rect = pygame.Rect(x, y, w, h) # creates a rectangle using given parameters. (x,y,w,h)
        self.colour = black # sets its border colour and font colour to black.
        self.text = text # variable text will be what the content of the input box is.
        self.txt_surface = FONT.render(text, True, self.colour) # sets text font and text colour.
        self.active = False # initialises the activated variable to False as it hasn't been clicked on.


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN: # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos): # sets the active variable to true.
                self.active = not self.active
            else:
                self.active = False # toggles the active variable to false.
            self.color = inputBox_active_colour if self.active else inputBox_active_colour
        if event.type == pygame.KEYDOWN: # if the user presses a key then it:
            if self.active: # checks to see if the user has clicked on the textbox that they want to use.
                if event.key == pygame.K_RETURN: # if the Enter key is pressed:
                    Input_textBox.text = self.text # the contents of the input box will be referred to as the instance.
                elif event.key == pygame.K_BACKSPACE: # if the Backspace key is pressed then -
                    self.text = self.text[:-1] # removes one character from the inputted text
                else:
                    self.text += event.unicode # whenever a key is pressed, the unicode character is re-rendered.
                self.txt_surface = FONT.render(self.text, True, self.colour)

    def update(self): # This function makes the extends the box width if the character count is longer than the box width.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width
    def draw(self, screen): # This function will blit the text and the rect onto the screen.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5)) # this draws and centres the text into the middle of text.
        pygame.draw.rect(screen, self.colour, self.rect, 2) # draws the borders of the input box. integer 2 is the size of borders.
class textBox:
    def __init__(self, x, y, w, h, text=''): # sets given parameters as its own variables
        self.rect = pygame.Rect(x, y, w, h)
        self.rect_colour = darkGreen
        self.font_colour = font_colour
        self.text = text
        self.txt_surface = FONT.render(text, True, self.font_colour)

    def draw(self, screen): # This will blit the text and the rect onto screen
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.rect_colour, self.rect,0)
class Button():
    def __init__(self, text, fontSize, x, y, w, h, active_colour, inactive_colour, action=None):
        self.text = text                # sets the variables to itself
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.active_colour = button_active_colour
        self.inactive_colour = button_inactive_colour
        self.action = action
        self.fontSize = fontSize

    def draw(self,screen):
        mouse = pygame.mouse.get_pos() # gets mouse coordinates
        click = pygame.mouse.get_pressed() # determines how many times mouse button is clicked (left, right and middle buttons)

        if self.x+self.w > mouse[0] > self.x and self.y+self.h > mouse[1] > self.y:  # if mouse is over button coordinates
            pygame.draw.rect(screen, self.active_colour,(self.x, self.y, self.w, self.h), 0) # draws button with the given active colour
            buttonFont = pygame.font.Font('freesansbold.ttf', self.fontSize)
            buttonText = buttonFont.render(self.text, True, black)
            buttonTextRect = buttonText.get_rect()
            buttonTextRect.center = (self.x + (self.w*0.5), self.y + (self.h*0.5))
            screen.blit(buttonText,buttonTextRect)
            if click[0] > 0:
                self.action()
        else:
            pygame.draw.rect(screen, self.inactive_colour, (self.x, self.y, self.w, self.h,), 0)  # draws the button with the given inactive colour
            buttonFont = pygame.font.Font('freesansbold.ttf', self.fontSize)
            buttonText = buttonFont.render(self.text, True, black)
            buttonTextRect = buttonText.get_rect()
            buttonTextRect.center = (self.x + (self.w*0.5), self.y + (self.h*0.5))
            screen.blit(buttonText,buttonTextRect)

def run_Customer_Details_window():
    id_no = uuid.uuid1() # creates an ID
    NumbersOnly = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"] # an array for numbers only
    Symbols = ["!", "£", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=", "+", "{", "[",
               "}", "]", "#", "~", ":", ";", "@", "'", "<", ",", ">", ".", "?", "/", "¬", "`"] # an array full of symbols
    LettersOnly = ["a", "A", "b", "B", "c", "C", "d", "D", "e", "E", "f", "F", "g", "G", "h", "H", "i", "I",
                   "j", "J", "k", "K", "l", "L", "m", "M",
                   "n", "N", "o", "O", "p", "P", "q", "Q", "r", "R", "s", "S", "t", "T", "u", "U", "v", "V",
                   "w", "W", "x", "X", "y", "Y", "z", "Z"] #] an array full of letters, lowercase and uppercase.

    def contactDetails():
        def propertyDetails():
            def appointmentDetails():
                def write_to_File():
                    mydb = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        passwd="password",
                        database="upcomingAppointments")

                    mycursor = mydb.cursor()  # initialises cursor in database, allows me to execute database commands
                    ContactDetails_sql = "INSERT INTO customercontactdetails(firstName, lastName, mobile, email) VALUES (%s,%s,%s,%s)"
                    PropertyDetails_sql = "INSERT INTO customerpropertydetails(HouseNameNo, Address_1, Address_2, Postcode) VALUES (%s,%s,%s,%s)"
                    AppointmentDetails_sql = "INSERT INTO customerappointmentdetails(Date, Mowing, Hedge_Trimming, Snow_Clearing, Pesticide_Appliance) VALUES (%s,%s,%s,%s,%s)"

                    date = str(datetime.date(int(chosen_date_year.text), int(chosen_date_month.text),
                                             int(chosen_date_day.text)))
                    contact_details = (fName.text,lName.text,mobile.text,email.text)
                    property_details = (houseNameNo.text,Address1.text,Address2.text,Postcode.text)
                    appointment_details = (date,chosen_mowing.text,chosen_hedge_trimming.text,chosen_snow_clearing.text,chosen_pesticide_appliance.text)

                    mycursor.execute(ContactDetails_sql, contact_details)
                    mycursor.execute(PropertyDetails_sql, property_details)
                    mycursor.execute(AppointmentDetails_sql, appointment_details)
                    mydb.commit()  # required to save changes or won't save to database
                    pygame.quit()
                    quit()

                def date_valid_check():
                    date = str(datetime.date(int(chosen_date_year.text), int(chosen_date_month.text),
                                             int(chosen_date_day.text)))
                    customer_details_csv = open('contact_details.csv', 'r').read()
                    date_valid = False
                    while date_valid == False:
                        if date in customer_details_csv:
                            print("Date used")
                            date_valid = False
                            break
                        else:
                            print("Date not used")
                            buttons.append(submit_application)
                            date_valid = True
                            break

                chosen_date_day = Input_textBox(250, 100, 10, 32)
                chosen_date_month = Input_textBox(250,150,10,32)
                chosen_date_year = Input_textBox(250,200,10,32)
                chosen_mowing = Input_textBox(250,300,10,32)
                chosen_hedge_trimming = Input_textBox(250, 350, 10, 32)
                chosen_snow_clearing = Input_textBox(250, 400, 10, 32)
                chosen_pesticide_appliance = Input_textBox(250, 450, 10, 32)

                appointment_details_title = textBox(50, 20, 0, 0, "Appointment details")
                chosen_date_label = textBox(5, 70, 0, 0, "Enter a date")
                chosen_date_day_label = textBox(125, 100,0,0,"Day (DD): ")
                chosen_date_month_label = textBox(115, 150, 0, 0, "Month (MM): ")
                chosen_date_year_label = textBox(110, 200, 0, 0, "Year (YYYY): ")
                mowing_label = textBox(5, 300, 0, 0, "Grass mowing")
                hedgeTrimming_label = textBox(5, 350, 0, 0, "Hedge Trimming")
                snowClearing_label = textBox(5, 400, 0, 0, "Snow Clearing")
                pesticideAppliance_label = textBox(5, 450, 0, 0, "Pesticide Appliance")

                validate_appt_date = Button("Confirm", 20, 500, 100, 150, 50, red, green, date_valid_check)
                submit_application = Button("Submit", 20, 500, 400, 150, 50, red, green, write_to_File)

                labels = [appointment_details_title, chosen_date_label, chosen_date_day_label, chosen_date_month_label, chosen_date_year_label, mowing_label, hedgeTrimming_label,
                          snowClearing_label, snowClearing_label, pesticideAppliance_label]
                buttons = [validate_appt_date]
                input_boxes = [chosen_date_day,chosen_date_month,chosen_date_year,chosen_mowing,chosen_hedge_trimming,chosen_snow_clearing,chosen_pesticide_appliance]

                done = False
                while not done:
                    screen.fill(darkGreen)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            done = True
                        for box in input_boxes:
                            box.handle_event(event)

                    for box in input_boxes:
                        box.update()
                    for box in input_boxes:
                        box.draw(screen)
                    for button in buttons:
                        button.draw(screen)
                    for text in labels:
                        text.draw(screen)

                    pygame.display.flip()
            def postcode_validation():
                postcodeValid = False
                while postcodeValid == False:
                    if len(Postcode.text) > 7 or len(Postcode.text) < 7:
                        postcodeValid = False
                        print("Invalid Postcode - incorrect number of characters")
                        break
                    else:
                        if Postcode.text[0] in LettersOnly and Postcode.text[1] in LettersOnly and Postcode.text[
                            2] in NumbersOnly and Postcode.text[3] in NumbersOnly and Postcode.text[
                            4] in NumbersOnly and \
                                Postcode.text[5] in LettersOnly and Postcode.text[6] in LettersOnly:
                            postcodeValid = True
                            print("Valid postcode")
                            buttons.append(nextButton2)
                            break
                        else:
                            print("Invalid postcode - wrong order")
                            break

            property_Details_title = textBox(100, 50, 0, 0, "Property Details")
            houseNameNo_prompt = textBox(5, 100, 0, 0, "House name/")
            houseNameNo_prompt2 = textBox(20, 120, 0, 0, "number")
            Address1_prompt = textBox(5, 150, 0, 0, "Address 1")
            Address2_prompt = textBox(5, 200, 0, 0, "Address 2")
            Postcode_prompt = textBox(5, 250, 0, 0, "Postcode")

            houseNameNo = Input_textBox(150, 100, 140, 32)
            Address1 = Input_textBox(150, 150, 140, 32)
            Address2 = Input_textBox(150, 200, 140, 32)
            Postcode = Input_textBox(150, 250, 140, 32)

            validButton = Button("Validate", 20, 50, 300, 100, 50, red, green,postcode_validation)
            nextButton2 = Button("Next",20,450,300,100,50,red,green,appointmentDetails)

            input_boxes = [houseNameNo, Address1, Address2, Postcode]
            labels = [property_Details_title, houseNameNo_prompt, houseNameNo_prompt2, Address1_prompt, Address2_prompt,
                      Postcode_prompt]
            buttons = [validButton]
            done = False

            if Postcode.text != "":
                POSTCODE()

            while not done:
                screen.fill(darkGreen)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        done = True
                    for box in input_boxes:
                        box.handle_event(event)
                for box in input_boxes:
                    box.update()
                for box in input_boxes:
                    box.draw(screen)
                for button in buttons:
                    button.draw(screen)
                for text in labels:
                    text.draw(screen)
                pygame.display.flip()
        def presentID():  # shows the generated ID onto screen
            uniqueID_prompt = textBox(2, 400, 0, 0, "Your unique ID is:" + str(id_no))
            uniqueID_prompt.draw(screen)
        def mobile_validation():
            mobileValid = False
            while mobileValid == False:
                if len(mobile.text) > 9 or len(mobile.text) < 9:
                    mobileValid = False
                    print("Invalid mobile")
                    break
                elif mobile.text[0] in NumbersOnly and mobile.text[1] in NumbersOnly and mobile.text[
                        2] in NumbersOnly and mobile.text[3] in NumbersOnly and mobile.text[4] in NumbersOnly and \
                            mobile.text[5] in NumbersOnly and mobile.text[6] in NumbersOnly and mobile.text[
                        7] in NumbersOnly and mobile.text[8]:
                        mobileValid = True
                        print("Valid mobile")
                        buttons.append(nextButton)
                        break
                else:
                    mobileValid = False
                    print("Invalid mobile")
                    break

        contact_details_title = textBox(100, 50, 0, 0, "Contact Details")
        first_name_prompt = textBox(5, 100, 0, 0, "First Name")
        last_name_prompt = textBox(5, 150, 0, 0, "Last Name")
        mobile_prompt = textBox(5, 200, 0, 0, "Mobile (07)")
        email_prompt = textBox(5, 250, 0, 0, "Email")
        invalid_prompt = textBox(350,50,0,0,"Invalid mobile")
        valid_prompt = textBox(350,100,0,0, "Valid mobile")

        fName = Input_textBox(150, 100, 140, 32)
        lName = Input_textBox(150, 150, 140, 32)
        mobile = Input_textBox(150, 200, 140, 32)
        email = Input_textBox(150, 250, 140, 32)

        validButton = Button("Validate", 20, 400, 200, 100, 50, red, green, mobile_validation)
        nextButton = Button("Next", 20, 200, 300, 100, 50, red, green, propertyDetails)
        generateID = Button("Generate ID", 20, 350, 300, 120, 50, red, green, presentID)

        input_boxes = [fName, lName, mobile, email]
        labels = [contact_details_title, first_name_prompt, last_name_prompt, mobile_prompt, email_prompt]
        buttons = [generateID, validButton]
        done = False

        while not done:
            screen.fill(darkGreen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                for box in input_boxes:
                    box.handle_event(event)

            for box in input_boxes:
                box.update()

            for box in input_boxes:
                box.draw(screen)

            for button in buttons:
                button.draw(screen)

            for text in labels:
                text.draw(screen)

            pygame.display.flip()

    details_title = textBox(100, 50, 0, 0, "Contact Details")
    contactDetailsButton = Button("Start", 20, 50, 300, 100, 50, red, green, contactDetails)
    labels = [details_title]
    buttons = [contactDetailsButton]
    done = False

    while not done:
        screen.fill(darkGreen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        for button in buttons:
            button.draw(screen)
        for text in labels:
            text.draw(screen)

        pygame.display.flip()

if __name__ == '__main__':
    run_Customer_Details_window()
    pygame.quit()