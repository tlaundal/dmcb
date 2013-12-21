# Package: dmcb
from struct import pack
from time import time
import socket

from dns import resolver

from dmcb.mc_protocol import server_status
    
def get_server_info(host, port=25565, check_srv = True):
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
    
    # Check DNS results from the nameservers
    if port == 25565 and check_srv:
        host, port = get_host_port_srv(host)
    
    return server_status(host, port)
     
     
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
