from tkinter import *
from PIL  import ImageTk, Image
import random

# Initialize the main window
main = Tk()
main.title("Random Joke Generator")  # Set the title of the window
main.geometry("550x750")  # Set the size of the window
main.config(bg="#E0F7FA")  # Set a light teal background color

# Load and set the window icon
main.iconphoto(False,ImageTk.PhotoImage(file=r"C:\Users\Hp\OneDrive\Desktop\AP.Assessment1\Jokelogo.jpeg"))


# Load jokes from a text file
def load_jokes():
    with open(r"C:\Users\Hp\OneDrive\Desktop\AP.Assessment1\randomJokes.txt") as file_handler:
        lines = file_handler.readlines()  # Read all lines from the file
        return [line.strip() for line in lines if line.strip()]  # Strip newline characters and empty lines

# Load jokes into a global variable
jokes = load_jokes()
current_joke = ""  # Initialize current_joke as an empty string

# Function to display a random joke setup
def display_joke():
    global current_joke
    current_joke = random.choice(jokes)  # Choose a random joke
    setup, _ = current_joke.split('?', 1)  # Split the joke into setup and punchline
    txtarea.delete(1.0, END)  # Clear the text area
    txtarea.insert(END, f"Setup: {setup.strip()}?\n\nPress 'Punchline' to see the punchline...")  # Display setup
    punchline_button.pack(pady=10)  # Show punchline button

# Function to reveal the punchline when the button is clicked
def reveal_punchline():
    if current_joke:  # Check if there's a current joke set to display
        _, punchline = current_joke.split('?', 1)  # Get punchline
        txtarea.insert(END, f"\n\nPunchline: {punchline.strip()}")  # Display punchline
        punchline_button.pack_forget()  # Hide punchline button

# Instruction label
heading = Label(main, text="Random Joke Generator", font=('Roboto', 14, 'bold'), fg='#FFFFFF', bg='#0097A7', padx=10, pady=5)
heading.pack(pady=20)  # Place the label at the specified position

# Text area to display jokes
txtarea = Text(main, font=('Roboto', 11), wrap=WORD, bg="#FFFFFF", fg="#004D40", borderwidth=2, relief="solid")
txtarea.pack(padx=10, pady=20, fill=BOTH, expand=True)  # Set position and size

# Button to trigger joke display
tell_joke_button = Button(main, text="Alexa tell me a joke", command=display_joke, font=('Roboto', 12, 'bold'),
                          bg="#00796B", fg="#FFFFFF", activebackground="#004D40", activeforeground="#FFFFFF", borderwidth=0)
tell_joke_button.pack(pady=10, ipadx=10, ipady=5)

# Button to reveal punchline
punchline_button = Button(main, text="Punchline", command=reveal_punchline, font=('Roboto', 12, 'bold'),
                          bg="#00796B", fg="#FFFFFF", activebackground="#004D40", activeforeground="#FFFFFF", borderwidth=0)
punchline_button.pack_forget()  # Initially hidden

# Button to quit the application
quit_button = Button(main, text="Quit", command=main.quit, font=('Roboto', 12, 'bold'),
                     bg="#37474F", fg="#FFFFFF", activebackground="#546E7A", activeforeground="#FFFFFF", borderwidth=0)
quit_button.pack(pady=10, ipadx=10, ipady=5)  # Pack the quit button with padding

# Keep the window open and responsive to user action
main.mainloop()

