import socket
from io import BytesIO
from json import loads as decodejson
from codecs import getencoder, getdecoder
from time import time
from struct import pack, unpack
from base64 import b64decode

def encodeutf8(value):
    return getencoder('utf8')(value)[0]
def decodeutf8(value):
    return getdecoder('utf8')(value)[0]

PROTOCOL_VERSION = 4

class Packet (object):
    ''' Packet object
    Represents a packet to be received or sent to/from a Minecraft server

    This object is abstract, either the code or decode method must be implemented.
    The object extending this has access to the self.read and self.write functions,

    The read function will get the next byte in the byte buffer as an integer, and 
    move the pointer to the next byte or delete the one it read. The same byte 
    can't be read twice.

    The write function will write the byte it is passed to the buffer, it is not 
    possible to access any bytes located before this byte in the buffer.

    In addition to these the extending object had access to methods to read and
    write integers, longs, strings and varints to the buffer.
    '''
    def __init__(self, socket):
        ''' Init a new packet
        An exception is raised if the socket is None
        '''
        if socket == None:
            raise Exception("Need a socket")
        self.socket = socket
    
    def send(self, *a, **kw):
        ''' Send this packet to the underlaying socket
        Arguments are forwarded to the code method of the packet.
        '''
        # The data bytearray is the main part of the package
        data = bytearray()
        def write1(byte):
            data.append(byte)
        self.write = write1
        
        # Write the main part of the packet to the data bytearray
        self.write_varint(self.packetid)
        self.code(*a, **kw)
        
        # The packet bytearray is the finished bytes we'll send
        packet = bytearray()
        def write2(byte):
            packet.append(byte)
        self.write = write2
        
        # Write the lenght and then the main part of the packet to the packet bytearray
        self.write_varint(len(data))
        packet.extend(data)
        self.socket.send(packet)
        
        del self.write
    
    def receive(self):
        ''' Receive this packet from the socket.
        The return value is from the decode method of the packet.
        '''
        # Receive the header of the packet. We need to get at least the lenght _varint
        header = bytearray(self.socket.recv(64))
        def read1():
            return header.pop(0)
        self.read = read1
        lenght = self.read_varint()
        # We now have the lenght of the whole packet, and header now contains the start of the main part of the packet
        
        # Calculate how many bytes we have left to receive, and get them
        bytesremaining = lenght - len(header)
        packet = None
        if bytesremaining > 0:
            packet = bytearray()
            packet.extend(header)
            while True:
                # Try to receive the rest of the packet, else, try again.
                packet.extend(self.socket.recv(bytesremaining))
                bytesremaining = lenght - len(packet)
                if bytesremaining < 1:
                    break
        else:
            packet = header
        
        def read2():
            return packet.pop(0)
        self.read = read2
        
        # Check we are receiving the correct packet
        assert self.read_varint() == self.packetid
        
        result = self.decode()
        
        del self.read
        return result
        
    def write_string(self, _string):
        ''' Write a _string to the buffer
        '''
        data = encodeutf8(_string)
        self.write_varint(len(_string))
        for b in data:
            self.write(b)
    
    def read_string(self):
        ''' Read a _string from the buffer
        '''
        lenght = self.read_varint()
        data = bytearray()
        for i in range(0, lenght):
            data.append(self.read())
        return decodeutf8(data)
    
    def write_varint(self, value):
        ''' Write a _varint formatted integer to the buffer
        '''
        part = 0
        while True:
            part = value & 0x7F
            value >>= 7
            if value != 0:
                part |= 0x80
            self.write( part )
            if value == 0:
                break
        
    def read_varint(self):
        ''' Read a _varint integer from the buffer.
        '''
        out = 0
        data = 0
        new = 0
        while True:
            new = self.read()
            out |= ( new & 0x7F ) << ( data * 7 )
            data = data +1
            if data > 32:
                raise Exception("_varint too big!")
            if ( new & 0x80 ) != 0x80:
                break
        return out
    
    def write_unsigned_short(self, value):
        ''' Write an unsigned short to the buffer
        '''
        data = bytes(pack('>H', value))
        for b in data:
            self.write(b)
    
    def read_unsigned_short(self):
        ''' Read an unsigned short from the buffer.
        '''
        data = bytearray()
        for i in range(0,2):
            data.append(self.read())
        return unpack('>H', data)[0]
    
    def write_packed_long(self, value):
        ''' Write a long to the buffer.
        '''
        data = bytes(pack('>q', value))
        for b in data:
            self.write(b)
    
    def read_packed_long(self):
        ''' Read a long from the buffer.
        '''
        data = bytearray()
        for i in range(0,8):
            data.append(self.read())
        return unpack('>q', data)[0]
        
    def code(self, *a, **kw):
        raise Exception('code(self, *a, **kw) not set')
    
    def decode(self):
        raise Exception('decode(self) not set')
        
class HandShakePacket(Packet):
    packetid = 0x00
    
    def code(self, adress, port, state):
        self.write_varint(PROTOCOL_VERSION)
        self.write_string(adress)
        self.write_unsigned_short(port)
        self.write_varint(state)
    
    def decode(self):
        raise Exception('Not implemented')
    
class RequestPacket(Packet):
    packetid = 0x00
    
    def code(self):
        pass
    
    def decode():
        raise Exception('Not implemented')
    
class ResponsePacket(Packet):
    packetid = 0x00
    
    def code(self):
        raise Exception('Not implemented')
    
    def decode(self):
        return self.read_string()

class PingPacket(Packet):
    packetid = 0x01
    
    def code(self, value):
        self.write_packed_long(value)
    
    def decode(self):
        return self.read_packed_long()

def server_status(host='localhost', port=25565, timeout=3.0):
    ''' Go through the process of receiving a servers status
    '''
    # Get the socket ready
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    s.connect((host, port)) 
    
    # send handshake packet
    handshake = HandShakePacket(s)
    handshake.send(host, port, 1)
    
    # send request packet
    request = RequestPacket(s)
    request.send()
    
    # receive response packet
    responsepacket = ResponsePacket(s)
    response = responsepacket.receive()
    
    # send and receive ping packet
    ping = PingPacket(s)
    ping.send(round(time()*1000))
    recv = ping.receive()
    ping = round(time()*1000) - recv # TODO this is always 0
    
    # Decode the json
    response = decodejson(response)
    
    # Put the favicon into a BytesIO in the dict
    if 'favicon' in response:
        favicon = response['favicon']
        favicontype = favicon[:22]
        assert favicontype == 'data:image/png;base64,'
        favicon = BytesIO(b64decode(favicon[22:]))
        response['favicon'] = favicon
    else:
        response['favicon'] = None
    
    # Add the ping to the dict
    response['ping'] = ping
    return response
