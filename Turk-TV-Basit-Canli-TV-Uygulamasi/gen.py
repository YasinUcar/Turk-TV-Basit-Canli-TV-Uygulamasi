import os,urllib.request
for f,u in [('tr.m3u','https://raw.githubusercontent.com/iptv-org/iptv/master/streams/tr.m3u'),('logos.csv','https://raw.githubusercontent.com/iptv-org/database/master/data/logos.csv')]:
    if not os.path.exists(f): urllib.request.urlretrieve(u,f)
import json,re,csv
raw=open('tr.m3u',encoding='utf-8').read().replace('\r','').split('\n')
E={}  # title -> dict
for i,l in enumerate(raw):
    if not l.startswith('#EXTINF'): continue
    m=re.search(r'tvg-id="([^"]*)"',l); tid=(m.group(1).split('@')[0] if m else '')
    t=l.rsplit('",',1)[-1] if '",' in l else l.split(',',1)[-1]
    j=i+1; vlc=False
    while j<len(raw) and raw[j].startswith('#'):
        vlc=vlc or 'EXTVLCOPT' in raw[j]; j+=1
    if j<len(raw) and raw[j].startswith('http') and not vlc and t not in E: E[t]=dict(id=tid,t=t,u=raw[j])
logos={}
for r in csv.DictReader(open('logos.csv',encoding='utf-8')):
    if r['format'] in('PNG','SVG','JPEG','WebP') and r['channel'] not in logos: logos[r['channel']]=r['url']
def clean(t): return re.sub(r'\s*(\(\d+p\)|\[[^\]]*\])','',t).strip()
G=[("Ulusal Kanallar",[("TRT 1","TRT 1 (1440p)"),("ATV","ATV (1080p)"),("Kanal D","Kanal D (1080p)"),("Star TV","Star TV (720p)"),("Show TV","ShowTV.tr","https://ciner.daioncdn.net/showtv/showtv.m3u8?app=web"),("NOW","NOW TV (720p)"),("TV8","TV 8 (1080p)"),("Kanal 7","Kanal 7 (720p)"),("Beyaz TV","Beyaz TV (720p) [Not 24/7]"),("Euro D","Euro D (720p)")]),
("Haber",[("A Haber","A Haber (1080p)"),("TRT Haber","TRT Haber (720p)"),("NTV","NTV"),("CNN Türk","CNNTurk.tr","https://live.duhnet.tv/S2/HLS_LIVE/cnnturknp/playlist.m3u8"),("Habertürk","Habertürk TV (720p) [Not 24/7]"),("Haber Global","Haber Global (720p) [Not 24/7]"),("Halk TV","Halk TV (1080p)"),("TGRT Haber","TGRT Haber (720p)"),("Tele 1","Tele 1 (1080p)"),("Bloomberg HT","BloombergHT (720p)"),("Flash Haber","Flash Haber TV"),("TR24","TR24 TV (720p) [Not 24/7]"),("360","360 TV (720p) [Not 24/7]"),("Finans Türk","Finans Turk TV (720p)"),("TürkHaber","TürkHaber (720p)")]),
("Spor",[("A Spor","A Spor (1080p)"),("TRT Spor","TRT Spor (720p)"),("S Sport","S Sport (720p)"),("S Sport 2","S Sport 2 (720p)"),("HT Spor","HTSpor TV (1080p)")]),
("Çocuk",[("TRT Çocuk","TRT Cocuk (1440p)"),("Minika Çocuk","Minika Cocuk (720p)"),("Minika Go","Minika Go (720p)"),("TRT Diyanet Çocuk","TRT Diyanet Çocuk (720p)")]),
("Müzik",[("Kral Pop","KRAL Pop TV (720p)"),("Power TV","Power TV (1080p)"),("Power Türk","PowerTürk TV (720p)"),("Number 1","Number 1 TV (720p)"),("TRT Müzik","TRT Müzik (720p)"),("Power Love","Power Love (1080p)"),("Power Dance","Power Dance (1080p)"),("Power Türk Akustik","Power Türk Akustik (1080p)"),("Power Türk Slow","Power Türk Slow (1080p)"),("Number 1 Aşk","Number 1 Ask (720p)"),("Number 1 Damar","Number 1 Damar (720p)")]),
("Belgesel ve Dini",[("TRT Belgesel","TRT Belgesel (720p)"),("TRT Türk","TRT Türk (720p)"),("TRT Avaz","TRT Avaz (720p)"),("Diyanet TV","Diyanet TV (1080p)"),("Semerkand TV","Semerkand TV (1080p) [Not 24/7]"),("TGRT Belgesel","TGRT Belgesel TV (576p) [Not 24/7]")])]
out=[];used=set();usedn=set();miss=[]
for g,items in G:
    for it in items:
        if len(it)==3: n,lid,u=it; e=dict(id=lid.split('.')[0]+'.tr' if lid.endswith('.tr') else lid)
        else:
            n,t=it; e=E.get(t)
            if not e: miss.append(n); continue
            lid=e['id']; u=e['u']
        out.append(dict(n=n,u=u,l=logos.get(lid if len(it)==3 else e['id'],''),g=g)); used.add(e['id'] if len(it)==2 else lid); usedn.add(n.lower())
BAD=re.compile(r'Geo-blocked|Not 24/7|Al-Zahra|Almahriah|Mekameleen|Arabi|TRT World|EBA|Kurdî|Kurdi|Muzik$',re.I)
best={}
for t,e in E.items():
    if BAD.search(t) or e['id'] in used or not e['id']: continue
    p=re.search(r'\((\d+)p\)',t); p=int(p.group(1)) if p else 0
    if e['id'] not in best or p>best[e['id']][0]: best[e['id']]=(p,e)
rest=sorted(((clean(e['t']),e) for p,e in best.values()),key=lambda x:x[0].lower())
for n,e in rest:
    if n.lower() in usedn: continue
    usedn.add(n.lower()); out.append(dict(n=n,u=e['u'],l=logos.get(e['id'],''),g='Yerel ve Diğer'))
open('channels.js','w',encoding='utf-8').write('const CHANNELS='+json.dumps(out,ensure_ascii=False)+';')
print(len(out),'channels, with logo:',sum(1 for c in out if c['l']),'missing:',miss)
