"""Vienots izmēru avots: centimetri; X garums, Y platums, Z virs grīdas."""
from pathlib import Path
from collections import Counter
import csv, json, math
ROOT=Path(__file__).resolve().parents[1]
DATE='2026-10-01'; REV='F'
PARAMS=dict(units='cm',length=200,width=100,height=78,plywood=5,isolation=0,
 upper_frame=False,head_plate=20,head_thickness=.8,gusset_leg=6,leg_length=68.4,
 welded_base=True,top_screw_length=4,top_screw_diameter=.8,shelf_length=150,shelf_width=35,
 shelf_top=23,shelf_plywood=0,shelf_load_kg=200,base_height=73,foot_allowance=3,saw_kerf=.3,stock_end_trim=1)
PARAMS.update(base_length=PARAMS['length']-20,base_width=PARAMS['width']-20)
LEG_SPAN_X=PARAMS['length']-40; LEG_SPAN_Y=PARAMS['width']-40
CORNERS=[(x,y) for y in [20,PARAMS['width']-20] for x in [20,PARAMS['length']-20]]
SHELF_X=(PARAMS['length']-PARAMS['shelf_length'])/2
SHELF_Y=(PARAMS['width']-PARAMS['shelf_width'])/2
SLATS=[SHELF_X+3+12*n for n in range(13)]
TOP_HOLES=[(cx+dx,cy+dy) for cx,cy in CORNERS for dx in [-7,7] for dy in [-7,7]]
def fmt(v):
    return f'{v:.3f}'.rstrip('0').rstrip('.').replace('.',',') if isinstance(v,(int,float)) else str(v)
CUTS=[
 dict(mark='L01',name='Galda kāja',section='SHS 6×6×0,3',qty=4,length=68.4,a=6,b=6,wall=.3,code='06CV06006003000'),
 dict(mark='S01',name='Plaukta garensija; 8 vertikāli',section='RHS 8×4×0,3',qty=2,length=LEG_SPAN_X-4,a=8,b=4,wall=.3,code='06CV08004003000'),
 dict(mark='S02',name='Plaukta gala šķērssija; 8 vertikāli',section='RHS 8×4×0,3',qty=2,length=LEG_SPAN_Y-6,a=8,b=4,wall=.3,code='06CV08004003000'),
 dict(mark='S03',name='Plaukta šķērslīste; 4 vertikāli',section='RHS 6×4×0,3',qty=13,length=27,a=6,b=4,wall=.3,code='06CV06004003000'),
 dict(mark='P01',name='Kājas balsta plāksne tieši zem saplākšņa',section='Plāksne 0,8',qty=4,length=20,a=20,b=.8,wall=0,code=''),
 dict(mark='P02',name='Kājas apakšējā plāksne',section='Plakandzelzs 6×0,8',qty=4,length=6,a=6,b=.8,wall=0,code='05PL08006000'),
 dict(mark='P05',name='Kājas stingrības riba; katetes 6 un 6',section='Plāksne 0,6',qty=8,length=6,a=6,b=.6,wall=0,code='',triangle=True),
]
for p in CUTS:
    area=p['a']*p['b']-(p['a']-2*p['wall'])*(p['b']-2*p['wall']) if p['wall'] else p['a']*p['b']
    p['mass_each_kg']=area*p['length']*.00785*(.5 if p.get('triangle') else 1)
HARDWARE=[
 ('H07',4,'M16 metināms uzgrieznis','Kājas iekšpusē virs P02; izvēlēties pirms metināšanas.'),
 ('H08',4,'M16 regulējams balsts; paliktnis ap Ø8 cm; vismaz 300 kg katram','Paliktnis ne augstāks par 2 cm; kāts vismaz 6 cm; regulējums 2,85–3,19 cm no grīdas līdz P02 apakšai.'),
 ('H09',4,'M16 plāns kontruzgrieznis; nomināli 0,8 cm','Ietilpst starp balsta paliktni un P02; pārbaudīt vītnes saķeri.'),
 ('H10',16,'Koka seškanšu skrūve Ø0,8 × 4 cm; garums zem galvas','Kvalitatīva kokskrūve ar rupju vītni; priekšurbums no apakšas pēc ražotāja norādes. Ne ģipškartona skrūve.'),
 ('H12',16,'Paplāksne skrūvei Ø0,8; ārējais Ø ap 2; biezums ap 0,2 cm','Zem P01; nomināli 3 cm skrūves ieiet saplāksnī, ap 2 cm līdz virspusei.'),
 ('W01',1,f"Bērza saplāksnis {PARAMS['length']}×{PARAMS['width']}×5 cm, RIGA PLY BB/WG EXT LN",'Gatavā virsma izgriežama no 250×125×5 cm loksnes; loksnes kods 0015001250250000061L. Cenu un pieejamību apstiprināt pirms pasūtīšanas.'),
 ('W02',2,'Bērza saplākšņa darba dēlis 60×45×2,1 cm','Atsevišķs materiāls; noapaļot malas, pārklāt ar noņemamu audeklu.'),
 ('W03',2,'Mazgājams, nostiepts audekla pārvalks','Dēlim W02; regulāri izžāvēt un pēc vajadzības nomainīt.'),
 ('W04',4,'Skavas ar mīkstiem paliktņiem','Atvērums atbilstošs galda virsmai un darba dēlim.'),
]
def hole(x,y,z,d,depth,axis='z',purpose='skrūves caurums'):
    return dict(x=x,y=y,z=z,d=d,depth=depth,axis=axis,purpose=purpose)
def model():
    parts=[]
    def box(mark,inst,x,y,z,dx,dy,dz,group='legs',axis=None,wall=0,holes=None,slots=None):
        p=dict(mark=mark,instance=inst,origin=[x,y,z],size=[dx,dy,dz],group=group,kind='tube' if axis else 'plate',axis=axis,wall=wall,holes=holes or [],slots=slots or [])
        parts.append(p); return p
    for n,(cx,cy) in enumerate(CORNERS,1):
        positions=[(cx+i,cy+j) for i in [-7,7] for j in [-7,7]]
        box('P01',f'P01-{n}',cx-10,cy-10,72.2,20,20,.8,
            holes=[hole(x,y,72.2,.9,.8,purpose='Kokskrūves caurums') for x,y in positions])
        box('L01',f'L01-{n}',cx-3,cy-3,3.8,6,6,68.4,group='legs',axis='z',wall=.3)
        box('P02',f'P02-{n}',cx-3,cy-3,3,6,6,.8,group='legs',holes=[hole(cx,cy,3,1.8,.8)])
        for side in [0 if cx==20 else 2,1 if cy==20 else 3]:
            parts.append(dict(mark='P05',instance=f'P05-{n}-{side+1}',kind='gusset',group='legs',centre=[cx,cy],side=side,top=72.2,leg=6,thickness=.6))
    for n,y in enumerate([SHELF_Y,SHELF_Y+PARAMS['shelf_width']-4],1):
        box('S01',f'S01-{n}',22,y,15,LEG_SPAN_X-4,4,8,group='shelf',axis='x',wall=.3,holes=[hole(PARAMS['length']/2,y+2,15,.6,.3,purpose='ventilācija')])
    for n,x in enumerate([18,PARAMS['length']-22],1):
        box('S02',f'S02-{n}',x,23,15,4,LEG_SPAN_Y-6,8,group='shelf',axis='y',wall=.3,holes=[hole(x+2,PARAMS['width']/2,15,.6,.3,purpose='ventilācija')])
    for n,x in enumerate(SLATS,1):
        box('S03',f'S03-{n}',x-3,SHELF_Y+4,19,6,27,4,group='shelf',axis='y',wall=.3,holes=[hole(x,PARAMS['width']/2,19,.6,.3,purpose='ventilācija')])
    return parts
PARTS=model()
def gusset_vertices(p):
    cx,cy=p['centre'];a=p['side']*math.pi/2
    return [[cx+r*math.cos(a)-t*math.sin(a),cy+r*math.sin(a)+t*math.cos(a),z] for t in [-p['thickness']/2,p['thickness']/2] for r,z in [(3,p['top']),(3+p['leg'],p['top']),(3,p['top']-p['leg'])]]
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
    ok(near(3+.8+PARAMS['leg_length']+PARAMS['head_thickness']+5,78),'Augstums bez augšējā rāmja: 3 + 0,8 + 68,4 + 0,8 + 5 = 78 cm.')
    ok(near(15+8,23) and PARAMS['shelf_plywood']==0,'Plaukta metāla balsta virsma nomināli 23 cm; saplākšņa klāja nav.')
    ok(not any(p['mark'] in ['T01','T02','T03','P04'] or p['group']=='frame' for p in PARTS),'Augšējā rāmja un P04 modeļa un griešanas sarakstā nav.')
    ok(counts['P01']==4 and counts['P05']==8 and counts['P03']==0 and counts['P06']==0,'Četras balsta plāksnes, astoņas ribas; nav skrūvēto plaukta mezglu vai iegremdēto plākšņu.')
    for p in PARTS:
        if p['mark']=='P01':ok(near(p['origin'][2]+p['size'][2],73),'P01 cieši balsta W01 apakšu pie Z=73.')
        elif p['kind']=='gusset':ok(near(p['top'],72.2) and p['leg']==6 and 3+p['leg']<10,p['instance']+': riba savieno kāju ar P01 un ietilpst zem plāksnes.')
    for cx,cy in CORNERS:
        ribs=[p for p in PARTS if p['kind']=='gusset' and p['centre']==[cx,cy]]
        ok({p['side'] for p in ribs}=={0 if cx==20 else 2,1 if cy==20 else 3},'Katrai kājai divas uz iekšpusi vērstas ribas; pa vienai X un Y virzienā.')
    head_holes={(h['x'],h['y']) for p in PARTS if p['mark']=='P01' for h in p['holes']}
    ok(head_holes==set(TOP_HOLES) and len(head_holes)==16,'Visas 16 plākšņu un saplākšņa urbumu asis sakrīt.')
    quantities={mark:qty for mark,qty,_,_ in HARDWARE}
    ok(quantities['H10']==quantities['H12']==len(TOP_HOLES),'Kokskrūvju un paplākšņu skaits atbilst 16 caurumiem.')
    ok(not any(m in quantities for m in ['H01','H02','H03','H11']),'Nav plaukta M12 vai virsmas caurejošo skrūvju uzgriežņu.')
    ok(near(PARAMS['width']-46,LEG_SPAN_Y-6),f'Plaukta gala sija {fmt(LEG_SPAN_Y-6)} cm aizpilda aili tieši starp kājām.')
    for cx in [20,PARAMS['length']-20]:
        beam=next(p for p in PARTS if p['mark']=='S02' and near(p['origin'][0]+2,cx))
        ok(near(beam['origin'][1],23) and near(beam['origin'][1]+beam['size'][1],PARAMS['width']-23),'S02 abi gali saskaras ar kājām metināšanai bez savienojuma plāksnēm.')
    for beam in [p for p in PARTS if p['mark']=='S01']:
        ok(near(beam['origin'][0],22) and near(beam['origin'][0]+beam['size'][0],PARAMS['length']-22),'S01 abi gali saskaras ar gala sijām metināšanai.')
    ok(near(PARAMS['shelf_width']-2*4,27),f'Plaukta garensijas {fmt(LEG_SPAN_X-4)} cm un šķērslīstes 27 cm precīzi aizpilda ailes.')
    ok(near(SLATS[0]-3,SHELF_X) and near(SLATS[-1]+3,SHELF_X+PARAMS['shelf_length']) and len(SLATS)==13 and all(near(b-a,12) for a,b in zip(SLATS,SLATS[1:])),f'Trīspadsmit šķērslīstes ar 12 cm soli un 6 cm spraugām; ārmalas X={fmt(SHELF_X)} un {fmt(SHELF_X+PARAMS["shelf_length"])} cm.')
    ok(SHELF_X>=22 and SHELF_X+PARAMS['shelf_length']<=PARAMS['length']-22 and SHELF_Y>=23 and SHELF_Y+PARAMS['shelf_width']<=PARAMS['width']-23,'Centrētais plaukta režģis ietilpst starp gala sijām un kājām.')
    boxes=[p for p in PARTS if p['kind']!='gusset'];clashes=[]
    for i,a in enumerate(boxes):
        for b in boxes[i+1:]:
            overlap=[min(a['origin'][j]+a['size'][j],b['origin'][j]+b['size'][j])-max(a['origin'][j],b['origin'][j]) for j in range(3)]
            if min(overlap)>1e-7:clashes.append((a['instance'],b['instance']))
    ok(not clashes,f'{len(boxes)} cauruļu un plākšņu apvalkiem nav savstarpēju tilpuma pārklāšanos: {clashes or "pārbaudīts"}.')
    base_min=[min(p['origin'][i] for p in boxes) for i in range(3)]
    base_max=[max(p['origin'][i]+p['size'][i] for p in boxes) for i in range(3)]
    ok(all(near(a,b) for a,b in zip(base_min,[10,10,3])) and all(near(a,b) for a,b in zip(base_max,[PARAMS['length']-10,PARAMS['width']-10,73])),
       f'Metinātā pamatne ar P01: {fmt(PARAMS["base_length"])} × {fmt(PARAMS["base_width"])} cm plānā; augša 73 cm virs grīdas.')
    for p in boxes:
        for h in p['holes']:
            axis='xyz'.index(h['axis'])
            for k in range(3):
                if k!=axis and not (p['origin'][k]+h['d']/2-1e-7<=h['xyz'[k]]<=p['origin'][k]+p['size'][k]-h['d']/2+1e-7):raise AssertionError('Urbums ārpus '+p['instance'])
    checks.append('Visi apaļie urbumi ietilpst atbilstošajās detaļu plaknēs.')
    for b in stock_nesting():ok(b['used']<=600,f"{b['section']}, sagatave {b['bar']}: griezumi ietilpst 600 cm, ieskaitot zāģējumu un gala rezervi.")
    ok(Counter(m for b in stock_nesting() for m,L in b['pieces'])==Counter({p['mark']:p['qty'] for p in CUTS if p['wall']}),'Cauruļu sadalījumā katra sagatave uzskaitīta tieši vienu reizi.')
    ok(near(PARAMS['top_screw_length']-(.8+.2),3),'Kokskrūve 4 cm: 0,8 plāksne + 0,2 paplāksne + 3 cm ieskrūvējums.')
    ok(4.81-3.3>=1.5,'Pat bez paplāksnes un ar 0,7 biezu plāksni skrūve nesasniedz virspusi; rezerve vismaz 1,5 cm.')
    ok(near(8-5.15,2.85) and near(8-4.81,3.19),'Virsmas biezuma pielaidei balsta regulējums nepieciešams 2,85–3,19 cm.')
    return checks

def write_csv(path,fields,rows):
    with open(path,'w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter=';',lineterminator='\n');w.writeheader()
        for row in rows:w.writerow({k:fmt(v) for k,v in row.items()})
def export_data():
    for d in ['model','drawings']:(ROOT/d).mkdir(exist_ok=True)
    fields=['pozīcija','detaļa','profils_cm','skaits','gatavais_garums_cm','platums_cm','biezums_vai_augstums_cm','piegādātāja_kods','norāde','kopējā_teorētiskā_masa_kg']
    rows=[]
    for p in CUTS:
        rows.append(dict(zip(fields,[p['mark'],p['name'],p['section'],p['qty'],p['length'],p['a'],p['b'],p['code'],f"Gatavs taisnleņķa trīsstūris; katetes {fmt(p['length'])} un {fmt(p['a'])} cm" if p.get('triangle') else 'Taisni gali; garuma pielaide ±0,1 cm; noņemt atskabargas',round(p['qty']*p['mass_each_kg'],3)])))
    write_csv(ROOT/'cutting-list.csv',fields,rows)
    fields=['pozīcija','daudzums','apraksts','piezīme'];write_csv(ROOT/'hardware-list.csv',fields,[dict(zip(fields,r)) for r in HARDWARE])
    fields=['profils_cm','sagataves_numurs','sagataves_garums_cm','gatavās_detaļas_cm','zāģējums_katrai_detaļai_cm','kopējā_galu_rezerve_cm','atlikums_cm']
    write_csv(ROOT/'stock-cutting.csv',fields,[dict(zip(fields,[b['section'],b['bar'],600,' | '.join(f'{m}: {fmt(L)}' for m,L in b['pieces']),.3,2,600-b['used']])) for b in stock_nesting()])
    fields=['detaļas_numurs','urbums','X_cm','Y_cm','Z_cm','ass','diametrs_cm','dziļums_cm','piezīme'];rows=[]
    for p in PARTS:
        for h in p.get('holes',[]):rows.append(dict(zip(fields,[p['instance'],h['purpose'],h['x'],h['y'],h['z'],h['axis'],h['d'],h['depth'],'Tikai viena caurules siena; virziens pa pozitīvo asi' if p['kind']=='tube' else 'Cauri plāksnei; virziens pa pozitīvo asi'])))
    for x,y in TOP_HOLES:
        rows.append(dict(zip(fields,['W01','Kokskrūves priekšurbums no apakšas',x,y,73,'z','Pēc izvēlētās kokskrūves ražotāja',3.2,'Dziļuma ierobežotājs; cauri virsmai neurbt; pārnest pēc sausās montāžas'])))
    write_csv(ROOT/'drilling-coordinates.csv',fields,rows)
    (ROOT/'model'/'design.json').write_text(json.dumps(dict(units='cm',revision=REV,date=DATE,parameters=PARAMS,parts=PARTS),indent=2),encoding='utf-8')
    return validate()
if __name__=='__main__':print('\n'.join(export_data()))
