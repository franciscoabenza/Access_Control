import time
import pigpio

class reader:
   
#A class to read PWM pulses and calculate their frequency
#and duty cycle.  The frequency is how often the pulse
#happens per second.  The duty cycle is the percentage of
#pulse high time per cycle.
   
  def __init__(self, pi, gpio):
  #Instantiate with the Pi and GPIO of the PWM signal to monitor.

     self.pi = pi
     self.gpio = gpio
     self._new = 1.0
     self._old = 0.0
     self._high_tick = None
     self._period = None
     self._high = None

     pi.set_mode(gpio, pigpio.INPUT)

     self._cb = pi.callback(gpio, pigpio.EITHER_EDGE, self._cbf)

  def _cbf(self, gpio, level, tick): #Callback function

    if level == 1:

      if self._high_tick is not None:
        t = pigpio.tickDiff(self._high_tick, tick)

        if self._period is not None:
          self._period = (self._old * self._period) + (self._new * t)
        else:
          self._period = t

      self._high_tick = tick

    elif level == 0:

      if self._high_tick is not None:
        t = pigpio.tickDiff(self._high_tick, tick)

        if self._high is not None:
          self._high = (self._old * self._high) + (self._new * t)
        else:
          self._high = t

  def frequency(self):

    #Returns the PWM frequency.
    if self._period is not None:
      return 1000000.0 / self._period
    else:
      return 0.0

  def pulse_width(self):

    #Returns the PWM pulse width in microseconds.
    if self._high is not None:
      return self._high
    else:
      return 0.0

  def duty_cycle(self):

   #Returns the PWM duty cycle percentage.
   if self._high is not None:
     return 100.0 * self._high / self._period
   else:
     return 0.0

  def cancel(self):

    #Cancels the reader and releases resources.
    self._cb.cancel()
