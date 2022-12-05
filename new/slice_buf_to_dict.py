

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

import json


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


def slice_buf_to_dict(buf):
  data, buf = slice_buf(buf)
  return json.loads(data), buf

# buf_dict, name_dict, ready_set 