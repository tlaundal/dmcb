# Imports from Python Standard Library
from struct import pack
from time import time
from dns import resolver
import socket

PROTOCOL_VERSION = 74

def pack_string(string):
    """Packs a string."""
    return pack('>h', len(string)) + string.encode('utf-16be')
    
def get_server_info(host, port, timeout=3.0, check_srv = True):
    """Returns the information the client receives when listing servers
    on the "server-selection" screen.
    The dict is contains:
    * protocol_version,
    * server_version,
    * motd,
    * players,
    * max_players
    """
    # If we should check SRV, we try that
    if port == 25565 and check_srv:
        # Fetch SRV records
        srvs = resolve_srv(host)
        # If we got any, those are the only that count
        if len(srvs) > 0:
            for srv in srvs:
                try:
                    return get_server_info(srv[0], srv[1], check_srv = False)
                except Exception:
                    pass
            raise Exception("Sorry mac, no server here!")
            
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    # Get the current time in millis
    t = int(time()*1000) 
    s.connect((host, port)) 
       
    # Send 0xFE: Server list ping with 'magic' payload: "\x01"
    s.send(b"\xfe")
    s.send(b"\x01")
    
    # Send 0xFA plugin message
    s.send(b"\xfa") # Packet identifier
    s.send(pack_string("MC|PingHost"))# Message identifier
    s.send(pack(">h", 7 + 2 * len(host))) # Payload length
    s.send(pack("b", PROTOCOL_VERSION)) # protocol version
    s.send(pack_string(host)) # host
    s.send(pack(">i", port))
    
    # Read as much data as we can, then close the socket.
    data = s.recv(1024)
    s.close()
    
    # The ping!
    ping = int(time()*1000) - t
    
    #Check we've got a 0xFF Disconnect
    assert data[0] == 0xff
    
    #Remove: packet ident (0xFF), short containing the length of the string
    data = data[3:] # packet ident: 1 byte, short: 2 bytes, total: 3 bytes
    #Decode UCS-2 string
    data = data.decode('utf-16be')
    
    # Check that the first 3 characters were what we expected.
    # Then throw them away.
    assert data[:3] == u"\xa7\x31\x00"
    data = data[3:]
    
    # Split
    data = data.split("\x00")
    return {"protocol_version": int(data[0]),
            "minecraft_version": data[1],
            "motd": data[2],
            "players": int(data[3]),
            "max_players": int(data[4]),
            "ping": ping}
            
def resolve_srv(adress):
    ''' Resolve SRV records
    Get all the SRV records for the adress and return them in an ordered array
    of tuples, with target adress and port
    RETURNS an array
    '''
    try:
        answers = resolver.query('_minecraft._tcp.' + adress, 'SRV')
        ordered = sorted(answers, key=lambda x: (x.priority, -x.weight))
        result = list()
        return [(x.target.to_text()[:-1], x.port) for x in ordered]
    except Exception:
        return []
