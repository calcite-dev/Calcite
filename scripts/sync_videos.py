import os,re,json,urllib.request,xml.etree.ElementTree as ET
channel=os.environ.get('YOUTUBE_CHANNEL_ID','').strip()
if not channel:
    req=urllib.request.Request('https://www.youtube.com/@calcitemc',headers={'User-Agent':'Mozilla/5.0'})
    with urllib.request.urlopen(req,timeout=25) as r: html=r.read().decode('utf-8','replace')
    m=re.search(r'<link[^>]+href="https://www.youtube.com/channel/(UC[A-Za-z0-9_-]{22})"[^>]*>',html) or re.search(r'"externalId":"(UC[A-Za-z0-9_-]{22})"',html)
    if not m: raise RuntimeError('Set YOUTUBE_CHANNEL_ID repository variable to channel ID')
    channel=m.group(1)
if not re.fullmatch(r'UC[A-Za-z0-9_-]{22}',channel): raise ValueError('Invalid channel ID')
with urllib.request.urlopen('https://www.youtube.com/feeds/videos.xml?channel_id='+channel,timeout=25) as r: root=ET.fromstring(r.read())
ns={'a':'http://www.w3.org/2005/Atom','yt':'http://www.youtube.com/xml/schemas/2015'}
items=[{'id':x.findtext('yt:videoId',namespaces=ns),'title':x.findtext('a:title',namespaces=ns),'category':'Minecraft'} for x in root.findall('a:entry',ns)]
if not items: raise RuntimeError('No public uploads returned')
with open('_site/videos.json','w',encoding='utf-8') as f: json.dump(items,f,ensure_ascii=False)
