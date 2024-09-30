from PIL import Image
import argparse
import json
import textwrap

def rgb2hex(rgb):
  return '%02x%02x%02x%02x' % rgb

def hex2rgb(hex):
  return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4,6))

ap = argparse.ArgumentParser('SUIF')
ap.add_argument('action')
ap.add_argument('filename')
ap.add_argument('output')
args = ap.parse_args()

if args.action == 'to':
  img = Image.open(args.filename)
  img = img.convert('RGBA')
  data = [img.size[0],img.size[1],""]
  for y in range(img.size[1]):
    for x in range(img.size[0]):
      data[2]+=rgb2hex(img.getpixel((x,y)))
  with open(args.output, 'w') as f:
    f.write(json.dumps(data))
  img.close()
    
if args.action in ['from','show']:
  with open(args.filename) as f:
    json = json.loads(f.read())
    json[2] = textwrap.wrap(json[2], 8)
    img = Image.new('RGBA',json[0:2])
    data = img.load()
    for y in range(json[1]):
      for x in range(json[0]):
        data[x,y] = hex2rgb(json[2][(y*json[0])+x])
    img.save(args.output)
