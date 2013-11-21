# Package: dmcb
from struct import pack
from time import time
import socket

from dns import resolver

from dmcb.mc_protocol import server_status
    
def pack_string(string):
    ''' Pack the string so it can be sent to a 1.6 minecraft server
    '''
    return pack('>h', len(string)) + string.encode('utf-16be')
    
def get_server_info(host, port=25565, version='1.7', check_srv = True):
    ''' Get information about a minecraft server
    The result is a dict which looks like this:
    {
        version:
            {
                protocol,
                name
            },
        players:
            {
                online,
                max
            },
        description,
        ping
    }      
    '''
    # Version should either be '1.7' or '1.6'
    assert version == '1.7' or version == '1.6'
    
    # Check DNS results from the nameservers
    if port == 25565 and check_srv:
        host, port = get_host_port_srv(host)
    
    if version == '1.7':
        # 1.7 protocol is in the mc_protocol module
        return server_status(host, port)
    elif version == '1.6':
        # 1.6 protocol
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(6.0)
        t = int(time()*1000)
        s.connect((host, port))
        s.send(b"\xfe")
        s.send(b"\x01")
        s.send(b"\xfa")
        s.send(pack_string("MC|PingHost"))
        s.send(pack(">h", 7 + 2 * len(host)))
        s.send(pack(">b", 78))
        s.send(pack_string(host))
        s.send(pack(">i", port))
        data = s.recv(1024)
        s.close()
        ping = int(time()*1000) - t
        assert data[0] == 0xff
        data = data[3:]
        data = data.decode('utf-16be')
        assert data[:3] == u"\xa7\x31\x00"
        data = data[3:]
        data = data.split("\x00")
        return {"version":
                {
                    'protocol':int(data[0]),
                    'name': data[1]
                },
                "description": data[2],
                "players": 
                {
                    'online': int(data[3]),
                    'max': int(data[4])
                },
                "ping": ping}
     
     
def get_host_port_srv(host):
    ''' Get host,port tuple
    Resolve the Minecraft SRV records for the host and return the first
    host, port pair received from resolve_srv, or the host supplied 
    and 25565 if no srv records where found.
    '''
    for srv in resolve_srv(host):
        return (srv[0], srv[1])
    return (host, 25565)
            
def resolve_srv(adress):
    ''' Resolve SRV records
    Get all the SRV records for the adress and return them in an 
    ordered array of tuples, with target adress and port
    RETURNS an array
    '''
    try:
        answers = resolver.query('_minecraft._tcp.' + adress, 'SRV')
        ordered = sorted(answers, key=lambda x: (x.priority, -x.weight))
        result = list()
        return [(x.target.to_text()[:-1], x.port) for x in ordered]
    except Exception:
        return []
