
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
