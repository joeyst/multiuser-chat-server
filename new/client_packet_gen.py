
from helper.dict_to_packet import _dict_to_packet 

def get_client_chat_packet_from_message(msg):
  return _dict_to_packet(type='chat', message=msg)

def get_client_hello_packet_from_nick(nick):
  return _dict_to_packet(type='hello', nick=nick)
