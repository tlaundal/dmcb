# Imports from dependency
from dns import resolver
# Imports from package
from mc_protocol import server_status
    
def get_server_info(host, port = 25565, timeout=3.0, check_srv = True):
    """Returns the information the client receives when listing servers
    on the "server-selection" screen.
    The dict is contains:
    * protocol_version,
    * server_version,
    * motd,
    * players,
    * max_players
    """
    if port == 25565 and check_srv:
        host, port = get_host_port_srv(host)
        if port == None:
            port = 25565
    
    return server_status(host, port)
     
def get_host_port_srv(host):
    ''' Get host,port tuple
    Resolve the Minecraft SRV records for the host and return the first host,
    port pair received from resolve_srv
    '''
    for srv in resolve_srv(host):
        return (srv[0], srv[1])
    return (host, None)
            
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
