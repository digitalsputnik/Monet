from artnet_client import ArtnetClient
import threading, queue
import io
import sys
from time import sleep

running = False

listener = None
unreal = None

q_received, q_to_send = queue.Queue(), queue.Queue()

def start(unreal_in):
    global unreal, listener, running
    if running == False:
        running = True
        unreal = unreal_in
        listener = ArtnetClient(q_received, q_to_send)
        listener.start()
        print("Artnet running")
    else:
        print("Artnet already running")

def stop():
    global running, listener
    if running == True:
        running = False
        listener.stop()
        print("Artnet stopped")
    else:
        print("Artnet not running")

def execute_next():
    global running, q_received, q_to_send
    if running == True and q_to_send.empty == True and q_received.empty != True:
        packet = q_received.get()
    
        command = packet[0]
        tag = packet[1]
        identifier = packet[2]
        address = packet[3]
    
        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()
        try:
            exec(command, globals())
        except Exception as err:
            print(err)
        output = buffer.getvalue()
        sys.stdout = old_stdout
        result = bytes(str(output) + "  ", encoding='utf8')
    
        if (len(output) > 0):
            q_to_send.put((str((tag, identifier, result)).encode(), address))
            print(output)
            
        return
    if running == True and q_to_send.empty != True:
        data = q_to_send.get()
        self.listener.socket.sendto(data[0],data[1])
        print("Sending data: "+str(data[0]))
        return