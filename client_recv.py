
import json
from packet_decode import is_poppable, pop 
from messages import *
from slice_buf import *

# client_recv.py
def display_messages(buf):
  while is_poppable(buf):
    msg, buf = pop(buf)
    display_msg(msg)
  return buf

def is_long_enough_to_get_length(buf):
  return len(buf) >= 2

def get_length_from_first_two_bytes(buf):
  return int.from_bytes(buf[0:2], 'big')

def is_long_enough_to_pop(buf):
  return get_length_from_first_two_bytes(buf) + 2 <= len(buf)

def can_pop(buf):
  return is_long_enough_to_get_length(buf) \
    and is_long_enough_to_pop(buf)

### Making sure can_pop works. 
length = int.to_bytes(12, 2, 'big')
packet = length + b'abc'
assert can_pop(packet) == False

packet = length + b'abcdefghijklmnopqrst'
assert can_pop(packet) == True

length = int.to_bytes(12, 1, 'big')
packet = length + b''
assert can_pop(packet) == False


def receive_input(s, buf):
  d = b'Temp'
  while (d != b''):
    d = s.recv(5)
    buf += d
  return buf 

def recv_fn(s):
  buf = b''


  while True:
    if can_pop(buf):
      bdict, buf = slice_buf_to_dict(buf)
      display_packet_from_dict(bdict)

    d = s.recv(5)
    if (len(d) == 0):
      return None 
    buf += d 

  # while True:
  #   buf = display_messages(buf)
  #   buf = receive_input(s, buf)

client_format_dict = {
  'chat': get_chat_msg,
  'hello': get_join_msg,
  'leave': get_leave_msg
}

def display_packet_from_dict(bdict):
  print(client_format_dict[bdict['type']](**bdict))