"""Dimensioned A3 SVG sheets, generated from the same geometry as the CAD model."""
import math
from html import escape
from design import ROOT, PARTS, DATE, REV, gusset_vertices, fmt, CORNERS, SLATS, TOP_HOLES

INK='#243441'; RED='#b83b31'; LIGHT='#f7e6e1'; GREY='#77858e'; GOLD='#aa854c'; WOOD='#ead7b3'

def num(v): return f'{v:.3f}'.rstrip('0').rstrip('.') if isinstance(v,(float,int)) else str(v)

class Sheet:
    def __init__(self,number,title,subtitle):
        self.number=number
        self.lines=['<svg xmlns="http://www.w3.org/2000/svg" width="42cm" height="29.7cm" viewBox="0 0 420 297">',
                    '<rect width="420" height="297" fill="white"/>']
        self.text(14,16,'DARBNĪCA / KERAMIKAS GALDS',3.1,GREY,bold=True)
        self.text(14,26,title,6.2,bold=True)
        self.text(14,34,subtitle,2.7,GREY)
        self.line(14,39,406,39,.45,INK)
        self.line(14,278,406,278,.4,INK)
        self.text(14,284,f'PT-250  /  {number}  /  RED. {REV}  /  {DATE}',2.6,bold=True)
        self.text(14,290,'Visi izmēri cm · Nomināla ģeometrija pirms krāsošanas · Izmantot norādītos izmērus',2.5,GREY)
        self.text(406,284,'A3 · 42 × 29,7 cm',2.6,align='end')
        self.line(356,287,406,287,.5)
        for x in [356,366,376,386,396,406]:self.line(x,286,x,288,.3)
        self.text(381,291,'Izdrukas pārbaude: 5 cm',2.1,GREY,align='middle')
    def line(self,x1,y1,x2,y2,w=.22,c=INK,dash=None):
        d=f' stroke-dasharray="{dash}"' if dash else ''
        self.lines.append(f'<line x1="{num(x1)}" y1="{num(y1)}" x2="{num(x2)}" y2="{num(y2)}" stroke="{c}" stroke-width="{w}"{d}/>')
    def rect(self,x,y,w,h,fill='none',stroke=INK,sw=.25,dash=None,rx=0):
        self.lines.append(f'<rect x="{num(x)}" y="{num(y)}" width="{num(w)}" height="{num(h)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" rx="{rx}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
    def poly(self,points,fill='none',stroke=INK,sw=.2):
        self.lines.append('<polygon points="'+' '.join(f'{num(x)},{num(y)}' for x,y in points)+f'" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
    def circle(self,x,y,r,fill='white',stroke=INK,sw=.22):
        self.lines.append(f'<circle cx="{num(x)}" cy="{num(y)}" r="{num(r)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
    def text(self,x,y,t,size=3,c=INK,bold=False,align='start',rotate=0):
        self.lines.append(f'<text x="{num(x)}" y="{num(y)}" font-family="DejaVu Sans" font-size="{size}" fill="{c}" text-anchor="{align}"'+(' font-weight="bold"' if bold else '')+(f' transform="rotate({rotate} {num(x)} {num(y)})"' if rotate else '')+'>'+escape(str(t))+'</text>')
    def note(self,x,y,lines,size=3,step=5):
        for n,t in enumerate(lines):self.text(x,y+n*step,t,size)
    def dimh(self,x1,x2,y,anchor,label):
        for x in [x1,x2]:self.line(x,anchor,x,y+2,.18,GREY)
        self.line(x1,y,x2,y,.18,GREY)
        self.poly([(x1,y),(x1+1.6,y-.55),(x1+1.6,y+.55)],GREY,GREY,.1)
        self.poly([(x2,y),(x2-1.6,y-.55),(x2-1.6,y+.55)],GREY,GREY,.1)
        self.text((x1+x2)/2,y-1.5,label,3,align='middle')
    def dimv(self,y1,y2,x,anchor,label):
        for y in [y1,y2]:self.line(anchor,y,x+2,y,.18,GREY)
        self.line(x,y1,x,y2,.18,GREY)
        self.poly([(x,y1),(x-.55,y1+1.6),(x+.55,y1+1.6)],GREY,GREY,.1)
        self.poly([(x,y2),(x-.55,y2-1.6),(x+.55,y2-1.6)],GREY,GREY,.1)
        self.text(x-1.5,(y1+y2)/2,label,3,align='middle',rotate=-90)
    def leader(self,points,label,x,y):
        for a,b in zip(points,points[1:]):self.line(*a,*b,.2,GREY)
        self.circle(*points[0],.5,GREY,GREY,.1);self.text(x,y,label,2.8)
    def save(self):
        path=ROOT/'drawings'/f'{self.number}.svg'
        path.write_text('\n'.join(self.lines+['</svg>']),encoding='utf-8')
        return path

def box_faces(p):
    if p['kind']=='gusset':
        v=gusset_vertices(p); ids=[[0,1,2],[3,5,4],[0,3,4,1],[1,4,5,2],[2,5,3,0]]
    else:
        x,y,z=p['origin'];a,b,c=p['size']
        v=[[x,y,z],[x+a,y,z],[x+a,y+b,z],[x,y+b,z],[x,y,z+c],[x+a,y,z+c],[x+a,y+b,z+c],[x,y+b,z+c]]
        ids=[[0,3,2,1],[4,5,6,7],[0,1,5,4],[1,2,6,5],[2,3,7,6],[3,0,4,7]]
    return [[v[i] for i in face] for face in ids]

def iso(s,parts,bounds,wood=True):
    allp=list(parts)
    if wood:allp.append(dict(kind='plate',origin=[0,0,73],size=[250,125,5],group='wood'))
    for cx,cy in CORNERS:
        allp.append(dict(kind='plate',origin=[cx-4,cy-4,0],size=[8,8,2],group='foot'))
    def proj(v):
        x,y,z=v; return (.8*x+.6*y,.3*x-.4*y-.8*z)
    faces=[]
    for p in allp:
        for face in box_faces(p):
            depth=sum(.48*x-.64*y+.6*z for x,y,z in face)/len(face)
            faces.append((depth,[proj(v) for v in face],p['group']))
    xs=[v[0] for _,f,_ in faces for v in f];ys=[v[1] for _,f,_ in faces for v in f]
    bx,by,bw,bh=bounds;scale=min(bw/(max(xs)-min(xs)),bh/(max(ys)-min(ys)))
    ox=bx+(bw-(max(xs)-min(xs))*scale)/2-min(xs)*scale
    oy=by+(bh-(max(ys)-min(ys))*scale)/2-min(ys)*scale
    # Draw each deck after its supports so large deck faces cover the shorter slats.
    layer={'shelf':0,'legs':2,'foot':2,'wood':4,'top_hardware':5}
    for n,(depth,f,g) in enumerate(sorted(faces,key=lambda f:(layer[f[2]],f[0]))):
        c=WOOD if g in ['wood'] else '#58616a' if g=='foot' else ['#c94b3c','#b93c32','#d45946'][n%3]
        s.poly([(ox+x*scale,oy+y*scale) for x,y in f],c,'#704337' if g=='wood' else '#81372f',.16)

def general():
    s=Sheet('S01','Kopskats un galvenie izmēri','Uz kājām balstīts māla plaukts · Savienojumi un detaļas: S02–S07')
    iso(s,PARTS,(18,48,275,185))
    s.text(301,56,'KONSTRUKCIJA',3.4,bold=True)
    s.note(301,66,['Virsma: 250 × 125 × 5','Galda augstums: 78','Bērza saplāksnis; BB uz augšu','Tērauds: satīna RAL 3020','','8 vietas; reizēm 10','Viengabala metināta pamatne','Plaukts piemetināts kājām','','Plaukta slodzes mērķis: 200 kg'],2.8,6)
    s.text(301,143,'PĀRVADĀŠANA',3.4,bold=True)
    s.note(301,153,['Virsma: 250 × 125','Pamatne: 230 × 105 × 73','Virsma noņemama','Režģa zona: 150 × 35','','Pārbaudīt durvju aili.','Pamatne neizjaucas.'],2.75,5.5)
    s.line(14,240,406,240,.25,GREY)
    s.note(18,249,['DARBA VIETA','Pa trim sēdvietām gar sāniem,','pa vienai katrā galā.'],2.9,5.6)
    s.note(150,249,['VIETA KĀJĀM','Režģis 45 no sāniem, 50 no galiem.','Gala šķērssijas Z=15–23.'],2.9,5.6)
    s.note(287,249,['SLODZE','Maisi → metāla režģis → kājas.','200 kg ir projektēšanas mērķis.'],2.9,5.6)
    return s.save()

def supports():
    s=Sheet('S02','Tiešie virsmas balsti — plāns','Mērogs 1:10 uz A3 · Četras atsevišķas kāju plāksnes · Bez augšējā rāmja')
    ox,oy=45,62
    s.rect(ox,oy,250,125,'none',GOLD,.25,'2 1',rx=2.5)
    for p in PARTS:
        if p['mark']!='P01':continue
        x,y,z=p['origin'];a,b,c=p['size']
        s.rect(ox+x,oy+y,a,b,LIGHT,RED,.25)
        for h in p['holes']:s.circle(ox+h['x'],oy+h['y'],.45,'white',INK,.15)
    for x,y in CORNERS:s.rect(ox+x-3,oy+y-3,6,6,'none',INK,.2,'1 .6')
    for p in PARTS:
        if p['kind']=='gusset':s.poly([(ox+v[0],oy+v[1]) for v in gusset_vertices(p)],RED,RED,.2)
    s.text(ox+125,oy+57,'5 cm bērza saplāksnis nes virsmas slodzi.',3.2,align='middle')
    s.text(ox+125,oy+66,'Kājas un plaukts sametināti vienā pamatnē.',3,align='middle')
    s.dimh(ox,ox+250,49,oy,'250 — virsma');s.dimv(oy,oy+125,25,ox,'125 — virsma')
    s.dimh(ox+20,ox+230,203,187,'210 — kāju centri');s.dimv(oy+20,oy+105,309,295,'85 — kāju centri')
    s.dimh(ox+30,ox+220,216,187,'190 — starp P01 iekšmalām')
    s.circle(ox,oy,1);s.text(ox-3,oy-3,'0;0',2.7,align='end')
    s.note(328,63,['P01: 4 GAB.','20 × 20 × 0,8','X: 10–30; 220–240','Y: 10–30; 95–115','','Kāju centri:','X=20 un 230','Y=20 un 105','','4 kokskrūves katrā P01.','Urbumu kvadrāts 14 × 14.','Plāksnes augša Z=73.','','Bez mīkstas starplikas.','Kāju galvas: S04.'],2.65,5.3)
    s.note(18,239,['Kāju centru diagonāle: 226,55; diagonāļu starpība ≤0,2. Plāksnēm cieši jābalsta virsma.',
        'Visām P01 cieši jābalsta virsma; spraugas koriģēt ar cietām pilnas saskares starplikām.',
        'Nav perimetra siju vai centrālo šķērssiju. Plaukts savieno visas četras kājas zemāk.',
        'Pārbaudīt tukšu galdu: stingri spiežot abos virzienos, nav šūpošanās, klikšķu vai slīdēšanas.'],2.8,6)
    return s.save()

def elevations():
    s=Sheet('S03','Sānskati un augstumu ķēde','Mērogs 1:10 uz A3 · Tieši balstīta 5 cm virsma · Bez mīksta starpslāņa')
    for end,ox in [(False,18),(True,279)]:
        base=151;span=125 if end else 250
        s.text(ox,54,'SKATS NO GALA' if end else 'SKATS NO GARĀS MALAS',3.1,bold=True)
        s.line(ox-2,base,ox+span+2,base,.25,GREY)
        for p in sorted(PARTS,key=lambda p:0 if p['group']=='shelf' else 1):
            if p['kind']=='gusset':
                s.poly([(ox+v[1 if end else 0],base-v[2]) for v in gusset_vertices(p)[:3]],LIGHT,RED,.15);continue
            x,y,z=p['origin'];a,b,c=p['size'];s.rect(ox+(y if end else x),base-z-c,b if end else a,c,LIGHT,RED,.18)
        s.rect(ox,base-78,span,5,WOOD,GOLD,.3)
        for u in ([20,105] if end else [20,230]):
            s.rect(ox+u-4,base-2,8,2,'#52616a',INK,.2,rx=.5);s.rect(ox+u-.8,base-3,1.6,1,'#a2a9ae',INK,.1)
        s.dimh(ox,ox+span,164,base,fmt(span))
    s.dimv(73,151,271,268,'78');s.dimh(68,218,177,126,'150 — režģis')
    s.dimh(324,359,140,132,'35 — režģis')
    s.text(20,192,'AUGSTUMI NO GRĪDAS',3.3,bold=True)
    s.note(20,203,['78 — gluda darba virsma bez caurejošiem urbumiem','73 — virsmas apakša un P01 augša','72,2 — P01 apakša un L01 augša','66,2 — mazo ribu P05 apakšpunkts','L01 garums 68,4; P01 biezums 0,8','3,8 — kājas caurules apakša','3 — P02 apakša; 0 — grīda','3 + 0,8 + 68,4 + 0,8 + 5 = 78'],2.85,7)
    s.text(211,192,'PLAUKTS UN REGULĒŠANA',3.3,bold=True)
    s.note(211,203,['23 — plaukta metāla balsta virsma.','23 — plaukta tērauda augša; 15 — siju apakša.',
        'Gala šķērssijas atrodas pie X=20 un 230.','Pirms griešanas pārbaudīt krēslus un vietu pēdām.','',
        'Balsta augstums = 8 − faktiskais virsmas biezums t.','Pie t=4,81–5,15: balsts 3,19–2,85.',
        'Tērauda augstumi mainās par 5 − t; skatīt aprakstu.'],2.75,7)
    return s.save()

def leg_details():
    s=Sheet('S04','Vienkāršas kāju plāksnes un pēdas','P01 mērogā 1:2 · Divas nelielas ribas katrai kājai · Kokskrūves no apakšas')
    x,y,k=31,72,5
    s.rect(x,y,100,100,LIGHT,RED,.4);s.rect(x+35,y+35,30,30,'none',INK,.3)
    for a in [3,17]:
        for b in [3,17]:s.circle(x+a*k,y+b*k,.45*k)
    s.line(x+65,y+50,x+95,y+50,3,RED);s.line(x+50,y+65,x+50,y+95,3,RED)
    s.dimh(x,x+100,60,y,'20');s.dimh(x+15,x+85,188,172,'14 — caurumu centru attālums');s.dimv(y,y+100,20,x,'20')
    s.note(31,207,['P01: 4 gab.; 20 × 20 × 0,8.','4 parasti urbumi Ø0,9.','Centri 3 no malām; kāja centrā.','Parādīts stūris X=20; Y=20.','Ribas vērstas uz galda vidu.','Pārējiem stūriem spoguļot.'],2.9,7)
    s.text(185,58,'DIVAS RIBAS, TAISNI CAURUĻU GALI',3.3,bold=True)
    ox,base=198,161
    s.rect(ox,base-25,100,25,WOOD,GOLD,.3);s.rect(ox,base,100,4,LIGHT,RED,.3)
    s.rect(ox+35,base+4,30,65,LIGHT,RED,.3)
    s.poly([(ox+65,base+4),(ox+95,base+4),(ox+65,base+34)],LIGHT,RED,.3)
    s.note(185,70,['L01: 6 × 6 × 0,3; garums 68,4.','P05: 8 gab.; katetes 6 × 6; biezums 0,6.','No 6 × 6 kvadrāta iegūst divus trīsstūrus;','ņem vērā zāģējumu vai pasūta gatavus.','Pa vienai ribai X un Y virzienā.','Ribas šuves pie kājas un plāksnes abās pusēs.'],2.8,6)
    s.note(185,245,['P02: 6 × 6 × 0,8; Ø1,8 centrā; M16 uzgrieznis augšpusē.','Uzgriezni piemetina pie atsevišķas P02, tad P02 pie kājas.','4 regulējamas gumijotas pēdas; fiksēt ar kontruzgriežņiem.'],2.75,6)
    return s.save()


def shelf():
    s=Sheet('S05','Plaukta metāla rāmis','Plāns un sānskats mērogā 1:10 uz A3 · Plaukts piemetināts tieši kājām; viena tērauda pamatne')
    ox,oy=35,52
    for p in PARTS:
        if p['group']!='shelf':continue
        x,y,z=p['origin'];a,b,c=p['size'];s.rect(ox+x,oy+y,a,b,LIGHT,RED,.23)
    for cx,cy in CORNERS:s.rect(ox+cx-3,oy+cy-3,6,6,'none',INK,.2,'1 .6')
    s.rect(ox+50,oy+45,150,35,'none',GOLD,.6,'2 1')
    for x in SLATS:s.text(ox+x,oy+64,fmt(x),2.35,align='middle',rotate=-90)
    s.dimh(ox+18,ox+232,64,oy+23,'214 — plaukta cauruļu ārmalas')
    s.dimh(ox+50,ox+200,143,oy+80,'150 — režģis');s.dimh(ox+22,ox+228,165,oy+100.4,'206 — S01 gatavais garums')
    s.dimv(oy+45,oy+80,289,267,'35');s.dimv(oy+23,oy+102,306,267,'79 — S02')
    s.note(326,58,['KOORDINĀTAS','Režģis X: 50–200','Režģis Y: 45–80','','S01 Y: 45–49','un 76–80','S01 X: 22–228','','S02 X: 18–22','un 228–232','S02 Y: 23–102','','S03: 13 gab., garums 27.','Centri X=53,65,…,197.','Solis 12; sprauga 6.'],2.55,5.3)
    base=220
    for p in PARTS:
        if p['group']!='shelf':continue
        x,y,z=p['origin'];a,b,c=p['size'];s.rect(ox+x,base-z-c,a,c,LIGHT,RED,.2)
    s.line(ox+10,base,ox+240,base,.2,GREY);s.dimv(base-23,base,287,267,'23 — nomināli')
    s.text(65,230,'Sānskats ar aizsegtajām detaļām; maisus balsta metāls.',2.8)
    s.note(18,246,['S01 un S02: profils 8 × 4 × 0,3 ar 8 vertikāli. S03: profils 6 × 4 × 0,3 ar 4 vertikāli.',
        'Siju augša Z=23; S01/S02 apakša Z=15; S03 apakša Z=19. Saplākšņa klāja nav.',
        'S02 garums 79; galus metina tieši pie kāju iekšējām sienām. Darbu secība: S07.',
        'Līdz 200 kg vienmērīgi izvietotu maisu; neuzskatīt par sertificētu nestspēju.'],2.75,6)
    return s.save()

def top_fixings():
    s=Sheet('S06','Virsma pieskrūvēta no apakšas','Plāns 1:10, skats caur virsmu · Augšpuse paliek gluda · Frēzēšana nav vajadzīga')
    ox,oy=32,62;s.rect(ox,oy,250,125,'#fcf6eb',GOLD,.35,rx=2.5)
    for cx,cy in CORNERS:s.rect(ox+cx-10,oy+cy-10,20,20,'none',RED,.2,'1 .7')
    for x,y in TOP_HOLES:s.circle(ox+x,oy+y,.45,'none',RED,.2)
    for x in [13,27,223,237]:s.text(ox+x,oy-4,fmt(x),2.5,align='middle')
    s.dimh(ox,ox+250,50,oy,'250');s.dimv(oy,oy+125,19,ox,'125')
    s.text(157,116,'W01 · biezums 5 · BB uz augšu',3,align='middle')
    s.text(157,126,'Augšpusē nav skrūvju vai metāla ielaidumu.',2.8,align='middle')
    s.note(302,57,['16 KOKSKRŪVES','Ø0,8 × 4, ar seškanšu galvu.','Garums 4 zem galvas.','Katrai parasta paplāksne.','','Caurums P01: Ø0,9.','Kokā priekšurbums no apakšas;','Ø pēc skrūves ražotāja.','Dziļums līdz 3,2.','','X=13; 27; 223; 237','Y=13; 27; 98; 112','Visas X un Y kombinācijas.'],2.65,5.6)
    x,y=32,211
    s.rect(x,y,88,30,WOOD,GOLD,.3);s.rect(x,y+30,88,4.8,LIGHT,RED,.3)
    s.rect(x+38,y+34.8,12,1.2,'#65727a',INK,.2)
    s.poly([(x+44,y+12),(x+46.4,y+16),(x+46.4,y+36),(x+41.6,y+36),(x+41.6,y+16)],'#88949c',INK,.2)
    s.rect(x+40,y+36,8,4,'#65727a',INK,.2)
    s.text(x,y+53,'Šķērsgriezums 1:1,67',2.7)
    s.note(137,207,['4 cm skrūve − 0,8 P01 − 0,2 paplāksne = 3 cm kokā.',
        'Virs skrūves paliek ap 2 cm saplākšņa. Neurbt cauri!',
        'Urbja dziļuma ierobežotājs; pirms montāžas izmēģināt atgriezumā.',
        'Pārnest caurumus pēc pamatnes uzlikšanas uz apgrieztās virsmas.',
        'Pievilkt cieši ar rokas atslēgu, neizplēšot vītni kokā.',
        'Virsmas svaru nes plāksnes; skrūves to notur vietā.',
        'Smago galdu celt aiz tērauda pamatnes, nevis saplākšņa malas.'],2.75,7)
    return s.save()


def shelf_joint():
    s=Sheet('S07','Viengabala pamatnes montāža','Taisni profilu gali · Gala sijas metina tieši pie kājām · Nav plaukta skrūvju vai slēptu uzgriežņu')
    ox,base,k=20,227,1.7
    for cy in [20,105]:s.rect(ox+(cy-3)*k,base-72.2*k,6*k,68.4*k,LIGHT,RED,.3)
    s.rect(ox+23*k,base-23*k,79*k,8*k,LIGHT,RED,.3)
    for cy in [20,105]:s.rect(ox+(cy-10)*k,base-73*k,20*k,.8*k,LIGHT,RED,.3)
    for cy in [23,102]:s.line(ox+cy*k,base-23*k,ox+cy*k,base-15*k,.8,RED)
    s.dimh(ox+23*k,ox+102*k,249,base-15*k,'79 — S02 starp kājām')
    s.text(ox+62.5*k,base-19*k,'S02 · 8 vertikāli',2.8,align='middle')
    s.note(229,57,['1. IZVEIDOT DIVUS VIENĀDUS GALUS','Pa divām kājām un vienai S02 sijai.','S02 apakša 11,2 virs kājas caurules apakšgala.','Ar pēdām tas ir Z=15; sijas augša Z=23.','Izmantot vienādus atgriezumus kā starplikas.','','2. SAVIENOT GALUS AR GARSIJĀM','Divas S01, garums 206; 8 vertikāli.','Sijas X=22–228; Y=45–49 un 76–80.','Pagaidām tikai pieķert; pārbaudīt taisnleņķus.','','3. IEVIETOT 13 ŠĶĒRSLĪSTES','Garums 27; 4 vertikāli; augša vienā līmenī.','6 cm atgriezums kalpo kā spraugas šablons.','','4. PĀRBAUDĪT UN SAMETINĀT','Kāju centru diagonāles 226,55; starpība ≤0,2.','P01 plāksnes vienā plaknē uz līdzenas pamatnes.','Metināt pārmaiņus pretējās pusēs.','S02 galus sametināt ar kājām pa perimetru.','Pieķeršanas punkti nav gatavs savienojums.'],2.8,7)
    s.note(23,61,['SKATS NO GALA · 1:5,88','Vienādi gala mezgli pie X=20 un 230.','Abu cauruļu sienas 0,3; piegulošus galus','piegriezt pēc faktiskās ailes.'],2.8,6)
    s.note(229,218,['PIRMS KRĀSOŠANAS','Apskatīt šuves; pārbaudīt pamatni uz grīdas.','Šaubīgas šuves parādīt pieredzējušam metinātājam.','Pamatne ir viena detaļa: 230 × 105 plānā.','Durvju aili un pārvietošanas ceļu pārbaudīt iepriekš.'],2.8,7)
    return s.save()


def build_drawings():return [general(),supports(),elevations(),leg_details(),shelf(),top_fixings(),shelf_joint()]
