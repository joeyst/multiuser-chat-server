
from chatui import read_command 
from packet_gen import get_client_chat_packet, get_client_hello_packet  

def client_prompt(name):
  return read_command("{}> ".format(name))

def is_quit(msg):
  return (msg == "/quit")

def is_command(msg):
  if (len(msg) == 0):
    return False
  elif (msg[0] != "/"):
    return False
  else:
    return True 

def unknown_cmd(msg):
  return "Unknown command {}".format(msg)

def input_fn(name, s):
  s.send(get_client_hello_packet(name))
  while True:
    msg = client_prompt(name)
    if is_quit(msg):
      return
    elif is_command(msg):
      print(unknown_cmd(msg))
    else:
      packet = get_client_chat_packet(msg)
      s.send(packet)
