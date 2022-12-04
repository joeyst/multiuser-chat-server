
import json
from packet_decode import pop_dict

def dict_to_packet(**kwargs):
  jsoned = json.dumps(kwargs).encode('utf-8')
  length = int.to_bytes(len(jsoned), 2, 'big')
  return length + jsoned



# Client packet generation 
def get_client_chat_packet(msg):
  return dict_to_packet(type='chat', message=msg)

def get_client_hello_packet(nick):
  return dict_to_packet(type='hello', nick=nick)



# Server packet generation 
def get_server_chat_packet(msg, nick):
  return dict_to_packet(type='chat', nick=nick, message=msg)

def get_server_join_packet(nick):
  return dict_to_packet(type='join', nick=nick)

def get_server_leave_packet(nick):
  return dict_to_packet(type='leave', nick=nick)

def get_server_error_packet():
  return dict_to_packet(type='error', msg='Unable to join server. Could be due to invalid nick name.')

def is_client_hello(packet):
  if (len(packet) < 2):
    return False

  json_dict, _ = pop_dict(packet)
  try:
    if (json_dict['type'] == 'hello'):
      return True
    else:
      return False
  except:
    return False 

def get_nick(packet):
  return pop_dict(hello_packet)['nick']