# Example usage:
#
# python select_server.py 3490

import sys
import socket
import select
from slice_buf_to_dict import slice_buf_to_dict
from can_pop import can_pop 
from packet_gen import * 

def usage():
    print("usage: chat_server.py port", file=sys.stderr)

try:
  port = int(sys.argv[1])
except:
  usage()
  sys.exit()

buf_dict = {}
name_dict = {} 
listening_socket = socket.socket()
listening_socket.bind(('', port))
listening_socket.listen()
ready_set = {listening_socket}


def run_server():
    global buf_dict, ready_set, listening_socket, name_dict 

    while True:
      ready_to_read, _, _ = select.select(ready_set, {}, {})

      for s in ready_to_read:
        # if socket is listener socket 
        if s == listening_socket:
          new_conn, src = s.accept()
          ready_set.add(new_conn)
          buf_dict[new_conn] = b''

        # if socket is client socket 
        else:
          # dictionary if it is a hello packet or hello packet 
          dict_or_none = get_client_packet(s)
          # If None, then client sent empty packet; the client left 
          if dict_or_none == None:
            broadcast_leave(name_dict[s])
            ready_set.remove(s)
            del buf_dict[s]
            del name_dict[s]

          # if type is hello, broadcast that the client joined and add them to the name dictionary 
          elif dict_or_none['type'] == 'hello':
            broadcast_join(dict_or_none['nick']) 
            name_dict[s] = dict_or_none['nick'] 
            
          # if type is chat, broadcast the message along with the client's name 
          elif dict_or_none['type'] == 'chat':
            broadcast_chat(dict_or_none['message'], name_dict[s])

          # if the packet is none of those types, print not registered 
          else:
            print("Packet not registered")

def broadcast_leave(name):
  broadcast(get_server_leave_packet_from_nick(name))

def broadcast_join(name):
  broadcast(get_server_join_packet_from_nick(name))

def broadcast_chat(name, msg):
  broadcast(get_server_chat_packet_from_message_and_nick(msg, name))

def broadcast(packet):
  global name_dict
  for s in name_dict.keys():
    s.send(packet)

def get_client_packet(s):
  # assumes that the socket is a client and
  # is ready from `select.select`. 
  # returns `None` or a dictionary with packet information. 
  # if it returns `None`, then it is the client disconnecting. 
  global buf_dict, name_dict, listening_socket, ready_set 

  while True:
    if can_pop(buf_dict[s]):
      bdict, rest = slice_buf_to_dict(buf_dict[s])
      buf_dict[s] = rest
      return bdict

    d = s.recv(5)
    if (len(d) == 0):
      return None 
    buf_dict[s] += d 

run_server()