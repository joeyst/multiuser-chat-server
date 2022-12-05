
import select 
from collect_data_from_list_of_clients import collect_data_from_single_client 
from slice_buf_to_dict import slice_buf_to_dict 

def handle_accept(listening_sockets, client_sockets, buffer_dict, nick_dict):
  ready, _, _ = select.select(listening_sockets, {}, {})
  for s in ready:
    if s in client_sockets:
      print("Error: s in client_sockets")
    print("handle_accept")
    new_conn, addr = s.accept()
    buffer_dict[new_conn] = b''
    
    print("New connection:", new_conn.getpeername())
    client_sockets.add(new_conn)
  print("exiting handle accept")
  return listening_sockets, client_sockets, buffer_dict, nick_dict 