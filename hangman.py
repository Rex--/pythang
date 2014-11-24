import random
import linecache
from Tkinter import *
from functools import partial

word = ''
guessed_word = ''
guessed_letters = ''
total_letters = 0
num_guessed_letters = 0
lives = 0
wins = 0
loses = 0

batman = False

class GUI():
   def __init__(self, master):

      grid = Grid()
      self._master = master

      self._canvas = Canvas(self._master, height=250, width=250)
      self._canvas.grid(row=1, column=1, columnspan=7)

      global word
      self._label = Label(self._master, text=' ')
      self._label.grid(row=2, column=1, columnspan=7)

      self._alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
      self._buttons = {}
      self._rgrid = 3
      self._cgrid = 1
      for self._letter in self._alphabet:
         self._command = partial(self.guess, self._letter)
         self._buttons[self._letter] = Button(self._master, text=self._letter.upper(), command=self._command)
         if self._rgrid == 3 or self._rgrid == 4:
            self._buttons[self._letter].grid(row=self._rgrid, column=self._cgrid)
            if self._cgrid == 7:
               if self._rgrid == 4:
                  self._rgrid = 5
               else:
                  self._rgrid = 4
               self._cgrid = 0
         elif self._rgrid == 5 or self._rgrid == 6:
            self._buttons[self._letter].grid(row=self._rgrid, column=self._cgrid, columnspan=2)
            if self._cgrid == 6:
               self._cgrid = 0
               if self._rgrid == 5:
                  self._rgrid = 6
         self._cgrid = self._cgrid + 1

      self._guessedWord = ''
      self._guessEntry = Entry(self._master, textvariable=self._guessedWord)
      self._guessEntry.grid(row=9, column=1, columnspan=5)

      self._reset_b = Button(self._master, text='Reset Game', command=self.reset)
      self._reset_b.grid(row=10, column=3, columnspan=3)

      self._wLabel = Label(self._master, text="Wins: 0")
      self._wLabel.grid(row=10, column=1, columnspan=2)
      self._lLabel = Label(self._master, text="Loses: 0")
      self._lLabel.grid(row=10, column=6, columnspan=2)

   def guess(self, letter):
      global guessed_letters
      Guess(letter)
      self._buttons[letter].config(state=DISABLED)
      #guessed_letters = guessed_letters + letter
      #print guessed_letters

   def reset(self):
      start_game()
      for self._letter in self._alphabet:
         self._buttons[self._letter].config(state=NORMAL)
      self._canvas.delete("all")
      self._canvas.config(bg='white')

   def draw_post(self):
      line1 = self._canvas.create_line(25, 200, 25, 25)
   def draw_beam(self):
      line2 = self._canvas.create_line(25, 25, 125, 25)
      line3 = self._canvas.create_line(125, 25, 125, 30)
   def draw_head(self):
      head = self._canvas.create_oval(100, 30, 150, 80)
   def draw_batman(self):
      mask = self._canvas.create_oval(100, 30, 150, 80, fill="black")
      rect = self._canvas.create_rectangle(110, 65, 140, 80, fill="white", outline="white")
      outline = self._canvas.create_oval(100, 30, 150, 80)
      ear1 = self._canvas.create_polygon(105, 40, 115, 15, 120, 40, fill="black")
      ear2 = self._canvas.create_polygon(130, 40, 135, 15, 145, 40, fill="black")
   def draw_body(self):
      body = self._canvas.create_line(125, 80, 125, 160)
   def draw_rightArm(self):
      rightArm = self._canvas.create_line(125, 100, 150, 120)
   def draw_leftArm(self):
      leftArm = self._canvas.create_line(125, 100, 100, 120)
   def draw_rightLeg(self):
      rightLeg = self._canvas.create_line(125, 160, 150, 185)
   def draw_leftLeg(self):
      leftLeg = self._canvas.create_line(125, 160, 100, 185)

   def set_label(self, text):
      self._label.config(text=text)

   def set_canvas_color(self, color):
      self._canvas.config(bg=color)

   def set_Wins(self, lives):
      self._text = "Wins: " + str(lives)
      self._wLabel.config(text=self._text)

   def set_Loses(self, lives):
      self._text = "Loses: " + str(lives)
      self._lLabel.config(text=self._text)

def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]

def get_Word():
   wordlist = "words.txt"
   line_numba = random.randint(1, 5)
   global word
   word = linecache.getline(wordlist, line_numba)

def deduct_life():
   global lives
   global word
   global loses
   global batman
   if lives == 8:
      gui.draw_post()
   elif lives == 7:
      gui.draw_beam()
   elif lives == 6:
      if batman == True:
         gui.draw_batman()
      else:
         gui.draw_head()
   elif lives == 5:
      gui.draw_body()
   elif lives == 4:
      gui.draw_leftLeg()
   elif lives == 3:
      gui.draw_rightLeg()
   elif lives == 2:
      gui.draw_leftArm()
   elif lives == 1:
      gui.draw_rightArm()
   elif lives == 0:
      gui.set_label(word)
      gui.set_canvas_color("red") # loss
      loses = loses + 1
      gui.set_Loses(loses)
   lives = lives - 1

def Guess(letter):
   global guessed_word
   global word
   global num_guessed_letters
   global total_letters
   global wins
   if letter not in word:      # Guessed incorrectly
      deduct_life()
   else:                  # Guessed correctly
      indexes = find(word, letter)
      gwList = guessed_word.split()
      for index in indexes:
         ri = (index - 2) + index
         gwList[index] = letter
         num_guessed_letters = num_guessed_letters + 1
      guessed_word = ' '.join(gwList)
      gui.set_label(guessed_word)
      if num_guessed_letters == total_letters:  # Win
         wins = wins + 1
         gui.set_canvas_color("green")
         gui.set_Wins(wins)

def start_game():
   global total_letters
   global num_guessed_letters
   global guessed_word
   global lives
   get_Word()
   total_letters = len(word) - 1
   guessed_word = '_ ' * total_letters
   gui.set_label(guessed_word)
   num_guessed_letters = 0
   lives = 8

root = Tk()
root.title("Hangman")
gui = GUI(root)
start_game()
root.mainloop()
