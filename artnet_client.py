from time import sleep
import threading, queue
import socket
import uuid
from struct import pack, unpack

class ArtnetClient(threading.Thread):
    
    def __init__(self, q_received, q_to_send, tag = "Desktop", ip = '0.0.0.0', port = 6454):
        self.received_queue = q_received
        self.to_send_queue = q_to_send
        self.tag = tag
        self.ip = ip
        self.port = port
        self.op_codes = { "0x4000":self.run_command }
        threading.Thread.__init__(self)
        
    def run(self):
        self._is_running = True
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.ip,self.port))
        while self._is_running:
            if self.to_send_queue.empty() != True:
                    to_send_data = self.to_send_queue.get()
                    self.socket.sendto(to_send_data[0], to_send_data[1])
                    
            try:
                data, address = self.socket.recvfrom(1024)
        
                if self.is_artnet_packet(data):
                    packet = ArtNetPacket(data)
                    self.check_op_code(address, packet)
                else:
                    print("Received a non Art-Net packet")
                
                
                    
            except Exception as e:
                print(e)
                sleep(0.2)
    
    def send(self,tags,data,ip = ('0.0.0.0',6454)):
        self.to_send_queue.put((str((tags, str(uuid.uuid4()), data)).encode(), ip))    
    
    def stop(self):
        self.socket.close()
        self._is_running = False
                
    def is_artnet_packet(self, data):
        if data[:7] != b'Art-Net':
            return False
        else:
            return True
    
    def check_op_code(self, address, packet):
        if packet.op_code in self.op_codes:
            self.op_codes[packet.op_code](address, packet)

    def run_command(self, address, packet):
        correct_tag = False
        packet_tuple = self.parse_tuple(packet.data.decode())
        identifier = packet_tuple[0]
        sent_tags = packet_tuple[1]
        command = packet_tuple[2]
    
        if (len(sent_tags) == 0):
            correct_tag = True
        else:
            if self.tag in sent_tags:
                correct_tag = True
    
        if correct_tag:
            self.received_queue.put((command, self.tag, identifier, address))
                
    def parse_tuple(self, string):
        try:
            s = eval(string)
            if type(s) == tuple:
                return s
        except:
            pass

class ArtNetPacket:
    def __init__(self, data = None):
        if (data != None):
            self.op_code = hex(unpack('<H', data[8:10])[0])
            self.ver = unpack('!H', data[10:12])[0]
            self.sequence = data[12]
            self.physical = data[13]
            self.universe = unpack('<H', data[14:16])[0]
            self.length = unpack('!H', data[16:18])[0]
            
            self.data = data[18:]