
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

# Sorry for some confusing logic between 'join' and 'hello' here.... was a headache writing 
# this and don't have the time to fix it. 
def get_server_join_packet(nick):
  return dict_to_packet(type='join', nick=nick)

def get_server_leave_packet(nick):
  return dict_to_packet(type='leave', nick=nick)

def get_server_error_packet():
  return dict_to_packet(type='error', msg='Unable to join server. Could be due to invalid nick name.')

def get_server_chat_packet_from_message_and_nick(msg, nick):
  return dict_to_packet(type='chat', nick=nick, message=msg)

def get_server_join_packet_from_nick(nick):
  return dict_to_packet(type='hello', nick=nick)

def get_server_leave_packet_from_nick(nick):
  return dict_to_packet(type='leave', nick=nick)
