import socket,json,urllib.request,base64,os,struct,time
from pathlib import Path
from urllib.parse import urlsplit
pages=json.load(urllib.request.urlopen('http://localhost:9223/json'))
u=urlsplit(pages[0]['webSocketDebuggerUrl']);sock=socket.create_connection((u.hostname,u.port));key=base64.b64encode(os.urandom(16)).decode()
sock.sendall(f'GET {u.path} HTTP/1.1\r\nHost: {u.netloc}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\nOrigin: http://localhost:9223\r\n\r\n'.encode())
data=b''
while b'\r\n\r\n' not in data:data+=sock.recv(1)
def read(n):
 b=b''
 while len(b)<n:b+=sock.recv(n-len(b))
 return b
i=0
def cmd(method,params={}):
 global i
 i+=1;b=json.dumps(dict(id=i,method=method,params=params)).encode();mask=os.urandom(4);n=len(b)
 h=bytes([129,128+n]) if n<126 else bytes([129,254])+struct.pack('!H',n)
 sock.sendall(h+mask+bytes(v^mask[j%4] for j,v in enumerate(b)))
 while True:
  h=read(2);n=h[1]&127
  if n==126:n=struct.unpack('!H',read(2))[0]
  elif n==127:n=struct.unpack('!Q',read(8))[0]
  r=json.loads(read(n))
  if r.get('id')==i:return r.get('result',r)
cmd('Emulation.setDeviceMetricsOverride',dict(width=390,height=844,deviceScaleFactor=1,mobile=True))
cmd('Page.navigate',dict(url='file:///E:/Sir%20Profile/index.html'))
time.sleep(4)
print(cmd('Runtime.evaluate',dict(expression='JSON.stringify({width:innerWidth,scroll:document.documentElement.scrollWidth,photo:document.querySelector(".hero-portrait").getBoundingClientRect().toJSON(),contact:document.querySelector(".personal-details").getBoundingClientRect().toJSON()})',returnByValue=True)))
r=cmd('Page.captureScreenshot',dict(format='png',captureBeyondViewport=False))
Path('mobile-preview.png').write_bytes(base64.b64decode(r['data']))
print('Saved mobile-preview.png at 390 x 844')
