"""Ģenerē latviešu dokumentāciju, PDF rasējumus un modeli centimetros."""
from pathlib import Path
import io, json, math, re, zipfile, shutil
from html import escape
from design import ROOT, DATE, REV, CUTS, HARDWARE, PARTS, PARAMS, CORNERS, TOP_HOLES, fmt, export_data, gusset_vertices, stock_nesting
from drawings import build_drawings

def cad():
    out=[f'// PT-250 / Redakcija {REV} / visas koordinātas cm; 1 vienība = 1 cm.',
         '// Izveidots no source/design.py. Cauruļu stūri un stiprinājumi vienkāršoti.',
         '// Šuves nav modelētas; rasējumos dotās prasības ir spēkā. Bez augšējā rāmja.',
         '$fn=36;', 'show_top=true;', 'show_shelf=true;', 'show_hardware=true;',
         'exploded=0; // Tikai ilustrācijai; samontētā stāvoklī 0.',
         'top_thickness=5; // Faktiski 4.81..5.15; galda augša paliek Z=78.',
         'dz=5-top_thickness;',
         'module steel(group) { translate([0,0,(group=="top_hardware"?0:dz)+(group=="legs"?-exploded*.45:group=="shelf"?-exploded*.7:group=="top_hardware"?exploded:0)]) color([.73,.12,.08]) children(); }',
         'module washer(x,y,z,od,id,h) {translate([x,y,z]) difference(){cylinder(d=od,h=h);translate([0,0,-.01])cylinder(d=id,h=h+.02);}}',
         'module hexnut(x,y,z,af,h,bore) {translate([x,y,z]) difference(){cylinder(d=af/cos(30),h=h,$fn=6);translate([0,0,-.01])cylinder(d=bore,h=h+.02);}}',
         'module bolt(x,y,z,diam,length,af,head) {translate([x,y,z]) {cylinder(d=diam,h=length);translate([0,0,-head])cylinder(d=af/cos(30),h=head,$fn=6);}}',
         'module deck(x,y,z,l,w,t,r) {color([.89,.77,.55]) translate([x,y,z]) linear_extrude(t) hull() for(a=[r,l-r],b=[r,w-r]) translate([a,b]) circle(r=r);}',
         'if(show_top) difference(){deck(0,0,78-top_thickness+exploded,250,125,top_thickness,2.5);']
    for x,y in TOP_HOLES:
        out += [f'translate([{x},{y},78-top_thickness+exploded-.01]) cylinder(d=1.05,h=top_thickness+.02);',
                f'translate([{x-2},{y-2},77.4+exploded]) cube([4,4,.61]);']
    out.append('}')
    def vec(v):return '['+','.join(f'{x:.6f}'.rstrip('0').rstrip('.') if isinstance(x,float) else str(x) for x in v)+']'
    for p in PARTS:
        prefix='if(show_shelf) ' if p['group']=='shelf' else 'if(show_top) ' if p['group']=='top_hardware' else ''
        out += [f'// {p["instance"]}',prefix+f'steel("{p["group"]}") '+'{']
        if p['kind']=='gusset':out.append('polyhedron(points='+json.dumps(gusset_vertices(p))+',faces=[[0,1,2],[3,5,4],[0,3,4,1],[1,4,5,2],[2,5,3,0]]);')
        else:
            o=p['origin'];d=p['size'];out += ['difference(){',f'translate({vec(o)}) cube({vec(d)});']
            if p['kind']=='tube':
                axis='xyz'.index(p['axis']);oo=[o[i]+p['wall'] for i in range(3)];dd=[d[i]-2*p['wall'] for i in range(3)]
                oo[axis]=o[axis]-.01;dd[axis]=d[axis]+.02;out.append(f'translate({vec(oo)}) cube({vec(dd)});')
            for h in p['holes']:
                oo=[h['x'],h['y'],h['z']];oo['xyz'.index(h['axis'])]-=.01
                rot='rotate([0,90,0]) ' if h['axis']=='x' else 'rotate([-90,0,0]) ' if h['axis']=='y' else ''
                out.append(f'translate({vec(oo)}) {rot}cylinder(d={h["d"]},h={h["depth"]+.02});')
            for h in p['slots']:
                out.append(f'hull() for(dx=[-.4,.4]) translate([{h["x"]}+dx,{h["y"]},{h["z"]}-.01]) cylinder(d=.8,h=.42);')
            if p['mark']=='P06':
                h=p['holes'][0]
                out.append(f'translate([{h["x"]},{h["y"]},77.5]) cylinder(d1=1,d2=2,h=.5);')
            out.append('}')
        out.append('}')
    out.append('if(show_hardware) {')
    for cx,cy in CORNERS:
        out += [f'translate([0,0,-exploded*.45]) {{ color([.2,.23,.24]) translate([{cx},{cy},0]) cylinder(d=8,h=2);',
                f'color([.6,.62,.63]) translate([{cx},{cy},2]) cylinder(d=1.6,h=6); }}',
                f'translate([0,0,dz-exploded*.45]) color([.6,.62,.63]) {{hexnut({cx},{cy},2.2,2.4,.8,1.6);hexnut({cx},{cy},3.8,2.4,1.3,1.6);}}']
        for x in [cx-11,cx+11]:
            for y in [cy-11,cy+11]:
                out += [f'translate([0,0,dz-exploded*.45]) color([.5,.53,.55]) {{washer({x},{y},72,2,1.05,.2);hexnut({x},{y},71,1.7,1,1);}}',
                        f'if(show_top) translate([{x},{y},exploded]) color([.6,.62,.63]) {{translate([0,0,70.5]) cylinder(d=1,h=7);translate([0,0,77.5]) cylinder(d1=1,d2=2,h=.5);}}']
        angle=90 if cy==20 else -90
        for z in [12.5,25.5]:
            out += [f'translate([{cx},{23 if cy==20 else 102},{z}+dz-exploded*.45]) rotate([{angle},0,0]) color([.5,.53,.55]) hexnut(0,0,0,1.9,1,1.2);',
                    f'if(show_shelf) translate([{cx},{24.85 if cy==20 else 100.15},{z}+dz-exploded*.7]) rotate([{angle},0,0]) color([.6,.62,.63]) {{washer(0,0,0,2.4,1.3,.25);bolt(0,0,0,1.2,3.5,1.9,.75);}}']
    out.append('}')
    (ROOT/'model'/'table.scad').write_text('\n'.join(out)+'\n',encoding='utf-8')

def quote():
    lines=['NESŪTĪTS MELNRAKSTS — cenu piedāvājuma pieprasījums',
           'Kam: biz@metalucentrs.lv','Temats: S235 materiāli un sagarināšana keramikas galdam PT-250, redakcija D',
           '', 'Labdien!', '',
           'Lūdzu cenu piedāvājumu necinkota S235 materiāliem un sagarināšanai pēc zemāk norādītā saraksta. VISI IZMĒRI CENTIMETROS, arī profilu sienu un plākšņu biezumi. Preču kodi paliek piegādātāja oriģinālie. Šī ir redakcija D: BEZ augšējā rāmja; četras tiešā balsta galvas un metāla plaukts ar 13 šķērslīstēm.',
           '', 'GATAVĀS DETAĻAS — cm']
    for p in CUTS:
        size=f'gatavais garums {fmt(p["length"])} cm' if p['wall'] else f'{fmt(p["length"])} × {fmt(p["a"])} × {fmt(p["b"])} cm'
        if p.get('triangle'):size='taisnleņķa trīsstūris; katetes 11 un 11 cm; biezums 0,6 cm'
        lines.append(f'{p["mark"]}: {p["name"]}; {p["section"]} cm; {p["qty"]} gab.; {size}'+(f'; kods {p["code"]}' if p['code'] else '')+'.')
    lines += ['', 'LŪDZU PRECIZĒT:',
              '1. Materiālu pieejamību, sagatavošanas termiņu un piegādi.',
              '2. Materiālu, griešanas, atskabargu noņemšanas un piegādes izmaksas atsevišķi; norādīt PVN.',
              '3. Vai gatavā garuma pielaide ±0,1 cm un perpendikulāri gali ir nodrošināmi. Zāģējumu pieskaitīt sagataves patēriņam, saglabājot gatavo detaļu izmērus.',
              '4. Vai maksā par nogrieztajām detaļām vai pilnām sagatavēm; lūdzu atdot apmaksātos atlikumus.',
              '5. Atsevišķu cenu P05 trīsstūriem ar norādītajiem gatavajiem izmēriem.',
              '6. Ja iespējama urbšana, gremdējumi un ligzdu izgatavošana — atsevišķu cenu pēc rasējumiem. Standarta sagarināšanā urbšana nav pieņemta kā iekļauta.',
              '7. Ja izmantojat citus materiālu garumus vai zāģējuma platumu, lūdzu pārrēķināt patēriņu, nemainot gatavos izmērus.',
              '', 'Pielikumi: cutting-list.csv; stock-cutting.csv; drawings.pdf; drilling-coordinates.csv.',
              'Plānotais cauruļu iepirkums: 1 × 600 cm profilam 8×4×0,3 cm; 1 × 600 cm profilam 6×4×0,3 cm; 1 × 600 cm profilam 6×6×0,3 cm.',
              'Sadalījumā pieņemts zāģējums 0,3 cm katrai detaļai un 2 cm kopēja gala rezerve katrai 600 cm sagatavei. Plakandzelzs un trīsstūru sagataves aprēķināt atsevišķi.',
              '', 'Šis ir cenu piedāvājuma pieprasījums; pasūtījums tiks apstiprināts atsevišķi. Piegādes adresi norādīsim pirms pasūtīšanas.',
              '', 'Ar cieņu,', '[Vārds, tālrunis]']
    (ROOT/'supplier-quote-lv.txt').write_text('\n'.join(lines)+'\n',encoding='utf-8')

def verification(checks):
    steel=sum(p['mass_each_kg']*p['qty'] for p in CUTS)
    E=21000000
    I=(4*8**3-3.4*7.4**3)/12; P=260*9.81/2; L=210
    stress=P*L/4/(I/4)/100; deflection=P*L**3/(48*E*I)
    legI=(6**4-5.4**4)/12
    ideal_sway=300*68.4**3/(12*E*legI)
    topI=125*5**3/12
    top_defl=5*((200+119)*9.81)*210**3/(384*540700*topI)
    lines=['# Ģeometrijas un aprēķinu pārbaude',f'Redakcija {REV} · {DATE} · Visi lineārie izmēri cm.',
        '', '## Automātiskās pārbaudes', '',f'Izpildītas {len(checks)} ģeometrijas pārbaudes; visas sekmīgas. Fiziskās slodzes pārbaudes nav veiktas.']
    lines += ['- IZPILDĪTS: '+c for c in dict.fromkeys(checks) if ': modeļa garums' not in c and ': riba savieno' not in c]
    lines += [
        '- IZPILDĪTS: katras caurules garums un profils atbilst sagatavei; visas 16 ribas savieno L01 un P01.',
        '', '## Materiāli un masa', '',
        f'- Gatavo tērauda detaļu teorētiskā masa {fmt(round(steel,2))} kg; redakcijā C bija ap 140,1 kg. Ietaupījums ap {fmt(round(140.1-steel,1))} kg.',
        '- Masa pēc ideāliem taisnstūra šķērsgriezumiem un blīvuma 0,00785 kg/cm³; neietver urbumu atskaitījumus, šuves un stiprinājumus.',
        '- Saplāksnim nominālais tilpums 156250 cm³; pie aprēķina blīvuma 0,00067–0,00076 kg/cm³ masa 104,7–118,8 kg.',
        f'- Tukša galda aplēse ar 8–12 kg stiprinājumiem un pēdām: {fmt(round(steel+104.7+8))}–{fmt(round(steel+118.8+12))} kg. Jānosver faktiskais galds.',
        '- Caurulēm pa vienai 600 cm sagatavei: RHS 8×4×0,3; RHS 6×4×0,3; SHS 6×6×0,3. Plāksnes pasūta atsevišķi.',
        '', '## Plaukta siju lieces novērtējums', '',
        'Divas RHS 8×4×0,3 sijas ar 8 vertikāli. Vienai sijai piemērota puse no 260 kg (200 kg maisi un 60 kg rezerve plauktam), koncentrēta laiduma vidū; L=210; E=21000000 N/cm². Maisus praksē izvieto vienmērīgi.',
        f'- I=(4×8³−3,4×7,4³)/12={fmt(I)} cm⁴. F={fmt(P)} N; spriegums FL/(4×I/4) ap {fmt(stress)} MPa; izliece FL³/(48EI) ap {fmt(deflection)} cm.',
        '- Tā nav punktveida slodzes atļauja vienai līstei. Savienojumu un metinājumu nestspēja ar sijas formulu netiek pārbaudīta.',
        '', '## Virsma bez augšējā rāmja', '',
        'Virsma tagad ir plātne uz četriem lokāliem 30 × 30 balstiem. Vecais trīs tērauda siju aprēķins vairs nav piemērojams. Ražotāja rokasgrāmatā 50 mm biezumam (šajā projektā 5 cm) ražošanas kontroles apakšējās 5% kvantiles lieces E ir 7021 MPa gar ārējo šķiedru un 5407 MPa šķērsām.',
        f'- Tikai mēroga salīdzinājumam: pilna platuma vienkārša sija ar nepārtrauktiem gala balstiem, E=540700 N/cm², I={fmt(topI)} cm⁴, L=210 un 319 kg vienmērīgu slodzi dotu ap {fmt(top_defl)} cm elastīgu izlieci.',
        '- Šis salīdzinājums NAV četru lokālu balstu plātnes aprēķins, nav konservatīvas robežas pierādījums un neapstiprina 200 kg nestspēju. Jāpārbauda reālais šķiedru virziens, plātnes liece, ilglaicīgā deformācija, lokālie balsti un urbumi.',
        '- Pirms 200 kg pieņemšanas vajadzīgs faktiskās plātnes un savienojumu novērtējums, pēc tam pakāpeniska slodzes pārbaude. Vienkārši noņemt rāmi jau izgatavotam galdam nedrīkst.',
        '', '## Horizontālā stingrība un slīdēšana', '',
        'Slodzes ceļš: virsma → 16 caurejoši M10 ar P06 → četras P01 → metinātas ribas abos virzienos → kājas un pie četrām kājām pievienots plaukts → četras pēdas. Saplākšņa savienojuma stingrība ir būtiska; galda ekspluatācija bez uzstādīta plaukta nav paredzēta.',
        f'- Ideāla atskaites shēma: četras kājas, augšā rotācija bloķēta ar absolūti stingru virsmu, apakšā neslīdošs šarnīrs. I={fmt(legI)} cm⁴; L=68,4; kopējais H=300 N; H L³/(12 E I)={fmt(ideal_sway)} cm. Tā ir tikai kāju elastība, nevis prognozēta visa galda kustība.',
        '- Pie H=300 N un augstuma 78 kopējais moments ir 23400 N·cm. Ja visu momentu uzņem viena galva, 22 cm skrūvju rindu plecs dod ap 1064 N rindā jeb 532 N uz katru no divām stieptām skrūvēm. Tā ir pieprasījuma aplēse, nevis koka, plāksnes, skrūves vai šuves nestspējas pārbaude.',
        '- Slīdēšanai nepieciešams μ m g ≥ H. Piemēram, pie 200 kg tukša galda un H=300 N vajadzīgs μ ≥0,153; reālais berzes koeficients uz konkrētās grīdas nav zināms. Svars un gumijas pēdas paši negarantē nekustīgumu.',
        '- Ja obligāti jānovērš visa galda pārbīde, vajadzīgi četri mehāniski fiksējami balsti pie grīdas. Enkuru tipu, nestspēju un grīdas pamatni nosaka uzstādītājs; enkuri nav iekļauti šajā universālajā materiālu sarakstā.',
        '- Darbnīcas pieņemšanas mērķis: 300 N pie virsmas abos X/Y virzienos un stūros, vispirms tukšam galdam; nobīde pret grīdu ≤0,1, paliekošā nobīde ≤0,02; nav slīdēšanas, pēdu pacelšanās vai klikšķu. Veikt arī ar paredzēto slodzi. Kritērijs nav standartizēts sertifikācijas tests.',
        '', '## Pārbaudes robežas un nodošana', '',
        '- Nav sertificētas nestspējas vai garantijas par absolūti nulles kustību. Nav veikta reālās grīdas, savienojumu padevības, koka ilglaicīgās saspiešanas, metinājumu un plātnes pilna konstrukcijas analīze.',
        '- Kompetentam izgatavotājam jāpārbauda iepriekš minētie mezgli pirms slodzes izmēģinājuma. Pierakstīt slodzi, X/Y kustību, paliekošo deformāciju un datumu; neatbilstošu galdu nelietot, līdz mezgls labots un atkārtoti pārbaudīts.',
        '- Ģeometrijas pārbaude aptver cauruļu/plākšņu ārējos apvalkus, ribu novietojumu un urbumus; neimitē šuves, krāsas kārtu vai īstos instrumentus. CAD skrūves ilustratīvas; OpenSCAD kompilācija nav veikta.',
        '', '## Avoti', '',
        '- Ražotāja 50 mm bērza saplāksnis: https://www.finieris.com/products/riga-ply/',
        '- Ražotāja lieces dati, rokasgrāmatas 3.17. tabula (80. lapa): https://www.finieris.com/wp-content/uploads/2026/05/RigaWood_PlywoodHandbook.pdf',
        '- Izmēri, masas un elementārās elastības formulas: šīs redakcijas parametriskais modelis; skaitļi nav ražotāja apstiprinājums šai galda konstrukcijai.']
    (ROOT/'verification.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')


def guide_pdf():
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_LEFT
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import cm
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfbase.pdfmetrics import registerFontFamily
    from fonts import register_fonts
    register_fonts()
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle('Text',fontName='Body',fontSize=9.2,leading=13.6,spaceAfter=8,textColor=colors.HexColor('#243441')))
    styles.add(ParagraphStyle('H',parent=styles['Text'],fontName='BodyBold',fontSize=14,leading=18,spaceBefore=16,spaceAfter=9,keepWithNext=True))
    styles.add(ParagraphStyle('Big',parent=styles['H'],fontSize=25,leading=31,spaceAfter=15))
    styles.add(ParagraphStyle('BulletText',parent=styles['Text'],leftIndent=11,firstLineIndent=-8,spaceAfter=5))
    styles.add(ParagraphStyle('Cell',parent=styles['Text'],fontSize=7.6,leading=10.2,spaceAfter=0))
    styles.add(ParagraphStyle('CellHead',parent=styles['Cell'],fontName='BodyBold',textColor=colors.white))
    def inline(t):
        t=escape(t)
        t=re.sub(r'`([^`]+)`',r'<font face="BodyBold">\1</font>',t)
        t=re.sub(r'\*\*([^*]+)\*\*',r'<b>\1</b>',t)
        t=re.sub(r'(https://[^\s]+)',r'<link href="\1" color="#b83b31">\1</link>',t)
        return t
    story=[]
    paragraph=[]
    def flush():
        if paragraph:story.append(Paragraph(inline(' '.join(paragraph)),styles['Text']));paragraph.clear()
    for line in (ROOT/'construction-guide.md').read_text(encoding='utf-8').splitlines():
        if line.startswith('# '):flush();story.append(Paragraph(inline(line[2:]),styles['Big']))
        elif line.startswith('## '):flush();story.append(Paragraph(inline(line[3:]),styles['H']))
        elif line.startswith('- '):flush();story.append(Paragraph('• '+inline(line[2:]),styles['BulletText']))
        elif not line.strip():flush()
        else:paragraph.append(line)
    flush()
    def table(headers,rows,widths,row_heights=None):
        data=[[Paragraph(inline(str(v)),styles['CellHead' if i==0 else 'Cell']) for v in row] for i,row in enumerate([headers]+rows)]
        t=Table(data,colWidths=[w/10*cm for w in widths],rowHeights=row_heights,repeatRows=1,hAlign='LEFT')
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#243441')),('VALIGN',(0,0),(-1,-1),'TOP'),
                               ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
                               ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor('#f6f3ed'),colors.white]),('LINEBELOW',(0,0),(-1,0),.5,colors.HexColor('#b83b31'))]))
        return t
    story += [PageBreak(),Paragraph('Tērauda detaļu saraksts',styles['Big']),Paragraph('Gatavie izmēri cm. Taisni gali, izņemot trīsstūrveida ribas. Necinkots S235. Zāģējums pieskaitāms materiāla patēriņam.',styles['Text'])]
    rows=[]
    for p in CUTS:
        size=fmt(p['length']) if p['wall'] else ' × '.join(fmt(p[k]) for k in ['length','a','b'])
        if p.get('triangle'):size='Katetes 11 un 11; biezums 0,6'
        rows.append([p['mark'],p['name'],p['section'],p['qty'],size])
    story.append(table(['Poz.','Detaļa','Profils, cm','Gab.','Gatavais izmērs, cm'],rows,[15,59,40,12,48]))
    story += [PageBreak(),Paragraph('Cauruļu sagatavju sadalījums',styles['Big']),Paragraph('600 cm sagataves; 0,3 cm zāģējums katrai detaļai; kopā 2 cm rezervē galiem. Plakandzelzs un trīsstūru sagataves aprēķina atsevišķi.',styles['Text'])]
    story.append(table(['Profils, cm / sagatave','Gatavie garumi, cm','Atlikums, cm'],[[b['section']+' / '+str(b['bar']),'; '.join(f'{m}: {fmt(L)}' for m,L in b['pieces']),fmt(600-b['used'])] for b in stock_nesting()],[48,101,25]))
    story += [Spacer(1,0.9*cm),Paragraph('Norādes piegādātājam',styles['H']),Paragraph('Visi norādītie izmēri ir gatavie detaļu izmēri centimetros. Pieskaitīt faktisko zāģējumu, saglabājot detaļu garumus. Marķēt detaļu pozīcijas un noņemt atskabargas. Ja zāģējumam vai galu apgriešanai vajadzīga lielāka rezerve, sadalījumu pārrēķināt.',styles['Text']),Paragraph('Atsevišķi precizēt maksu par pilnām sagatavēm, plakandzelzs minimumus, trīsstūru griešanu un piegādi. Apmaksātos atlikumus atdot pasūtītājam. Pievienotajā nesūtītajā pieprasījumā vēl jāieraksta pasūtītāja kontaktinformācija.',styles['Text'])]
    story += [PageBreak(),Paragraph('Stiprinājumi un saplāksnis',styles['Big']),Paragraph('Pirms urbšanas izvēlēties īstos balstus, metināmos uzgriežņus un M10 caurejošos stiprinājumus. Sausajā montāžā pārbaudīt skrūvju garumus. Skaits gabalos.',styles['Text'])]
    story.append(table(['Poz.','Sk.','Apraksts','Montāžas un iegādes piezīme'],[[m,q,d,n] for m,q,d,n in HARDWARE],[15,14,68,77]))
    story += [PageBreak(),Paragraph('Pārbaudes un aprēķini',styles['Big'])]
    for line in (ROOT/'verification.md').read_text(encoding='utf-8').splitlines():
        if line.startswith('## '):story.append(Paragraph(inline(line[3:]),styles['H']))
        elif line.startswith('- '):story.append(Paragraph('• '+inline(line[2:]),styles['BulletText']))
        elif line and not line.startswith('#') and not line.startswith('Redakcija'):story.append(Paragraph(inline(line),styles['Text']))
    story += [PageBreak(),Paragraph('Izgatavošanas pārbaudes protokols',styles['Big'])]
    story.append(table(['Pārbaude','Rezultāts / pārbaudītājs / datums'],[['Virsmas biezums / galīgais augstums',''],['Kāju diagonāles / četru P01 saskare',''],['Skrūves, šuves un regulējamie balsti',''],['Krēsli / 300 N X/Y un stūros; nobīde / paliekošā nobīde',''],['Plaukts 50 / 100 / 150 / 200 kg; izliece',''],['Virsmas un kopējā slodze; paliekoša deformācija','']],[85,89],[1.2*cm]+[3*cm]*6))
    def page(c,doc):
        c.setStrokeColor(colors.HexColor('#deddd5'));c.line(1.8*cm,28.2*cm,19.2*cm,28.2*cm)
        c.setFont('BodyBold',8);c.setFillColor(colors.HexColor('#b83b31'));c.drawString(1.8*cm,28.5*cm,'PT-250 / IZGATAVOŠANAS DOKUMENTĀCIJA')
        c.setFont('Body',7.5);c.setFillColor(colors.HexColor('#62747d'));c.drawString(1.8*cm,1.3*cm,f'Redakcija {REV} · {DATE} · visi izmēri cm');c.drawRightString(19.2*cm,1.3*cm,str(doc.page))
    path=ROOT/'construction-guide.pdf'
    doc=SimpleDocTemplate(str(path),pagesize=A4,rightMargin=1.8*cm,leftMargin=1.8*cm,topMargin=2.3*cm,bottomMargin=2.3*cm,
                          title='PT-250 keramikas galds — izgatavošanas apraksts',author='Izgatavošanas dokumentācija')
    doc.build(story,onFirstPage=page,onLaterPages=page)
    return path

def assemble_pdfs(svg_paths):
    from svglib.svglib import svg2rlg
    from reportlab.graphics import renderPDF
    from fonts import register_fonts
    register_fonts()
    from pypdf import PdfReader, PdfWriter
    drawings=PdfWriter()
    for path in svg_paths:
        b=renderPDF.drawToString(svg2rlg(str(path)))
        drawings.append(PdfReader(io.BytesIO(b)))
    drawings.add_metadata({'/Title':'PT-250 keramikas galds — A3 rasējumi','/Author':'Izgatavošanas dokumentācija','/Subject':'Redakcija D / visi izmēri cm'})
    drawings.write(str(ROOT/'drawings.pdf'))
    guide=guide_pdf()
    combined=PdfWriter();combined.append(str(guide));combined.append(str(ROOT/'drawings.pdf'))
    combined.add_metadata({'/Title':'PT-250 keramikas galds — pilnā dokumentācija','/Author':'Izgatavošanas dokumentācija'})
    combined.write(str(ROOT/'workshop-package.pdf'))

def build():
    checks=export_data();cad();quote();verification(checks)
    reference=ROOT.parent/'Table.jpeg'
    if reference.is_file():
        (ROOT/'reference').mkdir(exist_ok=True)
        shutil.copy2(reference,ROOT/'reference'/'Table.jpeg')
    template=(ROOT/'source'/'viewer.html').read_text(encoding='utf-8')
    (ROOT/'index.html').write_text(template.replace('__MODEL__',json.dumps(PARTS,separators=(',',':'))),encoding='utf-8')
    svgs=build_drawings();assemble_pdfs(svgs)
    from website import build_website
    document_count,preview_count=build_website()
    zpath=ROOT.parent/'pottery-table-workshop-package.zip'
    with zipfile.ZipFile(zpath,'w',compression=zipfile.ZIP_DEFLATED) as z:
        for path in sorted(ROOT.rglob('*')):
            if path.is_file() and '__pycache__' not in path.parts:z.write(path,path.relative_to(ROOT.parent))
        for path in [ROOT.parent/'index.html',ROOT.parent/'README.md',ROOT.parent/'.nojekyll',ROOT.parent/'.gitattributes',ROOT.parent/'.gitignore']:
            if path.is_file():z.write(path,path.relative_to(ROOT.parent))
        for path in sorted((ROOT.parent/'site-assets').rglob('*')):
            if path.is_file():z.write(path,path.relative_to(ROOT.parent))
    print(f'Izveidotas {len(svgs)} A3 lapas, apraksts, saraksti, CAD, skatītājs un ZIP; vietnē {document_count} dokumenti; sekmīgas {len(checks)} ģeometrijas pārbaudes.')

if __name__=='__main__':build()
