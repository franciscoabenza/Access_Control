#The Light Control Class definitions

from enum import Enum
from gpiozero import LED

class Lights(Enum):
  OFF = 10
  ON  = 11

class Light_Control:

  def __init__(self):
    self.locked    = Lights.OFF
    self.open      = Lights.OFF
    self.violated  = Lights.OFF

    #Configure leds on the Pi
    self.locked_led   = LED(19)
    self.open_led     = LED(20)
    self.violated_led = LED(21)

    self.locked_led.off()
    self.open_led.off()
    self.violated_led.off()

  def set_locked(self,OnOff):
    if OnOff != self.locked:
      if OnOff == Lights.ON:
        self.locked = Lights.ON
        self.locked_led.on()
      else:
        self.locked = Lights.OFF
        self.locked_led.off()
  
  def get_locked(self):
    return self.locked

  def set_open(self,OnOff):
    if OnOff != self.open:
      if OnOff == Lights.ON:
        self.open = Lights.ON
        self.open_led.on()
      else:
        self.open = Lights.OFF
        self.open_led.off()
  
  def get_open(self):
    return self.locked

  def set_violated(self,OnOff):
    if OnOff != self.violated:
      if OnOff == Lights.ON:
        self.violated = Lights.ON
        self.violated_led.on()
      else:
        self.violated = Lights.OFF
        self.violated_led.off()
  
  def get_violated(self):
    return self.locked
  
  def all_lights_off(self):
    self.set_locked(Lights.OFF)
    self.set_open(Lights.OFF)
    self.set_violated(Lights.OFF)
  
