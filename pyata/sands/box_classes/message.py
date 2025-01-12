
##########################################################
##########################################################
# description: abstract class that represents a message box
#
# autor: jeraman
# date: 14/04/2010
##########################################################
##########################################################

from . import canvas
from .. import communication

from .box import Box

#number class itself
class Message (Box):
    #constructor
    def __init__(self, x, y,text, id=-1):
        self.text = text
        Box.__init__(self,x, y, id)

    def create(self):
        command = canvas.current.name + " msg " + str(self.x) + " " + str(self.y) + " " + self.text + "; "
        communication.snd.send_pd(command)
        Box.create(self)
    
    #edits this object
    def edit(self, text):
        self.unselect() #unselects        
        self.click() #selects this
        
        command = ""
        for i in text: #sends all key pressed
            command += canvas.current.name + " key 1 " + str(ord(i)) + " 0 ; " 
            command += canvas.current.name + " key 0 " + str(ord(i)) + " 0 ; "
        communication.snd.send_pd(command)
        self.unselect() #unselects this
        #ajeita o indice atual do objeto na memoria do pd
        temp = memory_box.pop(search_box(self))
        memory_box.append(temp)
        self.text = text  
    
    
    def click(self):
        #sets no-edit mode
        command  = canvas.current.name + " editmode 1 ; "
        command += canvas.current.name + " editmode 0 ; "
        communication.snd.send_pd(command)
        Box.click(self)
        #sets edit mode
        command  = canvas.current.name + " editmode 1 ; "
        communication.snd.send_pd(command)
        
    
    #aux static function to debug this class
    @staticmethod
    def debug():
        box = Message(20, 20, "alo!", 0)
        print(box.edit("ola"))
