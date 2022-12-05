
import select 
from collect_data_from_list_of_clients import collect_data_from_single_client
from server_packet_gen import get_server_leave_packet_from_nick, get_server_chat_packet_from_message_and_nick 
from server_packet_gen import get_server_join_packet_from_nick 

from can_pop import can_pop 
from slice_buf_to_dict import slice_buf_to_dict 
from broadcast import broadcast 

# def handle_recv_from_clients(clients, buffer_dict, nick_dict):
#   ready, _, _ = select.select(clients, {}, {})
#   for s in ready:
# 
#     d = collect_data_from_single_client(s)
#     if (len(d) == 0):
#       packet_to_broadcast = get_server_leave_packet_from_nick(nick_dict[s])
#       broadcast(clients, packet_to_broadcast)
#       clients.remove(s)
#     else:
#       buffer_dict[s] += d
#   return clients, buffer_dict, nick_dict 
# 
#   # if complete, return 
#   # if guaranteed to be ready. If empty, then break 
#   # 

def handle_recv_from_clients(clients, buffer_dict, nick_dict):
  print("Before select")
  ready, _, _ = select.select(clients, {}, {})
  print("After select")
  for s in ready:
    pdict, buffer_dict, nick_dict = \
      get_dict_for_packet_via_receive_input_from_ready_client(s, buffer_dict, nick_dict) 
    
    # accept connection is handled elsewhere 

    if pdict == None: 
      packet_to_broadcast = get_server_leave_packet_from_nick(nick_dict[s])
      broadcast(clients, packet_to_broadcast)
      clients.remove(s)
      s.close()

    if (pdict['type'] == 'hello'):
      print("Hello packet in handle_recv_from_clients")
      packet_to_broadcast = get_server_join_packet_from_nick(pdict['nick'])
      nick_dict[s] = pdict['nick']
      broadcast(clients, packet_to_broadcast)
      
    if (pdict['type'] == 'chat'): 
      packet_to_broadcast = get_server_chat_packet_from_message_and_nick(pdict['message'], nick_dict[s])
      broadcast(clients, packet_to_broadcast)
  return clients, buffer_dict, nick_dict 

def get_dict_for_packet_via_receive_input_from_ready_client(s, buffer_dict, nick_dict):
  # `s` is client socket, shortened for readability 
  while True:
    print("S:", s)
    print("buffer_dict: ", buffer_dict)
    print("nick_dict:", nick_dict)
    if can_pop(buffer_dict[s]):
      pdict, rest_of_buf = slice_buf_to_dict(buffer_dict[s])
      buffer_dict[s] = rest_of_buf 
      return pdict, buffer_dict, nick_dict 
    
    # before reciv 
    d = s.recv(4096)
    # after recv
    if (len(d) == 0):
      return None, buffer_dict, nick_dict 
    buffer_dict[s] += d
