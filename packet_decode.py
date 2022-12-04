
import json 
from messages import client_format_dict as decode_dict, unknown_packet_type 

def is_poppable(buf):
  if (len(buf) >= 2):
    length = buf[0:2]
    length = int.from_bytes(length, 'big')
    return (len(buf) >= 2 + length)
  else:
    return False 

def pop_dict(buf):
  payload_len_bytes = buf[0:2]
  payload_len = int.from_bytes(payload_len_bytes, 'big')
  json_data = buf[2:2+payload_len]
  
  buf = buf[2+payload_len:]
  json_dict = json.loads(json_data)
  return json_dict, buf

def get_client_msg(json_dict):
  if json_dict['type'] in decode_dict.keys():
    return decode_dict[json_dict['type']](**json_dict)
  else:
    return unknown_packet_type(json_dict['type'])

def pop(buf):
  json_dict, buf = pop_dict(buf)
  return get_client_msg(**json_dict), buf 
