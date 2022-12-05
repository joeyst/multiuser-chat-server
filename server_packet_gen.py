
import json

def _dict_to_packet(**kwargs):
  jsoned = json.dumps(kwargs).encode('utf-8')
  length = int.to_bytes(len(jsoned), 2, 'big')
  return length + jsoned

def get_client_chat_packet_from_message(msg):
  return _dict_to_packet(type='chat', message=msg)

def get_client_hello_packet_from_nick(nick):
  return _dict_to_packet(type='hello', nick=nick)

def get_server_chat_packet_from_message_and_nick(msg, nick):
  return _dict_to_packet(type='chat', nick=nick, message=msg)

def get_server_join_packet_from_nick(nick):
  return _dict_to_packet(type='hello', nick=nick)

def get_server_leave_packet_from_nick(nick):
  return _dict_to_packet(type='leave', nick=nick)

def get_server_error_packet():
  return _dict_to_packet(type='error', msg='Unable to join server. Could be due to invalid nick name.')