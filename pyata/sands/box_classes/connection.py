##########################################################
##########################################################
# description: abstract class that represents any Connection between boxes
#
# autor: jeraman
# date: 15/04/2010
##########################################################
##########################################################

from . import canvas
from .. import communication

#connects two generic boxes
def connect (b1, outlet, b2, inlet):
    c = Connection(b1, outlet, b2, inlet)
    return c.status 


#disconnect a connection
def disconnect(b1, outlet, b2, inlet):
    #procura a conexao
    i = search_connection(b1, outlet, b2, inlet)
    #se realmente existir
    if i>-1:
        return canvas.current.connections[i].delete()
    else:
        return False


#searchs a generic connection
def search_connection (b1, outlet, b2, inlet):
    i=0   
    #seraching for a specific box in memory    
    for c in canvas.current.connections:
        if (b1==c.box_orig) & (outlet==c.outlet) & (b2==c.box_dest) & (inlet==c.inlet):
            return i
        i+=1
    
    #return -1 if not
    if i==len(canvas.current.connections):
        return -1


    

class Connection:
    #constructor
    def __init__(self, box_orig, outlet, box_dest, inlet):
        self.box_orig = box_orig
        self.outlet = outlet
        self.box_dest = box_dest
        self.inlet = inlet
        self.status = self.create()
        
        
    #creates a connection in Pd    
    def create(self):
        b1 = canvas.current.box_number(self.box_orig)
        b2 = canvas.current.box_number(self.box_dest)

        if (b1 > -1) & (b2 > -1):
            #get the state before inserting the connection
            communication.snd.save_state(canvas.current.name)
            t1 = communication.snd.get_file()

            #try to build the connection
            command = " ".join([canvas.current.name, "connect", str(b1), str(self.outlet), str(b2), str(self.inlet)]) + " ; "
            communication.snd.send_pd(command)
            
            #get the state after insertin the connection
            communication.snd.save_state(canvas.current.name)
            t2 = communication.snd.get_file()
            
            #verifies if changed
            if t1 != t2:
                canvas.current.connections.append(self)
                return True
            else:
                return False

    
    #creates a connection in Pd    
    def delete(self):
        b1 = canvas.current.box_number(self.box_orig)
        b2 = canvas.current.box_number(self.box_dest)
        if (b1 > -1) & (b2 > -1):
            #get the state before removing the connection
            communication.snd.save_state(canvas.current.name)
            t1 = communication.snd.get_file()
            
            #try to remove the connection
            command = " ".join([canvas.current.name, "disconnect ", str(b1), str(self.outlet), str(b2), str(self.inlet)]) + " ; "
            communication.snd.send_pd(command)
            
            #get the state after removing the connection
            communication.snd.save_state(canvas.current.name)
            t2 = communication.snd.get_file()
            
            #verifies if changed
            if t1 != t2:
                i=search_connection(self.box_orig, self.outlet, self.box_dest, self.inlet)
                canvas.current.connections.pop(i)
                return True
            else:
                return False
            
        
        
