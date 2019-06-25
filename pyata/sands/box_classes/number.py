
##########################################################
##########################################################
# description: abstract class that represents a generic Number box
#
# autor: jeraman
# date: 13/04/2010
##########################################################
##########################################################

from .box import Box
from socket import socket
from time import sleep
from . import canvas
from .. import communication

#number class itself
class Number(Box):
    
    #constructor
    def __init__(self, x, y, id =-1):
        self.value = 0
        Box.__init__(self,x, y, id)        

    def create(self):
        command = canvas.current.name + " obj " + str(self.x) + " " + str(self.y) + " nmb ; "
        communication.snd.send_pd(command)
        Box.create(self)
        command = "id " + str(canvas.current.box_id(self)) + " ; "
        #print command
        communication.snd.send_pd(command)
        sleep(0.1)
        
    #get the value from pd
    def get_value(self):
        sleep(0.1)
        return int(self.value)
        
    
    #edits this object
    def set(self, value): 
        #sets no-edit mode
        command  = canvas.current.name + " editmode 1 ; "
        command += canvas.current.name + " editmode 0 ; "
        communication.snd.send_pd(command)
        
        self.click() #clicks
        
        str_value = str(value) # transforms the value to str
        for i in str_value: #sends all key pressed
            command += canvas.current.name + " key 1 " + str(ord(i)) + " 0 ; "
            command += canvas.current.name + " key 0 " + str(ord(i)) + " 0 ; "   
        communication.snd.send_pd(command)
        
        command  = canvas.current.name + " key 1 10 0 ; " # press enter
        command += canvas.current.name + " key 0 10 0 ; "
        
        #sets edit mode
        command += canvas.current.name + " editmode 1 ; "
        
        communication.snd.send_pd(command)
    
    #increments the lowest amount from the value of a number
    def increment(self):
        #sets no-edit mode
        command  = canvas.current.name + " editmode 1 ; "
        command += canvas.current.name + " editmode 0 ; "
        communication.snd.send_pd(command)
        
        command  = canvas.current.name + " mouse " + str(self.x+1) + " " + str(self.y+1) + " 1 0 ; "
        command += canvas.current.name + " motion " + str(self.x+1) + " " + str(self.y) + " 0 ; "
        command += canvas.current.name + " mouseup " + str(self.x+1) + " " + str(self.y) + " 1 0 ; "
        #self.value = self.get_value()
        
        command += canvas.current.name + " editmode 1 ; "
        communication.snd.send_pd(command)
    
    #decrements the lowest amount from the value of a numbe
    def decrement(self):
        #sets no-edit mode
        command  = canvas.current.name + " editmode 1 ; "
        command += canvas.current.name + " editmode 0 ; "
        communication.snd.send_pd(command)
        
        command  = canvas.current.name + " mouse " + str(self.x+1) + " " + str(self.y+1) + " 1 0 ; "
        command += canvas.current.name + " motion " + str(self.x+1) + " " + str(self.y+2) + " 0 ; "
        command += canvas.current.name + " mouseup " + str(self.x+1) + " " + str(self.y+2) + " 1 0 ; "
        #self.value = self.get_value()
        command += canvas.current.name + " editmode 1 ; "
        communication.snd.send_pd(command)
    

    
    
    #aux static function to debug this class
    @staticmethod
    def debug():
        o = Number(10, 10, 0)
        print(o.set(20))
        print(o.increment())
        print(o.decrement())   
