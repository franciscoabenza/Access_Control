# The User Interface Class definitions

from os import system, name

import tty, sys, termios, os, fcntl


class User_Interface:

  def __init__(self, AC, IF_Type):
    self.__AC = AC #Access Control Object
    self.__IF_Type = IF_Type

  def Clear_Screen(self):
    print('Clear User_Interface Screen')

  def Print_Menu(self):
    print('User_Interface Menu')

  def Read_Key(self):
    print('Read a key')

class Terminal_Interface(User_Interface):

  def __init__(self,AC):
    User_Interface.__init__(self,AC,'Terminal')
    self.__AC = AC  # Access Control Object
    self.__filedescriptors = termios.tcgetattr(sys.stdin) #Save File Descriptor for stdin

    tty.setcbreak(sys.stdin) #Enable Keypress without carriage return

    # make stdin a non-blocking file
    fd = sys.stdin.fileno()
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

    self.Print_Menu()

  def Terminal_Cleanup(self):
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN,self.__filedescriptors)    

    
  def Clear_Screen(self):
    system('clear')

  def Print_Menu(self):
    self.Clear_Screen()
    print('---------------------', self.__AC.Get_Name(),'---------------------')
    print('                                                                   ')
    print('          Press l to lock the Access Control                       ')
    print('                                                                   ')
    print('          Press o to open Access Control                           ')
    print('                                                                   ')
    print('                                                                   ')
    print('                                                                   ')
    print('                    Press q to quit                                ')
    print('                                                                   ')
    print('----------------------', self.__AC.Get_Interface_Type(), '----------------------')

  def Read_Key(self):

    key = sys.stdin.read(1)
    if key == '\x1b': # Escape:
      key = sys.stdin.read(1)
      if key == '[':
        key = sys.stdin.read(1)
        if key == 'A':
          return 'Arrow_Up'
        elif key == 'B':
          return 'Arrow_Down'
        elif key == 'C':
          return 'Arrow_Right'
        elif key == 'D':
          return 'Arrow_Left'
    else:
      return key #Anything else   

    
    
class Web_Interface(User_Interface):
  def __init__(self,AC):
    User_Interface.__init__(self,AC,'Web')
    self.__RC = RC  # Access Control Object
    self.Print_Menu()

  def Clear_Screen(self):
    print('Clear Screen on Web Interface')

  def Print_Menu(self):
    self.Clear_Screen()
    print(self.__RC.Get_Name())
    print('Print Web Interface Menu')
    print(self.__RC.Get_Interface_Type())

  def Read_Key(self):
    key='A'
    return key


