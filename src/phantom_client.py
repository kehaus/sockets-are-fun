#!/usr/bin/env python3
"""
client class to allow for TCP control of python objects from host computer


example from here:
    https://realpython.com/python-sockets/

"""

import socket




# =======================================================================
# 
# =======================================================================


class PhantomClient():
    """ """
    BYTE_STRING_SIZE = 1024
    
    def __init__(self, host, port, verbose=False):
        
        self.verbose = verbose
        self._init_socket(host, port)
        self.query_device_attributes()

        
    def _init_socket(self, host, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))        
        
    def send_msg(self, msg):
        self._sendall(msg)
        rspns = self._recv()
        return rspns
        

    def _sendall(self, msg):
        if self.verbose:
            print('send: ', msg)
        self.s.sendall(msg)
    
    def _recv(self):
        rspns = self.s.recv(self.BYTE_STRING_SIZE)
        if self.verbose:
            print('Received: ', repr(rspns))
        return rspns
    
    def close(self):
        self.s.close()
        
    # ==============================================================
    # 
    # ==============================================================
    
    def stop_communication(self):
        msg = b'stop communication'
        return self.send_msg(msg)
    
    def query_device_attributes(self):
        msg = b'get attributes'
        rspns = self.send_msg(msg)
        self.dev_attributes = rspns.decode().split(',')

    def __getattr__(self, item):
        print('item')
        
        if item in self.dev_attributes:
            msg = item.encode()
            return self.send_msg(msg)
        else:
            return super().__getattr__(item)
        

# =======================================================================
# 
# =======================================================================



if __name__ == "__main__":
        
    host = '192.168.1.143'  # The server's hostname or IP address
    port = 65451        # The port used by the server

    
    

    pass












