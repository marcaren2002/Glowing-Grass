import pygame_functions,random,csv,uuid,pygame

pygame.init() # setting colour variables
darkGreen = (159,232,63)
green = (0,200,0)
red = (200,0,0)
black = (0,0,0)
white = (255,255,255)
grey = (10,10,10)

# setting up the window
font_colour = black
screen = pygame.display.set_mode((650, 480))
pygame.display.set_caption("Appointment details")
button_inactive_colour = green
button_active_colour = red
inputBox_inactive_colour = black
inputBox_active_colour = black

NumbersOnly = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"] # an array for numbers only
Symbols = ["!", "£", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=", "+", "{", "[",
               "}", "]", "#", "~", ":", ";", "@", "'", "<", ",", ">", ".", "?", "/", "¬", "`"] # an array full of symbols
LettersOnly = ["a", "A", "b", "B", "c", "C", "d", "D", "e", "E", "f", "F", "g", "G", "h", "H", "i", "I",
                   "j", "J", "k", "K", "l", "L", "m", "M",
                   "n", "N", "o", "O", "p", "P", "q", "Q", "r", "R", "s", "S", "t", "T", "u", "U", "v", "V",
                   "w", "W", "x", "X", "y", "Y", "z", "Z"] # an array for English letters only

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

def appointment_details_window():
    def validation_check():
        def write_to_File():
            write = csv.writer(open("contact_details.csv", "a", newline=""), delimiter=",")
            write.writerow([])
            pygame.quit()
            quit()

    chosen_date = Input_textBox(250,100,10,32)
    chosen_mowing = Input_textBox(250, 150, 10, 32)
    chosen_hedgeTrimming = Input_textBox(250, 200, 10, 32)
    chosen_snowClearing = Input_textBox(250, 250, 10, 32)
    chosen_pesticideAppliance = Input_textBox(250, 300, 10, 32)

    appointment_details_title = textBox(50,20,0,0,"Appointment details")
    chosen_date_label = textBox(5,100,0,0,"Enter a date: ")
    mowing_label = textBox(5, 150, 0, 0, "Grass mowing")
    hedgeTrimming_label = textBox(5, 200, 0, 0, "Hedge Trimming")
    snowClearing_label = textBox(5, 250, 0, 0, "Snow Clearing")
    pesticideAppliance_label = textBox(5,300,0,0,"Pesticide Appliance")

    submit_application = Button("Submit",20,100,400,150,50,red,green,validation_check)

    labels = [appointment_details_title,chosen_date_label,mowing_label,hedgeTrimming_label,snowClearing_label,snowClearing_label,pesticideAppliance_label]
    buttons = [submit_application]
    input_boxes = [chosen_date,chosen_mowing,chosen_hedgeTrimming,chosen_snowClearing,chosen_pesticideAppliance]
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


if __name__ == '__main__':
    appointment_details_window()
    pygame.quit()