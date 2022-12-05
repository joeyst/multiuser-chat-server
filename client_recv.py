
import json
from packet_decode import is_poppable, pop 
from messages import *
from slice_buf_to_dict import *
from can_pop import * 
from chatui import print_message

client_format_dict = {
  'chat': get_chat_msg,
  'hello': get_join_msg,
  'leave': get_leave_msg
}

def display_packet_from_dict(bdict):
  print_message(client_format_dict[bdict['type']](**bdict))

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

