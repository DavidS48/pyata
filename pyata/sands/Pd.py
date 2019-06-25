

##########################################################
##########################################################
# description: main class that emulates Pd
#
# autor: jeraman
# date: 16/04/2010
##########################################################
##########################################################


from .communication import Communication
from .gui_updater import GuiUpdater
import sands.box_classes.canvas as canvas


class Pd():
    #construtor
    def __init__(self):
        self.c = Communication(False)
        self.b = ""
    
    #inicializando a api
    def init(self):
        self.c.init_pd()
        self.clear()
        self.dsp(True)
        self.editmode(True)
        
        self.b = GuiUpdater(self.c.rcv)
        self.b.start()
        
    #finalizando a api
    def quit(self):
        self.clear()
        self.save()
        self.dsp(False)
        GuiUpdater.finish = True
        self.c.finish_pd()

        
    #salvando o arquivo
    def save(self):
        self.c.save_state(canvas.current.name)
        
    #cleans the patch
    def clear(self):
        self.c.send_pd(canvas.current.name + " clear ; ")
        canvas.current.clear()
        
    
    #modifies the editmode. receives a boolean.
    def editmode(self, on_off):
        command = canvas.current.name + " editmode 1 ; "
        if on_off==False:
            command += canvas.current.name + " editmode 0 ; "
        self.c.send_pd(command)
    
    #modifies the dsp. receives a boolean
    def dsp(self, on_off):
        if on_off==False:
            self.c.send_pd("; pd dsp 0 ; ")
        else:
            self.c.send_pd("; pd dsp 1 ; ")
   
   #returns the memory available in Pd     
    def get_box_list(self):
        return canvas.current.boxes
    
    #return the connections available in Pd
    def get_connection_list(self):
        return canvas.current.connections
    
   
    
    #################################
    ## FIND MENU METHODS
    #################################
    
    #finds a given box by its label
    def find(self, label):
        command = self.canvas + "find " + str(label) + " ; "
        self.send.send_pd(command)
    
    #continues the last find called
    def findagain(self):
        command = self.canvas + "findagain ; "
        self.send.send_pd(command)
    
    def finderror(self):
        command = "; pd finderror"
        self.send.send_pd(command)
    
    
