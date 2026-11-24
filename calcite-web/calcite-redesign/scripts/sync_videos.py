import os, re, json, urllib.request, xml.etree.ElementTree as ET
channel=os.environ.get('YOUTUBE_CHANNEL_ID','')
if not re.fullmatch(r'UC[A-Za-z0-9_-]{22}',channel): raise SystemExit('Set repository variable YOUTUBE_CHANNEL_ID to your actual UC channel ID.')
url='https://www.youtube.com/feeds/videos.xml?channel_id='+channel
with urllib.request.urlopen(url,timeout=30) as response: root=ET.fromstring(response.read())
ns={'a':'http://www.w3.org/2005/Atom','yt':'http://www.youtube.com/xml/schemas/2015'}
items=[{'id':x.findtext('yt:videoId',namespaces=ns),'title':x.findtext('a:title',namespaces=ns),'category':'Minecraft'} for x in root.findall('a:entry',ns)]
if not items: raise SystemExit('Empty feed; retaining old videos')
with open('videos.json','w',encoding='utf-8') as f: json.dump(items,f,ensure_ascii=False,indent=2)
