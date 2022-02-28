#The Access Control Class definitions

from User_Interface import User_Interface, Terminal_Interface, Web_Interface
from Sensors import Line_Sensor, TOF_Sensor
from enum import Enum
from time import sleep
from Light_Control import Light_Control, Lights 

class States(Enum):
  LOCKED   = 0
  OPEN     = 1
  VIOLATED = 2
  
SAMPLE_TIME = 0.1
  
class Access_Control:
  
  def __init__(self, Name, IF_Type,LC):
    self.__Name = Name
    self.__IF_Type = IF_Type
    self.__State = States.LOCKED
    self.LC = LC #Light Controller Object reference - Aggregation

    # User Interface Object is created and AccessControl object reference is passed down
    if IF_Type == 'Terminal':
      self.MyFace = Terminal_Interface(self)
    elif IF_Type == 'Web':
      self.MyFace = Web_Interface(self)

    # TOF Sensor Object is created 
    self.MyTOF = TOF_Sensor('TOF1')

    # Line Sensor Object is created 
    self.MyLine = Line_Sensor('Line1')

    # Light Control Object is created
    #self.MyLights = Light_Control()

    #Start the Main Access Control Loop
    self.Main_Loop()

  def Get_Interface_Type(self):
    return self.__IF_Type

  def Set_Name(self, Name):
    self.__Name = Name

  def Get_Name(self):
    return self.__Name

  def Set_State(self, State):
    self.__State = State

  def Get_State(self):
    return self.__State

  def Handle_Open(self):
    self.LC.set_open(Lights.ON)
    #print('Handle Open') #Test
    self.MyLine.Update_Detect()
    if self.MyLine.Get_Detect() == True:
      self.Set_State(States.LOCKED) #lock the door
      self.MyLine.Reset_Detect()
      self.LC.all_lights_off()
    sleep(SAMPLE_TIME)  

  def Handle_locked(self):
    self.LC.set_locked(Lights.ON)
    #print('Handle Locked') #Test
    self.MyLine.Update_Detect()
    if self.MyLine.Get_Detect() == True:
      self.Set_State(States.OPEN) #Unlock the door
      self.MyLine.Reset_Detect()
      self.LC.all_lights_off()
      

    self.MyTOF.Update_Detect()
    if self.MyTOF.Get_Detect() == True:
      self.Set_State(States.VIOLATED) #Violation - Activate Security !
      self.MyTOF.Reset_Detect()
      self.LC.all_lights_off()

    sleep(SAMPLE_TIME)
    
  def Handle_Violation(self):
    self.LC.set_violated(Lights.ON)
    #print('Handle Violation') #test
    self.MyLine.Update_Detect()
    if self.MyLine.Get_Detect() == True:
      self.Set_State(States.OPEN) #Unlock the door
      self.MyLine.Reset_Detect()
      self.LC.all_lights_off()
    sleep(SAMPLE_TIME)
    
  def Main_Loop(self):

    quit = False
    
    actions = {States.OPEN:     self.Handle_Open,
               States.LOCKED:   self.Handle_locked,
               States.VIOLATED: self.Handle_Violation}

    while not quit:
      key = self.MyFace.Read_Key()
      if key == 'q':
        quit = True
        self.MyFace.Terminal_Cleanup()
        self.MyTOF.Sensor_Cleanup()
      elif key == 'l':
        self.LC.all_lights_off()
        self.Set_State(States.LOCKED)
      elif key == 'o':
        self.LC.all_lights_off()
        self.Set_State(States.OPEN)
     
      action = actions.get(self.__State)
      action()
