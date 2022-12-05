
import json
from packet_decode import is_poppable, pop 

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

def get_chat_msg(nick, message, **_):
  return "{}: {}".format(nick, message)

def get_join_msg(nick, **_):
  return "*** {} has joined the chat".format(nick)

def get_leave_msg(nick, **_):
  return "*** {} has left the chat".format(nick)

def unknown_packet_type(packet_type):
  return "Error, unknown packet type {}.".format(packet_type)

client_format_dict = {
  'chat': get_chat_msg,
  'hello': get_join_msg,
  'leave': get_leave_msg
}

def _get_length_from_first_two_bytes(buf):
  return int.from_bytes(buf[0:2], 'big')

def _get_remaining_buffer(buf):
  length = _get_length_from_first_two_bytes(buf)
  return buf[2+length:]

def _get_slice_data(buf):
  length = _get_length_from_first_two_bytes(buf)
  return buf[2:2+length]

def slice_buf(buf):
  return _get_slice_data(buf), _get_remaining_buffer(buf)

### Ensuring 
length = int.to_bytes(12, 2, 'big')
packet = length + b'abc'
assert slice_buf(packet) == (b'abc', b'')

packet = length + b'abcdefghijklmnopqrst'
assert slice_buf(packet) == (b'abcdefghijkl', b'mnopqrst')

import json

def slice_buf_to_dict(buf):
  data, buf = slice_buf(buf)
  return json.loads(data), buf

# buf_dict, name_dict, ready_set 


def display_packet_from_dict(bdict):
  print(client_format_dict[bdict['type']](**bdict))