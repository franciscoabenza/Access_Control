# The Sensors Class definitions

from gpiozero import DigitalInputDevice
from read_PWM import reader
from time import sleep
import pigpio

PWM_GPIO = 5
DUTY_CYCLE_DOOR = 10
SAMPLE_TIME = 0.1

class Sensor:

  def __init__(self, Sensor_Type, Name):
    self.__Sensor_Type = Sensor_Type
    self.__Name = Name
    self.Detect = False

  def Update_Detect(self):
    return self.Detect

  def Get_Detect(self):
    return self.Detect

  def Reset_Detect(self):
    self.Detect = False

class Line_Sensor(Sensor):

  def __init__(self, Name):
    Sensor.__init__(self,'Line Sensor',Name)
    self.__SensorPin = DigitalInputDevice(4) #Line Sensor on Pin 4

  def Update_Detect(self):
    if self.__SensorPin.value == 0:
      self.Detect = True

  def Get_Detect(self):
    return self.Detect

class TOF_Sensor(Sensor):

  def __init__(self, Name):
    Sensor.__init__(self,'TOF Sensor',Name)
    self.__pi = pigpio.pi()
    self.__p = reader(self.__pi, PWM_GPIO)
    sleep(SAMPLE_TIME) # Wait for Sensor to finish first measurement

  def Update_Detect(self):
      
    dc = int(self.__p.duty_cycle())
    #print(dc) #For testing
    if (dc < DUTY_CYCLE_DOOR):
      self.Detect = True

  def Get_Detect(self):
    return self.Detect

  def Sensor_Cleanup(self):
    self.__p.cancel()
    self.__pi.stop()
