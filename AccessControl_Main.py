# This is the main Function for the Access Control
from Access_Control import Access_Control
from Light_Control import Light_Control, Lights

def main():

  NAME = 'DoorMaster'
  USER_INTERFACE = 'Terminal'

  MyLights = Light_Control() 
  MyAccess = Access_Control(NAME, USER_INTERFACE, MyLights)
  
main()
