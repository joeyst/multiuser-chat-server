
import select 
from slice_buf_to_dict import slice_buf_to_dict 
from server_packet_gen import get_server_join_packet_from_nick, get_server_chat_packet_from_message_and_nick 
from broadcast import broadcast 

def handle_pop(client_sockets, buffer_dict, nick_dict):
  for s, buf in buffer_dict.items():
    bdict, rest = slice_buf_to_dict(buf)
    buffer_dict[s] = rest
    if (bdict['type'] == 'hello'):
      # Ignoring logic to handle if name already in `nick_dict`
      nick_dict[s] = bdict['nick']
      packet_to_broadcast = get_server_join_packet_from_nick(bdict['nick'])
      broadcast(client_sockets, packet_to_broadcast)
    elif (bdict['type'] == 'chat'):
      # Ignoring logic to handle if name not in `nick_dict` 
      packet_to_broadcast = get_server_chat_packet_from_message_and_nick(bdict['message'], bdict['nick'])
      broadcast(client_sockets, packet_to_broadcast)
    else:
      print("Error, handle_pop {} type not found".format(bdict['type']))
  return client_sockets, buffer_dict, nick_dict 