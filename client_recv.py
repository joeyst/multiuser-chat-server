
import json
from packet_decode import is_poppable, pop 

# client_recv.py
def display_messages(buf):
  while is_poppable(buf):
    msg, buf = pop(buf)
    display_msg(msg)
  return buf

def receive_input(s, buf):
  d = b'Temp'
  while (d != b''):
    d = s.recv(5)
    buf += d
  return buf 

def recv_fn(s):
  buf = b''
  while True:
    buf = display_messages(buf)
    buf = receive_input(s, buf)
