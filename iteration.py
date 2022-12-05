import socket, select, sys, threading 

from packet_gen import is_client_hello, get_server_error_packet, get_nick 
from packet_decode import pop_dict, is_poppable

from chat_servers import ClientTracker 

# Iterating through buffer dictionary (third set for chat_server.py)
def iterate_pop_and_broadcast_msg(client_tracker):
  for s, buf in client_tracker.buffer_dict.items():
    if is_poppable(buf):
      dicted = pop_tracker_packet(client_tracker, s)
      if dicted is not None:
        handle_named_or_unnamed(client_tracker, buf, s, dicted)

def handle_named_or_unnamed(client_tracker, buf, s, dicted):
  if client_tracker.is_not_named(s):
    handle_join(client_tracker, s, dicted)
  else:
    msg_packet = get_tracker_msg_packet(client_tracker, dicted, s)
    client_tracker.broadcast(msg_packet)

def handle_join(client_tracker, s, dicted):
  print("handle_join, line 24")
  if ('type' in dicted.keys()) and (dicted['type'] == 'hello'):
    print("in 'type' in dicted.keys(), line 26")
    print("hello packet received")
    client_tracker.socket_nick[s] = dicted['name']
    # TODO: BROADCAST HELLO PACKET 
    print(dicted['name'], "joined the chat")
  else:
    s.send(get_server_error_packet())
    s.close()
    del client_tracker.buffer_dict[s]
    print("Client {} disconnected".format(s.getpeername()))

def pop_tracker_packet(client_tracker, s):
  if is_poppable(client_tracker.buffer_dict[s]):
    dicted, buf = pop_dict(client_tracker.buffer_dict[s])
    client_tracker.buffer_dict[s] = buf
    return dicted
  return None

def get_tracker_msg_packet(client_tracker, dicted, s):
  msg = dicted['message']
  nick = client_tracker.socket_nick[s]
  return get_server_chat_packet(msg, nick)




# Iterating through ready listening sockets (first set for chat_server.py)
def iterate_accept(client_tracker):
  ready, _, _ = select.select(client_tracker.listening_set, {}, {})
  for s in ready:
    new_conn, addr = s.accept()
    print(new_conn.getpeername(), "connected")
    client_tracker.buffer_dict[new_conn] = b''




# Iterating through clients (second set for chat_server.py) 
def iterate_clients(client_tracker):
  ready, _, _ = select.select(set(client_tracker.buffer_dict.keys()), {}, {})
  for s in ready:
    d = s.recv(BYTES_PER_RECV)
    client_tracker.buffer_dict[s] += d
    
################# TRYING OUT #################

# sample command line: `python chat_server.py 3490`
def usage():
    print("usage: python3 chat_server.py port", file=sys.stderr)

try:
  PORT = int(sys.argv[1])
except:
  usage()
  sys.exit()

BYTES_PER_RECV = 4096

listen = socket.socket()
listen.bind(('', PORT))
listen.listen()

print("waiting for connections")

ct = ClientTracker({listen})
while True:
  iterate_pop_and_broadcast_msg(ct)
  iterate_accept(ct)
  iterate_clients(ct)
  print("ct.buffer_dict:", ct.buffer_dict)
  print("ct.socket_nick:", ct.socket_nick)
  print("ct.listening_set:", ct.listening_set)
