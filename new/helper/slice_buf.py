
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
