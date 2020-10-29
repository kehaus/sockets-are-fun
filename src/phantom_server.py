#!/usr/bin/env python3
"""
example from here:
    https://realpython.com/python-sockets/

"""

import socket



# =======================================================================
# 
# =======================================================================
class TemperatureReader():
    
    def __init__(self):
        self.temperature = 24

    def get_temperature(self):
        return self.temperature

# =======================================================================
# 
# =======================================================================

class PhantomServer():
    """ """
    BYTE_STRING_SIZE = 1024
    CONTROL_COMMANDS = [
        'stop communication',
        'get attributes'
    ]
    
    def __init__(self, host, port, dev, verbose=False):     
        
        self.verbose = verbose
        self._init_socket(host, port)
        self._set_device(dev)
        self._establish_communication()
        
    
    def _init_socket(self, host, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((host, port))    
        self.s.listen()

    def _establish_communication(self): 
        
        self.stop_commun = False
        conn, addr = self.s.accept()
        with conn:
            if self.verbose:
                print('connected by', addr)
            while True:
                
                # get message
                msg = self._recv(conn)
                rspns = self.parse_msg(msg)
                
                # check to stop
                if self.stop_commun:
                    if self.verbose:
                        print('stop communication')
                    break
                
                # send response
                self.send_response(conn, rspns)


    def close(self):
        self.s.close()
                    
    def _recv(self, conn):
        msg = conn.recv(self.BYTE_STRING_SIZE)
        if self.verbose:
            print('received: ', msg)
        return msg
    
    def parse_msg(self, msg):
        
        # if msg.decode() in self.CONTROL_COMMANDS:
        #     msg = msg.decode().replace(' ', '_')
        #     mthd = getattr(self, msg)
        #     rspns = mthd()
        if msg == b'stop communication':
            self.stop_commun = True
            rspns = b''
        elif msg == b'get attributes':
            # rspns = ','.join(self.dev.__dict__.keys()).encode()
            rspns = ','.join(self.device_attributes).encode()
        elif self._is_device_attribute(msg):
            msg = msg.decode()
            rspns = str(getattr(self.dev, msg)).encode()
        else:           
            rspns = msg + b'82'
        return rspns

    def send_response(self, conn, msg):
        conn.sendall(msg)


    # ===================================
    # control commands
    # ===================================
    def stop_communication(self):
        self.stop_commun = True
        rspns = b''
        return rspns        
    
    def get_attributes(self):
        rspns = ','.join(self.device_attributes).encode()
        return rspns
    
    
    # ===================================
    # 
    # ===================================
    
    def _set_device(self, dev):
        self.dev = dev
        self._compile_device_methods()
        
    def _complie_device_methods(self):
        
        _attrs = [ # exclude dunder functions
            s for s in dir(self.dev) if '__' not in s
        ]
        
        # compile list of non-callable attributes
        attributes = [ 
            s for s in _attrs if not callable(getattr(self.dev, s))
        ]
        self.device_attributes = attributes
        
        # compile list of callable attributes
        methods = [ 
            s for s in _attrs if callable(getattr(self.dev, s))
        ]
        self.device_methods = methods

    def _is_device_attribute(self, msg):
        msg = msg.decode()
        # if msg in self.dev.__dict__.keys():
        if msg in self.device_attributes:
            return True
        else:
            False

    def _is_device_method(self, msg):
        msg = msg.decode()
        
        if msg in self.device_methods:
            return True
        else:
            False
        







# =======================================================================
# 
# =======================================================================

if __name__ == "__main__":
        
    host = '127.0.0.1'  # The server's hostname or IP address
    port = 65448        # The port used by the server
    tr = TemperatureReader() 
    ps = PhantomServer(host, port, tr, verbose=True)
    
    pass








