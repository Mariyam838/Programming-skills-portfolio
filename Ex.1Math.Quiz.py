from tkinter import*# Import tkinter library
from tkinter import messagebox
import tkinter as tk
import random # Import random for generating random numbers


class MathQuizApp:  # Define a class for the application

    def __init__(self,root):  # Initialize the class with the root window

        #Initialize the main app window
        self.root= root  # Create the main application window

        self.root.title("Math Quiz")   # Set the title of the window

        self.root.geometry("300x300")   # Set the size of the window
        self.root.config(bg="#B6FBFE")

        #Initialize score,question number,difficulty, and try
        self.score = 0 # Tracks  the score of the user

        self.question_count = 0  # Tracks the number of questions asked

        self.difficulty = None   # Stores the  difficulty level of the questions

        self.first_try = True   # Tracks if it's the first attempt at each question

        # Initial user interface setup
        self.setup_ui()
    
    def setup_ui(self): 
        #Display the welcome message and menu
        self.welcome_label = tk.Label(self.root, text="Welcome to Math Quiz!", font=("Arial",14,"bold"),bg="#f0f0f0") # Create a label to display the welcome message

        self.welcome_label.pack(pady=(20,10)) 

        self.display_menu() #Show the difficulty selection menu

    def display_menu(self):#Display the menu selecting the quiz  difficulty level

        #Clear  the welcome label and display the difficulty selection menu
        self.clear_widgets()
        #Label  to display the difficulty selection menu

        self.menu_label = tk.Label(self.root, text="Select Difficulty Level:", font=("Roboto",12,"bold"), bg="#f0f0f0")
        self.menu_label.pack()

        #Difficulty level buttons
        #EASY
        self.easy_button = tk.Button(self.root, text="1.Easy", command=lambda: self.start_quiz(1),
                                     font=("Arial", 10,"bold"), width=10, bg="#4CAF50", fg="white")
        self.easy_button.pack(pady=5)
        #MODERATE
        self.moderate_button = tk.Button(self.root, text="2.Moderate", command=lambda: self.start_quiz(2)
                                         , font=("Arial", 10,"bold"), width=10, bg="#FFC107", fg="black")
        self.moderate_button.pack(pady=5)
        #ADVANCED
        self.advanced_button = tk.Button(self.root, text="3.Advanced", command=lambda: self.start_quiz(3)
                                         , font=("Arial", 10,"bold"), width=10, bg="#F44336", fg="white")
        self.advanced_button.pack(pady=5)

    def clear_widgets(self):
        #Clear the widgets from the window for new content prep
        for widget in self.root.winfo_children():
            widget.destroy()

    def start_quiz(self,difficulty):
        """Start the quiz with the selected difficulty level
            Args
            difficulty (int): The difficulty level of the quiz (1, 2, or 3)
        """
        self.difficulty = difficulty #set the  difficulty level

        self.score = 0  #reset the score for each quiz attempt

        self.question_count = 0   #reset the question count for each quiz attempt

        self.first_try = True   #reset the first try flag for each quiz attempt

        self.next_question()  #display the first question

    def random_int(self):
        """Generate a random integer based on difficulty level.
        Returns:
        int: A random integer between the range determined  by the difficulty level.
        """
        if self.difficulty == 1: 
            return random.randint(1, 10)#Single  digit number for easy 
        elif self.difficulty == 2:
            return random.randint(10, 99) # Two digit number for moderate

        else:
            return random.randint(1000, 9999)# four digit number for advanced
        
    def decide_operation(self):
        """Randomly decide between addition subtraction questions.
        Returns:
        str: Either '+' or  '-' for the operation.
        """
        return random.choice(['+','-'])
    
    def next_question(self):
        """Display the next question in the quiz, or show the results if the quiz is over."""
        #If 10  questions have been asked, show the results
        if self.question_count == 10: 
            self.display_results()
            return
        
        #prepare the interface for new question
        self.clear_widgets()
        self.question_count += 1 #Increment the question count
        self.first_try = True #Reset first try

        #Generate two numbers and an operation for the question
        num1 = self.random_int()
        num2 = self.random_int()
        self.operation = self.decide_operation()

        #Ensure subtraction results in a non-negative answer
        if self.operation == '-' and num1< num2: # swap the numbers if num1 is smaller

            num1, num2 = num2, num1 # swap the numbers if necessary

        #Calculate the correct answer
        self.correct_answer = eval(f"{num1} {self.operation}  {num2}")
        # Display the question to user
        self.display_problem(num1,num2)

    def display_problem(self, num1, num2):
        """Display the question to the user."""
        #Display label showing question text(e.g,  "22 + 2 = ")
        self.question_label = tk.Label(self.root,text=f"Question{self.question_count}:{num1} {self.operation} {num2}="
                                       ,font=('Arial', 20),fg='blue')
        self.question_label.pack(pady=10)

        #Entry field to type answer
        self.answer_entry = tk.Entry(self.root, font=('Arial', 20),justify="center")

        self.answer_entry.pack(pady=5)

        #Button to submit the answer
        self.submit_button = tk.Button(self.root, text="Submit", command=self.check_answer,  font=('Arial', 20), width=8, bg="#2196F3", fg="white")

        self.submit_button.pack(pady=10)

    def check_answer(self):
        """Check the user's answer and display the result."""
        #Disable the submit button to prevent multiple clicks
        self.submit_button.config(state=tk.DISABLED)
        try:
            user_answer = int(self.answer_entry.get())
        except ValueError:
            #Display error message if input is not an integer
            messagebox.showerror("Error","Invalid input. Please enter a number.")
            self.submit_button.config(state=tk.NORMAL) # Re-enable the submit button
            return
        
        #Check if the user's answer is correct
        if user_answer ==  self.correct_answer:
            #Award  points if the answer is correct based on whather it was first try
            self.score  += 10 if self.first_try else 5
            #Display success mesaage
            self.feedback_label = tk.Label(self.root, text="Correct!",  font=('Arial', 20, "bold"), fg='green', bg="#f0f0f0")
            self.feedback_label.pack(pady=5)
            #Move  to the next question
            self.root.after(1000,self.next_question)
        else:
            #If  the answer is incorrect on first  try, allow a second attempt
            if self.first_try:
                self.first_try = False
                messagebox.showerror("Incorrect", "Try Again!")
                self.submit_button.config(state=tk.NORMAL) # Re-enable the submit button
            else:
                #If incorrect on the second attempt,Show the correct answer
                messagebox.showinfo("Answer",f"Incorrect. The correct answer was {self.correct_answer}.")
                self.root.after(1000,self.next_question)# Move to next question
    
    def display_results(self):
        """Display the final score to the user and rank on user performance"""
        self.clear_widgets()

        #Show final score
        self.results_label =  tk.Label(self.root, text=f"Final Score: {self.score}/100", font=('Arial', 20, "bold"), bg="#f0f0f0")
        self.results_label.pack(pady=10)

        #Show the rank  based on the score
        self.rank_label = tk.Label(self.root, text=f"Rank: {self.get_rank()}", font=('Arial', 20, "bold"),fg="blue", bg="#f0f0f0")

        self.rank_label.pack(pady=5)

        #Button to start a new game
        self.play_again_button = tk.Button(self.root, text= "Play Again", command= self.display_menu, font=("Arial",10),width=10,bg="#4CAF50",fg="white")
        self.play_again_button.pack(pady=5)

        #Button to exit the quiz
        self.exit_button = tk.Button(self.root, text= "Quit", command= self.root.quit,  font=("Arial",10),width=10,bg="#F44336",fg="white")

        self.exit_button.pack()

    def get_rank(self):
        """Calculate the user's rank based on final score.
        Returns:
        str: The rank (e.g, "A+" for scores  90-100, "A" for scores 80-89, etc.)"""
        if self.score >= 90:
            return "A+"
        elif self.score >= 80:
            return "A"
        elif self.score >= 70:
            return "B"
        elif self.score >= 60:
            return "C"
        elif self.score >= 50:
            return "D"
        else:
            return "F"
        
# Main code to initialize and start the  quiz
if __name__ == "__main__":
    root =  tk.Tk()
    app = MathQuizApp(root)
    root.mainloop()




















        
