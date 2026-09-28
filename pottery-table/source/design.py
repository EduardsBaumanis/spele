"""Vienots izmēru avots: centimetri; X garums, Y platums, Z virs grīdas."""
from pathlib import Path
from collections import Counter
import csv, json, math
ROOT=Path(__file__).resolve().parents[1]
DATE='2026-09-28'; REV='D'
PARAMS=dict(units='cm',length=250,width=125,height=78,plywood=5,isolation=.2,
 frame_length=230,frame_width=105,frame_depth=4,shelf_length=150,shelf_width=35,
 shelf_top=26.2,shelf_plywood=3,shelf_deck_length=154,shelf_deck_width=39,shelf_load_kg=200,shelf_module_length=216,
 shelf_module_width=77.4,shelf_module_height=16,foot_allowance=3,saw_kerf=.3,stock_end_trim=1)
CORNERS=[(20,20),(230,20),(20,105),(230,105)]
SLATS=[53,101,149,197]
SHELF_X=[77,125,173]
SHELF_DECK=dict(origin=[48,43,23.2],size=[154,39,3],overhang=2,corner_radius=1)
TOP_X=[40,74,108,142,176,210]
def fmt(v):
    return f'{v:.3f}'.rstrip('0').rstrip('.').replace('.',',') if isinstance(v,(int,float)) else str(v)
CUTS=[
 dict(mark='T01',name='Augšējā rāmja garensija',section='RHS 8×4×0,3',qty=3,length=214,a=8,b=4,wall=.3,code='06CV08004003000'),
 dict(mark='T02',name='Augšējā rāmja gala sija',section='RHS 8×4×0,3',qty=2,length=105,a=8,b=4,wall=.3,code='06CV08004003000'),
 dict(mark='T03',name='Augšējā rāmja šķērssija',section='RHS 6×4×0,3',qty=4,length=40.5,a=6,b=4,wall=.3,code='06CV06004003000'),
 dict(mark='L01',name='Galda kāja',section='SHS 6×6×0,3',qty=4,length=63.4,a=6,b=6,wall=.3,code='06CV06006003000'),
 dict(mark='S01',name='Plaukta garensija; 8 vertikāli',section='RHS 8×4×0,3',qty=2,length=206,a=8,b=4,wall=.3,code='06CV08004003000'),
 dict(mark='S02',name='Plaukta gala šķērssija; 8 vertikāli',section='RHS 8×4×0,3',qty=2,length=75.8,a=8,b=4,wall=.3,code='06CV08004003000'),
 dict(mark='S03',name='Plaukta šķērslīste; 4 vertikāli',section='RHS 6×4×0,3',qty=4,length=27,a=6,b=4,wall=.3,code='06CV06004003000'),
 dict(mark='P01',name='Kājas augšējā plāksne; 4 fiksētas + 4 noņemamas',section='Plakandzelzs 20×0,8',qty=8,length=20,a=20,b=.8,wall=0,code='05PL08020001'),
 dict(mark='P02',name='Kājas apakšējā plāksne',section='Plakandzelzs 6×0,8',qty=4,length=6,a=6,b=.8,wall=0,code='05PL08006000'),
 dict(mark='P03',name='Plaukta savienojuma plāksne; 4 pie kājām + 4 pie S02',section='Plakandzelzs 6×0,8',qty=8,length=16,a=6,b=.8,wall=0,code='05PL08006000'),
 dict(mark='P04',name='Klāju stiprinājuma plāksnīte; 12 virsmai + 6 plauktam',section='Plakandzelzs 4×0,4',qty=18,length=4,a=4,b=.4,wall=0,code='05PL04004000'),
 dict(mark='P05',name='Kājas trīsstūrveida riba; katetes 6 un 6',section='Plāksne 0,6',qty=16,length=6,a=6,b=.6,wall=0,code='',triangle=True),
]
for p in CUTS:
    area=p['a']*p['b']-(p['a']-2*p['wall'])*(p['b']-2*p['wall']) if p['wall'] else p['a']*p['b']
    p['mass_each_kg']=area*p['length']*.00785*(.5 if p.get('triangle') else 1)
HARDWARE=[
 ('H01',24,'M12 skrūve, garums 3,5 cm, klase 8.8','16 kāju augšējiem mezgliem; 8 plaukta savienojumiem. Garums zem galvas.'),
 ('H02',24,'M12 rūdīta paplāksne; nomināli 0,25 cm bieza','16 augšā; 8 pie plaukta. Pārbaudīt faktisko komplektu.'),
 ('H03',24,'M12 pilna augstuma metināms uzgrieznis','16 augšā; 8 kāju sānos. Uzgrieznis ar šuvi ietilpst Ø3 cm atverē.'),
 ('H07',4,'M16 metināms uzgrieznis','Kājas iekšpusē virs P02; izvēlēties pirms metināšanas.'),
 ('H08',4,'M16 regulējams balsts; paliktnis ap Ø8 cm; vismaz 300 kg katram','Paliktnis ne augstāks par 2 cm; kāts vismaz 6 cm; regulējums 2,85–3,19 cm no grīdas līdz P02 apakšai.'),
 ('H09',4,'M16 plāns kontruzgrieznis; nomināli 0,8 cm','Ietilpst starp balsta paliktni un P02; pārbaudīt vītnes saķeri.'),
 ('H10',18,'M6 koka vītņieliktnis, garums 1,8 cm','12 galda virsmai un 6 plaukta klājam; urbuma Ø pēc ražotāja, dziļums līdz 2 cm.'),
 ('H11',18,'M6 skrūve, garums 2 cm','W01 un W05; nomināla saķere 1,24 cm, pārbaudīt faktiskajā ieliktnī.'),
 ('H12',18,'M6 plata paplāksne; ārējais Ø ap 1,8 cm, biezums 0,16 cm','12 galda virsmai un 6 plauktam; pārsedz 0,8 × 1,6 cm spraugu.'),
 ('H13',4,'Plastmasas noslēgs profilam 8×4×0,3 cm','T02 atvērtajiem galiem; uzstādīt pēc krāsošanas.'),
 ('H15',1600,'Blīva EPDM lente; platums 2 cm, biezums 0,2 cm','Daudzums centimetros; abiem klājiem, arī plāksnītēm.'),
 ('W01',1,'Bērza saplāksnis 250×125×5 cm, RIGA PLY BB/WG EXT LN','Kods 0015001250250000061L. Cenu un pieejamību apstiprināt pirms pasūtīšanas.'),
 ('W02',2,'Bērza saplākšņa darba dēlis 60×45×2,1 cm','Atsevišķs materiāls; noapaļot malas, pārklāt ar noņemamu audeklu.'),
 ('W03',2,'Mazgājams, nostiepts audekla pārvalks','Dēlim W02; regulāri izžāvēt un pēc vajadzības nomainīt.'),
 ('W05',1,'Bērza saplākšņa plaukta klājs 154×39×3 cm','2 cm pārkare pār centrālo 150×35 cm balsta zonu; seši M6 stiprinājumi no apakšas.'),
 ('W04',4,'Skavas ar mīkstiem paliktņiem','Atvērums atbilstošs galda virsmai un darba dēlim.'),
]
def hole(x,y,z,d,depth,axis='z',purpose='skrūves caurums'):
    return dict(x=x,y=y,z=z,d=d,depth=depth,axis=axis,purpose=purpose)
def model():
    parts=[]
    def box(mark,inst,x,y,z,dx,dy,dz,group='frame',axis=None,wall=0,holes=None,slots=None):
        p=dict(mark=mark,instance=inst,origin=[x,y,z],size=[dx,dy,dz],group=group,kind='tube' if axis else 'plate',axis=axis,wall=wall,holes=holes or [],slots=slots or [])
        parts.append(p); return p
    rails=[]
    for n,y in enumerate([10,58.5,107],1):
        rails.append(box('T01',f'T01-{n}',18,y,68.8,214,8,4,axis='x',wall=.3,holes=[hole(125,y+4,68.8,.6,.3,purpose='ventilācija')]))
    for n,x in enumerate([10,232],1):rails.append(box('T02',f'T02-{n}',x,10,68.8,8,105,4,axis='y',wall=.3))
    for n,(x,y) in enumerate([(x,y) for x in [62,182] for y in [18,66.5]],1):
        box('T03',f'T03-{n}',x,y,68.8,6,40.5,4,axis='y',wall=.3,holes=[hole(x+3,y+20.25,68.8,.6,.3,purpose='ventilācija')])
    for n,(cx,cy) in enumerate(CORNERS,1):
        positions=[(cx+i,cy+j) for i in [-7,7] for j in [-7,7]]
        for z,label,group in [(68,'F','frame'),(67.2,'L','legs')]:
            box('P01',f'P01-{label}{n}',cx-10,cy-10,z,20,20,.8,group=group,holes=[hole(x,y,z,1.3,.8) for x,y in positions])
        for x,y in positions:
            for p in rails:
                px,py,pz=p['origin'];dx,dy,dz=p['size']
                if px<x<px+dx and py<y<py+dy:p['holes'].append(hole(x,y,68.8,3,.3,purpose='M12 augšējā uzgriežņa atvere'))
        # P03 receives the shelf at the inward-facing wall of each leg.
        entry=22.7 if cy==20 else 102
        leg=box('L01',f'L01-{n}',cx-3,cy-3,3.8,6,6,63.4,group='legs',axis='z',wall=.3,
            holes=[hole(cx,entry,z,3,.3,axis='y',purpose='M12 plaukta uzgriežņa atvere') for z in [12.5,25.5]])
        box('P02',f'P02-{n}',cx-3,cy-3,3,6,6,.8,group='legs',holes=[hole(cx,cy,3,1.8,.8)])
        for side in range(4):parts.append(dict(mark='P05',instance=f'P05-{n}-{side+1}',kind='gusset',group='legs',centre=[cx,cy],side=side,top=67.2,leg=6,thickness=.6))
        for yy,label,group in [(23 if cy==20 else 101.2,'L','legs'),(23.8 if cy==20 else 100.4,'S','shelf')]:
            box('P03',f'P03-{label}{n}',cx-3,yy,11,6,.8,16,group=group,
                holes=[hole(cx,yy,z,1.3,.8,axis='y') for z in [12.5,25.5]])
    for n,y in enumerate([45,76],1):
        box('S01',f'S01-{n}',22,y,15,206,4,8,group='shelf',axis='x',wall=.3,holes=[hole(125,y+2,15,.6,.3,purpose='ventilācija')])
    for n,x in enumerate([18,228],1):
        box('S02',f'S02-{n}',x,24.6,15,4,75.8,8,group='shelf',axis='y',wall=.3,holes=[hole(x+2,62.5,15,.6,.3,purpose='ventilācija')])
    for n,x in enumerate(SLATS,1):
        box('S03',f'S03-{n}',x-3,49,19,6,27,4,group='shelf',axis='y',wall=.3,holes=[hole(x,62.5,19,.6,.3,purpose='ventilācija')])
    for group,xs,ys,z,wood in [('frame',TOP_X,[20,105],72.4,'W01'),('shelf',SHELF_X,[51,74],22.6,'W05')]:
        for n,(x,y) in enumerate([(x,y) for y in ys for x in xs],1):
            box('P04',f'P04-{wood}-{n}',x-2,y-2,z,4,4,.4,group=group,
                slots=[dict(x=x,y=y,z=z,width=.8,length=1.6,depth=.4,wood=wood)])
    return parts
PARTS=model()
def gusset_vertices(p):
    cx,cy=p['centre'];a=p['side']*math.pi/2
    return [[cx+r*math.cos(a)-t*math.sin(a),cy+r*math.sin(a)+t*math.cos(a),z] for t in [-.3,.3] for r,z in [(3,67.2),(9,67.2),(3,61.2)]]
def stock_nesting():
    by={}
    for p in CUTS:
        if p['wall']:by.setdefault(p['section'],[]).extend([(p['mark'],p['length'])]*p['qty'])
    result=[]
    for section,pieces in by.items():
        bars=[]
        for mark,length in sorted(pieces,key=lambda p:-p[1]):
            for b in bars:
                if b['used']+length+.3<=600+1e-9:break
            else:
                b=dict(section=section,bar=len(bars)+1,stock=600,used=2,pieces=[]);bars.append(b)
            b['pieces'].append([mark,length]);b['used']+=length+.3
        result.extend(bars)
    return result

def validate():
    checks=[]
    def ok(c,t):
        if not c:raise AssertionError(t)
        checks.append(t)
    near=lambda a,b:abs(a-b)<1e-7
    counts=Counter(p['mark'] for p in PARTS)
    ok(counts==Counter({p['mark']:p['qty'] for p in CUTS}),'Katra griešanas saraksta detaļa precīzi atbilst vienam modeļa elementam.')
    # Check actual part sizes against purchased sections and cut lengths.
    for p in PARTS:
        cut=next(c for c in CUTS if c['mark']==p['mark'])
        if p['kind']=='tube':
            axis='xyz'.index(p['axis']);cross=[p['size'][i] for i in range(3) if i!=axis]
            ok(near(p['size'][axis],cut['length']) and all(near(a,b) for a,b in zip(sorted(cross),sorted([cut['a'],cut['b']]))),p['instance']+': modeļa garums un profils atbilst sagatavei.')
        elif p['kind']=='plate':
            if not all(near(a,b) for a,b in zip(sorted(p['size']),sorted([cut['length'],cut['a'],cut['b']]))):raise AssertionError(p['instance']+' plāksnes izmēri')
    ok(near(3+.8+63.4+.8+.8+4+.2+5,78),'Neatkarīga augstumu summa: 78 cm.')
    ok(near(15+8+.2+3,26.2),'Plaukts: tērauds līdz 23 cm + EPDM 0,2 cm + klājs 3 cm = 26,2 cm.')
    ok(near(105-3*8,2*40.5) and near(230-2*8,214),'Augšējā rāmja garensijas un šķērssijas precīzi aizpilda ailes.')
    ok(near(102-23-4*.8,75.8),'Plaukta gala šķērssija 75,8 cm + četras plāksnes 0,8 cm aizpilda 79 cm starp kāju iekšējām plaknēm.')
    ok(near(228-22,206) and near(80-45-2*4,27),'Plaukta garensijas 206 cm un šķērslīstes 27 cm precīzi aizpilda ailes.')
    ok(SLATS[0]-3==50 and SLATS[-1]+3==200 and len(SLATS)==4 and all(b-a==48 for a,b in zip(SLATS,SLATS[1:])),'Četras šķērslīstes ar 48 cm soli un 42 cm brīvām spraugām; ārmalas X=50 un 200 cm.')
    boxes=[p for p in PARTS if p['kind']!='gusset'];clashes=[]
    for i,a in enumerate(boxes):
        for b in boxes[i+1:]:
            overlap=[min(a['origin'][j]+a['size'][j],b['origin'][j]+b['size'][j])-max(a['origin'][j],b['origin'][j]) for j in range(3)]
            if min(overlap)>1e-7:clashes.append((a['instance'],b['instance']))
    ok(not clashes,f'{len(boxes)} cauruļu un plākšņu apvalkiem nav savstarpēju tilpuma pārklāšanos: {clashes or "pārbaudīts"}.')
    shelf_boxes=[p for p in boxes if p['group']=='shelf']
    shelf_min=[min(p['origin'][i] for p in shelf_boxes) for i in range(3)]
    shelf_max=[max(p['origin'][i]+p['size'][i] for p in shelf_boxes) for i in range(3)]
    ok(all(near(a,b) for a,b in zip(shelf_min,[17,23.8,11])) and all(near(a,b) for a,b in zip(shelf_max,[233,101.2,27])),
       'Plaukta transporta gabarīts ar P03: 216 × 77,4 × 16 cm; plāksnes iekļautas.')
    for p in boxes:
        for h in p['holes']:
            axis='xyz'.index(h['axis'])
            for k in range(3):
                if k!=axis and not (p['origin'][k]+h['d']/2-1e-7<=h['xyz'[k]]<=p['origin'][k]+p['size'][k]-h['d']/2+1e-7):raise AssertionError('Urbums ārpus '+p['instance'])
    checks.append('Visi apaļie urbumi ietilpst atbilstošajās detaļu plaknēs.')
    for label,count in [('M12 augšējā uzgriežņa atvere',12),('M12 plaukta uzgriežņa atvere',8)]:
        ok(sum(h['purpose']==label for p in PARTS for h in p.get('holes',[]))==count,f'{label}: {count} atveres vienā caurules sienā.')
    for n in range(1,5):
        a=next(p for p in PARTS if p['instance']==f'P03-L{n}')
        b=next(p for p in PARTS if p['instance']==f'P03-S{n}')
        ok(all(near(h1['x'],h2['x']) and near(h1['z'],h2['z']) for h1,h2 in zip(a['holes'],b['holes'])) and near(abs(a['origin'][1]-b['origin'][1]),.8),f'Plaukta savienojums {n}: plāksnes saskaras un abi skrūvju urbumi sakrīt.')
    for b in stock_nesting():ok(b['used']<=600,f"{b['section']}, sagatave {b['bar']}: griezumi ietilpst 600 cm, ieskaitot zāģējumu un gala rezervi.")
    ok(Counter(m for b in stock_nesting() for m,L in b['pieces'])==Counter({p['mark']:p['qty'] for p in CUTS if p['wall']}),'Cauruļu sadalījumā katra sagatave uzskaitīta tieši vienu reizi.')
    ok(near(3.5-(.8+.8+.25),1.65),'M12 skrūvei aiz fiksētās plāksnes paliek 1,65 cm; jāpārbauda īstais uzgrieznis.')
    ok(near(2-(.4+.2+.16),1.24),'M6 skrūves saķere abos saplākšņa klājos: 1,24 cm.')
    ok(counts['P04']==18 and sum(p['mark']=='P04' and p['group']=='shelf' for p in PARTS)==6,'Abu klāju stiprinājumi: 12 augšējās un 6 plaukta plāksnītes.')
    ok(all(min(abs(x-c) for c in SLATS)>5 for x in SHELF_X),'Plaukta stiprinājuma plāksnītes nekrustojas ar šķērslīstēm.')
    ox,oy,oz=SHELF_DECK['origin'];sx,sy,sz=SHELF_DECK['size']
    ok(near(50-ox,2) and near(ox+sx-200,2) and near(45-oy,2) and near(oy+sy-80,2),'Klājam 154 × 39 cm ir 2 cm pārkare pār 150 × 35 cm centrālo balsta zonu.')
    ok(near(oz+sz,PARAMS['shelf_top']),'Plaukta klāja modeļa augša atbilst norādītajam augstumam 26,2 cm.')
    ok(near(8-5.15,2.85) and near(8-4.81,3.19),'Virsmas biezuma pielaidei balsta regulējums nepieciešams 2,85–3,19 cm.')
    return checks

def write_csv(path,fields,rows):
    with open(path,'w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter=';');w.writeheader()
        for row in rows:w.writerow({k:fmt(v) for k,v in row.items()})
def export_data():
    for d in ['model','drawings']:(ROOT/d).mkdir(exist_ok=True)
    fields=['pozīcija','detaļa','profils_cm','skaits','gatavais_garums_cm','platums_cm','biezums_vai_augstums_cm','piegādātāja_kods','norāde','kopējā_teorētiskā_masa_kg']
    rows=[]
    for p in CUTS:
        rows.append(dict(zip(fields,[p['mark'],p['name'],p['section'],p['qty'],p['length'],p['a'],p['b'],p['code'],'Gatavs taisnleņķa trīsstūris; katetes 6 un 6 cm' if p.get('triangle') else 'Taisni gali; garuma pielaide ±0,1 cm; noņemt atskabargas',round(p['qty']*p['mass_each_kg'],3)])))
    write_csv(ROOT/'cutting-list.csv',fields,rows)
    fields=['pozīcija','daudzums','apraksts','piezīme'];write_csv(ROOT/'hardware-list.csv',fields,[dict(zip(fields,r)) for r in HARDWARE])
    fields=['profils_cm','sagataves_numurs','sagataves_garums_cm','gatavās_detaļas_cm','zāģējums_katrai_detaļai_cm','kopējā_galu_rezerve_cm','atlikums_cm']
    write_csv(ROOT/'stock-cutting.csv',fields,[dict(zip(fields,[b['section'],b['bar'],600,' | '.join(f'{m}: {fmt(L)}' for m,L in b['pieces']),.3,2,600-b['used']])) for b in stock_nesting()])
    fields=['detaļas_numurs','urbums','X_cm','Y_cm','Z_cm','ass','diametrs_cm','dziļums_cm','piezīme'];rows=[]
    for p in PARTS:
        for h in p.get('holes',[]):rows.append(dict(zip(fields,[p['instance'],h['purpose'],h['x'],h['y'],h['z'],h['axis'],h['d'],h['depth'],'Tikai viena caurules siena; virziens pa pozitīvo asi' if p['kind']=='tube' else 'Cauri plāksnei; virziens pa pozitīvo asi'])))
        for h in p.get('slots',[]):
            rows.append(dict(zip(fields,[p['instance'],'Ovāls 0,8 × 1,6 cm; garenass X',h['x'],h['y'],h['z'],'z',.8,.4,'Galu loku centru attālums 0,8 cm'])))
            rows.append(dict(zip(fields,[h['wood'],'M6 ieliktņa urbums',h['x'],h['y'],73 if h['wood']=='W01' else 23.2,'z','Pēc ieliktņa ražotāja','Līdz 2','Urbums no apakšas; caur virsmu neurbt'])))
    write_csv(ROOT/'drilling-coordinates.csv',fields,rows)
    (ROOT/'model'/'design.json').write_text(json.dumps(dict(units='cm',revision=REV,date=DATE,parameters=PARAMS,shelf_deck=SHELF_DECK,parts=PARTS),indent=2),encoding='utf-8')
    return validate()
if __name__=='__main__':print('\n'.join(export_data()))
