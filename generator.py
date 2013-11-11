# Imports from Python Standard Library
from socket import gaierror
# Imports from Pillow
from PIL import Image, ImageDraw
# Imports from our package
import font, network

# Parse the background texture
texture = Image.open("static/texture.png")
texture = texture.resize((60,60))
texture = texture.point(lambda p: p * 0.17)

def _repeat(image, pattern):
    ''' Repeat the pattern over the image
    '''
    iw, ih = image.size
    pw, ph = pattern.size
    x = 0
    while x < iw:
        y = 0
        while y < ih:
            image.paste(pattern, (x, y))
            y += ph
        x += pw
    return image

def generate_big(name, adress, port=25565, version='1.7'):
    assert version == '1.7' or version == '1.6'    
    # Create the image, and past the texture on it
    image = Image.new("RGB", (660, 120))
    _repeat(image, texture)
    drawer = ImageDraw.Draw(image)
    
    # Render the two strings that should be there no matter what
    font.render((5,11), font.parse(name[:25]), image)
    # This uses the drawers function, because the adress should be in a 
    # shadow colour
    drawer.text((5,77),adress+(':'+str(port) if port != 25565 else ""), 
                fill=(42,42,42), font=font.font_regular)
    
    info = dict()
    try:
        info = network.get_server_info(adress, port=port, version=version);
        font.render((5,44),font.parse(info['description'].split('\n')[0]), image)
        
        player_str = "§7" + str(info['players']['online']) + "§8/§7" + str(info['players']['max'])
        players = font.parse(player_str)
        players_width = font.get_width(players)
        font.render((image.size[0]-10-players_width,44), players, image)
        
        version_str = "§7" + info['version']['name']
        version = font.parse(version_str)
        version_width = font.get_width(version)
        font.render((image.size[0]-55-version_width,11), version, image)
    except Exception as ex:
        print('exception:', ex)
        font.render((5,44),font.parse("§4Can't reach server"), image)
    
    ping = parse_ping(info.get('ping', -1))    
    draw_ping(drawer, (image.size[0]-47,7), ping)
    
    return image

def draw_ping(drawer, xy, ping):
    x, y = xy
    if ping == -1:
        drawer.rectangle([(x+1*4-1,y+5*4),(x+2*4-2,y+7*4-1)], fill=(42,42,42))
        drawer.rectangle([(x+0*4,y+4*4),(x+1*4-1,y+6*4-1)], fill=(85,85,85))
        drawer.rectangle([(x+3*4-1,y+4*4),(x+4*4-2,y+7*4-1)], fill=(42,42,42))
        drawer.rectangle([(x+2*4,y+3*4),(x+3*4-1,y+6*4-1)], fill=(85,85,85))
        drawer.rectangle([(x+5*4-1,y+3*4),(x+6*4-2,y+7*4-1)], fill=(42,42,42))
        drawer.rectangle([(x+4*4,y+2*4),(x+5*4-1,y+6*4-1)], fill=(85,85,85))
        drawer.rectangle([(x+7*4-1,y+2*4),(x+8*4-2,y+7*4-1)], fill=(42,42,42))
        drawer.rectangle([(x+6*4,y+1*4),(x+7*4-1,y+6*4-1)], fill=(85,85,85))
        drawer.rectangle([(x+9*4-1,y+1*4),(x+10*4-2,y+7*4-1)], fill=(42,42,42))
        drawer.rectangle([(x+8*4,y+0*4),(x+9*4-1,y+6*4-1)], fill=(85,85,85))
        drawer.line([(x+4,y),(x+9*4-5,y+7*4-1)], fill=(170,0,0), width=3)
        drawer.line([(x+4,y+7*4-1),(x+9*4-5,y)], fill=(170,0,0), width=3)
    elif ping == 1:
        drawer.rectangle([(x+1*4-1,y+5*4),(x+2*4-2,y+7*4-1)], fill=(21,63,21))
        drawer.rectangle([(x+0*4,y+4*4),(x+1*4-1,y+6*4-1)], fill=(85,255,85))
        drawer.rectangle([(x+3*4-1,y+4*4),(x+4*4-2,y+7*4-1)], fill=(42,42,42))
        drawer.rectangle([(x+2*4,y+3*4),(x+3*4-1,y+6*4-1)], fill=(85,85,85))
        drawer.rectangle([(x+5*4-1,y+3*4),(x+6*4-2,y+7*4-1)], fill=(42,42,42))
        drawer.rectangle([(x+4*4,y+2*4),(x+5*4-1,y+6*4-1)], fill=(85,85,85))
        drawer.rectangle([(x+7*4-1,y+2*4),(x+8*4-2,y+7*4-1)], fill=(42,42,42))
        drawer.rectangle([(x+6*4,y+1*4),(x+7*4-1,y+6*4-1)], fill=(85,85,85))
        drawer.rectangle([(x+9*4-1,y+1*4),(x+10*4-2,y+7*4-1)], fill=(42,42,42))
        drawer.rectangle([(x+8*4,y+0*4),(x+9*4-1,y+6*4-1)], fill=(85,85,85))
    elif ping == 2:
        drawer.rectangle([(x+1*4-1,y+5*4),(x+2*4-2,y+7*4-1)], fill=(21,63,21))
        drawer.rectangle([(x+0*4,y+4*4),(x+1*4-1,y+6*4-1)], fill=(85,255,85))
        drawer.rectangle([(x+3*4-1,y+4*4),(x+4*4-2,y+7*4-1)], fill=(21,63,21))
        drawer.rectangle([(x+2*4,y+3*4),(x+3*4-1,y+6*4-1)], fill=(85,255,85))
        drawer.rectangle([(x+5*4-1,y+3*4),(x+6*4-2,y+7*4-1)], fill=(42,42,42))
        drawer.rectangle([(x+4*4,y+2*4),(x+5*4-1,y+6*4-1)], fill=(85,85,85))
        drawer.rectangle([(x+7*4-1,y+2*4),(x+8*4-2,y+7*4-1)], fill=(42,42,42))
        drawer.rectangle([(x+6*4,y+1*4),(x+7*4-1,y+6*4-1)], fill=(85,85,85))
        drawer.rectangle([(x+9*4-1,y+1*4),(x+10*4-2,y+7*4-1)], fill=(42,42,42))
        drawer.rectangle([(x+8*4,y+0*4),(x+9*4-1,y+6*4-1)], fill=(85,85,85))
    elif ping == 3:
        drawer.rectangle([(x+1*4-1,y+5*4),(x+2*4-2,y+7*4-1)], fill=(21,63,21))
        drawer.rectangle([(x+0*4,y+4*4),(x+1*4-1,y+6*4-1)], fill=(85,255,85))
        drawer.rectangle([(x+3*4-1,y+4*4),(x+4*4-2,y+7*4-1)], fill=(21,63,21))
        drawer.rectangle([(x+2*4,y+3*4),(x+3*4-1,y+6*4-1)], fill=(85,255,85))
        drawer.rectangle([(x+5*4-1,y+3*4),(x+6*4-2,y+7*4-1)], fill=(21,63,21))
        drawer.rectangle([(x+4*4,y+2*4),(x+5*4-1,y+6*4-1)], fill=(85,255,85))
        drawer.rectangle([(x+7*4-1,y+2*4),(x+8*4-2,y+7*4-1)], fill=(42,42,42))
        drawer.rectangle([(x+6*4,y+1*4),(x+7*4-1,y+6*4-1)], fill=(85,85,85))
        drawer.rectangle([(x+9*4-1,y+1*4),(x+10*4-2,y+7*4-1)], fill=(42,42,42))
        drawer.rectangle([(x+8*4,y+0*4),(x+9*4-1,y+6*4-1)], fill=(85,85,85))
    elif ping == 4:
        drawer.rectangle([(x+1*4-1,y+5*4),(x+2*4-2,y+7*4-1)], fill=(21,63,21))
        drawer.rectangle([(x+0*4,y+4*4),(x+1*4-1,y+6*4-1)], fill=(85,255,85))
        drawer.rectangle([(x+3*4-1,y+4*4),(x+4*4-2,y+7*4-1)], fill=(21,63,21))
        drawer.rectangle([(x+2*4,y+3*4),(x+3*4-1,y+6*4-1)], fill=(85,255,85))
        drawer.rectangle([(x+5*4-1,y+3*4),(x+6*4-2,y+7*4-1)], fill=(21,63,21))
        drawer.rectangle([(x+4*4,y+2*4),(x+5*4-1,y+6*4-1)], fill=(85,255,85))
        drawer.rectangle([(x+7*4-1,y+2*4),(x+8*4-2,y+7*4-1)], fill=(21,63,21))
        drawer.rectangle([(x+6*4,y+1*4),(x+7*4-1,y+6*4-1)], fill=(85,255,85))
        drawer.rectangle([(x+9*4-1,y+1*4),(x+10*4-2,y+7*4-1)], fill=(42,42,42))
        drawer.rectangle([(x+8*4,y+0*4),(x+9*4-1,y+6*4-1)], fill=(85,85,85))
    elif ping == 5:
        drawer.rectangle([(x+1*4-1,y+5*4),(x+2*4-2,y+7*4-1)], fill=(21,63,21))
        drawer.rectangle([(x+0*4,y+4*4),(x+1*4-1,y+6*4-1)], fill=(85,255,85))
        drawer.rectangle([(x+3*4-1,y+4*4),(x+4*4-2,y+7*4-1)], fill=(21,63,21))
        drawer.rectangle([(x+2*4,y+3*4),(x+3*4-1,y+6*4-1)], fill=(85,255,85))
        drawer.rectangle([(x+5*4-1,y+3*4),(x+6*4-2,y+7*4-1)], fill=(21,63,21))
        drawer.rectangle([(x+4*4,y+2*4),(x+5*4-1,y+6*4-1)], fill=(85,255,85))
        drawer.rectangle([(x+7*4-1,y+2*4),(x+8*4-2,y+7*4-1)], fill=(21,63,21))
        drawer.rectangle([(x+6*4,y+1*4),(x+7*4-1,y+6*4-1)], fill=(85,255,85))
        drawer.rectangle([(x+9*4-1,y+1*4),(x+10*4-2,y+7*4-1)], fill=(21,63,21))
        drawer.rectangle([(x+8*4,y+0*4),(x+9*4-1,y+6*4-1)], fill=(85,255,85))
        
        
    
def parse_ping(ping):
    if ping < 0:
        return -1
    elif ping < 150:
        return 5
    elif ping < 300:
        return 4
    elif ping < 600:
        return 3
    elif ping < 1000:
        return 2
    else:
        return 1   
