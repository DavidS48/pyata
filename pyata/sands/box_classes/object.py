
##########################################################
##########################################################
# description: abstract class that represents a generic Object box
#
# autor: jeraman
# date: 13/04/2010
##########################################################
##########################################################

from .box import Box
from .. import communication
from . import canvas



#box class itself
class Object (Box):
    #constructor
    def __init__(self, x, y, label, id=-1):
        self.label = label
        Box.__init__(self,x, y, id)


    def create(self):
        command = canvas.current.name + " obj " + str(self.x) + " " + str(self.y) + " " + self.label + "; "
        communication.snd.send_pd(command)
        Box.create(self)

    
    #edits this object
    def edit(self, label):
        self.unselect() #unselects
        self.click() #selects this    
        
        command = ""
        for i in label: #sends all key pressed
            command += canvas.current.name + " key 1 " + str(ord(i)) + " 0 ; "
            command += canvas.current.name + " key 0 " + str(ord(i)) + " 0 ; " 
        
        communication.snd.send_pd(command)
        self.unselect() #unselects this
        #ajeita o indice atual do objeto na memoria do pd
        temp = memory_box.pop(search_box(self))
        memory_box.append(temp)
        self.label = label
        
    
    #aux static function to debug this class
    @staticmethod
    def debug():
        o = Object(10, 10, 0, "dac~")
        print(o.edit("osc~"))
        print(o.edit(""))
    
