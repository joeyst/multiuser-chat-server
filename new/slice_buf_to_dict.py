
from helper.slice_buf import slice_buf 
import json

def slice_buf_to_dict(buf):
  data, buf = slice_buf(buf)
  return json.loads(data), buf
