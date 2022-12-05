
from slice_buf_to_dict import slice_buf_to_dict 

def is_client_hello(buf):
  dict, buf = slice_buf_to_dict(buf)
  return dict['type'] == 'hello'

### Ensure is_client_hello works 
length = int.to_bytes(12, 2, 'big')
buf = length + '"type": "hello"'.encode('utf-8')
assert is_client_hello(buf) == True

# GET BACK TO THIS 
buf = length + '"type": "chat"'.encode('utf-8')
assert is_client_hello(buf) == False

def is_client_chat(buf):
  dict, buf = slice_buf_to_dict(buf)
  return dict['type'] == 'chat'