import time

import exp_read
import msmidi_fx_edit

#Regarding the EXP pedal
exp_value= exp_read.get_exp_value()
established_exp_value= exp_value
number_of_exp_functions = 3
is_engaged= 0
window_width= 3 #The value leaves the window if it is > established_value + window_width. Same applies for -/< If this happens, is_engaged is set to true.
settling_limit= 6 #If the value stays this sime for <settling_limit> amount of times, "is_engaged" is set to false.
settling_counter= 0
wait_for_cc= 0.02 #this defines how often expression CC messages can be sent via the exp pedal
last_call= 0

class Exp_handler:
    def __init__(self):
        self.exp_value = exp_value
        self.old_exp_value = 0
        self.exp_function = 1
        self.number_of_exp_functions = number_of_exp_functions
        self.established_exp_value = established_exp_value
        self.is_engaged= is_engaged
        self.window_width = window_width
        self.settling_limit = settling_limit
        self.settling_counter = settling_counter
        self.wait_for_cc = wait_for_cc
        self.last_call = last_call
        pass
    
    #This needs to be called in your main loop
    def react_to_exp_activity(self):
        self.old_exp_value= self.exp_value
        self.exp_value= exp_read.get_exp_value()
        if (time.time() > (self.last_call + self.wait_for_cc)):
            if self.is_engaged:
                val = int((self.exp_value / 127)*100) #Change this to adapt the value range. Right now it goes from 0 to 100.
                msmidi_fx_edit.edit_parameter(2, 4, val) #Determine effect and parameter to be changed here!
                #print('CC-Change: ' + str(89 + self.exp_function) + ' ' + str(self.exp_value)) #4 testing
                self.last_call= time.time()
                if self.settling_counter >= self.settling_limit:
                    self.is_engaged= 0
                    self.established_exp_value= self.exp_value
                    self.settling_counter= 0
                elif self.exp_value == self.old_exp_value:
                    self.settling_counter= self.settling_counter + 1
            else:
                if self.exp_value < (self.established_exp_value - self.window_width) or self.exp_value > (self.established_exp_value + self.window_width):
                    self.is_engaged= 1
    
    