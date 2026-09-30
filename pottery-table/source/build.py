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
         'module steel(group) { translate([0,0,dz]) color([.73,.12,.08]) children(); }',
         'module washer(x,y,z,od,id,h) {translate([x,y,z]) difference(){cylinder(d=od,h=h);translate([0,0,-.01])cylinder(d=id,h=h+.02);}}',
         'module hexnut(x,y,z,af,h,bore) {translate([x,y,z]) difference(){cylinder(d=af/cos(30),h=h,$fn=6);translate([0,0,-.01])cylinder(d=bore,h=h+.02);}}',
         'module bolt(x,y,z,diam,length,af,head) {translate([x,y,z]) {cylinder(d=diam,h=length);translate([0,0,-head])cylinder(d=af/cos(30),h=head,$fn=6);}}',
         'module deck(x,y,z,l,w,t,r) {color([.89,.77,.55]) translate([x,y,z]) linear_extrude(t) hull() for(a=[r,l-r],b=[r,w-r]) translate([a,b]) circle(r=r);}',
         'pilot_diameter=.5; // Ilustratīvi; priekšurbuma Ø pēc kokskrūves ražotāja.',
         'if(show_top) difference(){deck(0,0,78-top_thickness+exploded,250,125,top_thickness,2.5);']
    for x,y in TOP_HOLES:
        out.append(f'translate([{x},{y},78-top_thickness+exploded-.01]) cylinder(d=pilot_diameter,h=3.21);')
    out.append('}')
    def vec(v):return '['+','.join(f'{x:.6f}'.rstrip('0').rstrip('.') if isinstance(x,float) else str(x) for x in v)+']'
    for p in PARTS:
        prefix='if(show_shelf) ' if p['group']=='shelf' else ''
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
            out.append('}')
        out.append('}')
    out.append('if(show_hardware) {')
    for cx,cy in CORNERS:
        out += [f'color([.2,.23,.24]) translate([{cx},{cy},0]) cylinder(d=8,h=2);',
                f'color([.6,.62,.63]) translate([{cx},{cy},2]) cylinder(d=1.6,h=6);',
                f'translate([0,0,dz]) color([.6,.62,.63]) {{hexnut({cx},{cy},2.2,2.4,.8,1.6);hexnut({cx},{cy},3.8,2.4,1.3,1.6);}}']
    for x,y in TOP_HOLES:
        out.append(f'if(show_top && exploded==0) translate([0,0,dz]) color([.6,.62,.63]) {{washer({x},{y},72,2,.9,.2);bolt({x},{y},72,.8,4,1.3,.55);}}')
    out.append('}')
    (ROOT/'model'/'table.scad').write_text('\n'.join(out)+'\n',encoding='utf-8')

def quote():
    lines=['NESŪTĪTS MELNRAKSTS — cenu piedāvājuma pieprasījums',
           'Kam: biz@metalucentrs.lv','Temats: S235 materiāli un sagarināšana keramikas galdam PT-250, redakcija E',
           '', 'Labdien!', '',
           'Lūdzu cenu piedāvājumu necinkota S235 materiāliem un sagarināšanai pēc zemāk norādītā saraksta. VISI IZMĒRI CENTIMETROS, arī profilu sienu un plākšņu biezumi. Preču kodi paliek piegādātāja oriģinālie. Šī ir redakcija E: BEZ augšējā rāmja; viengabala metināta pamatne, četras balsta plāksnes un metāla plaukts ar 13 šķērslīstēm.',
           '', 'GATAVĀS DETAĻAS — cm']
    for p in CUTS:
        size=f'gatavais garums {fmt(p["length"])} cm' if p['wall'] else f'{fmt(p["length"])} × {fmt(p["a"])} × {fmt(p["b"])} cm'
        if p.get('triangle'):size='taisnleņķa trīsstūris; katetes 6 un 6 cm; biezums 0,6 cm'
        lines.append(f'{p["mark"]}: {p["name"]}; {p["section"]} cm; {p["qty"]} gab.; {size}'+(f'; kods {p["code"]}' if p['code'] else '')+'.')
    lines += ['', 'LŪDZU PRECIZĒT:',
              '1. Materiālu pieejamību, sagatavošanas termiņu un piegādi.',
              '2. Materiālu, griešanas, atskabargu noņemšanas un piegādes izmaksas atsevišķi; norādīt PVN.',
              '3. Vai gatavā garuma pielaide ±0,1 cm un perpendikulāri gali ir nodrošināmi. Zāģējumu pieskaitīt sagataves patēriņam, saglabājot gatavo detaļu izmērus.',
              '4. Vai maksā par nogrieztajām detaļām vai pilnām sagatavēm; lūdzu atdot apmaksātos atlikumus.',
              '5. Atsevišķu cenu P05 trīsstūriem ar norādītajiem gatavajiem izmēriem.',
              '6. Ja iespējama vienkāršu apaļu urbumu izgatavošana — atsevišķu cenu pēc rasējumiem. Standarta sagarināšanā urbšana nav pieņemta kā iekļauta.',
              '7. Ja izmantojat citus materiālu garumus vai zāģējuma platumu, lūdzu pārrēķināt patēriņu, nemainot gatavos izmērus.',
              '', 'Pielikumi: cutting-list.csv; stock-cutting.csv; drawings.pdf; drilling-coordinates.csv.',
              'Plānotais cauruļu iepirkums: 1 × 600 cm profilam 8×4×0,3 cm; 1 × 600 cm profilam 6×4×0,3 cm; 1 × 600 cm profilam 6×6×0,3 cm.',
              'Sadalījumā pieņemts zāģējums 0,3 cm katrai detaļai un 2 cm kopēja gala rezerve katrai 600 cm sagatavei. Plakandzelzs un trīsstūru sagataves aprēķināt atsevišķi.',
              '', 'Šis ir cenu piedāvājuma pieprasījums; pasūtījums tiks apstiprināts atsevišķi. Piegādes adresi norādīsim pirms pasūtīšanas.',
              '', 'Ar cieņu,', '[Vārds, tālrunis]']
    (ROOT/'supplier-quote-lv.txt').write_text('\n'.join(lines)+'\n',encoding='utf-8')

def verification(checks):
    steel=sum(p['mass_each_kg']*p['qty'] for p in CUTS)
    E=21000000; I=(4*8**3-3.4*7.4**3)/12; F=260*9.81/2; L=210
    stress=F*L/4/(I/4)/100; deflection=F*L**3/(48*E*I)
    lines=['# Izmēru pārbaude un vienkāršā projekta robežas',f'Redakcija {REV} · {DATE} · Izmēri cm.',
        '', '## Kas pārbaudīts datorā', '',f'Izpildītas {len(checks)} ģeometrijas pārbaudes. Tas nav fiziska galda slodzes tests.']
    lines += ['- '+c for c in dict.fromkeys(checks) if ': modeļa garums' not in c and ': riba savieno' not in c]
    lines += ['', '## Daudzumi un masa', '',
        f'- {len(PARTS)} tērauda detaļas agrāko 69 vietā; 8 ribas agrāko 16 vietā. Nav P03, P06, M10 vai M12 savienojumu.',
        f'- Teorētiskā tērauda masa {fmt(round(steel,1))} kg; saplāksnim ap 105–119 kg. Kopā ar pēdām un skrūvēm tukšs galds ap {round(steel+105+5)}–{round(steel+119+8)} kg.',
        '- Masai lietoti ideāli taisnstūra profili un tērauda blīvums 0,00785 kg/cm³; precīzu masu nosaka faktiskie materiāli.',
        '- Trīs 600 cm cauruļu sagataves: pa vienai no katra profila; plāksnes un ribas atsevišķi.',
        '', '## Stiprinājumi un stingrība', '',
        '- Kājas un plaukts sametināti vienā pamatnē. S02 79 cm gali tieši saskaras ar kājām; nav skrūvju brīvkustības plaukta savienojumos.',
        '- Pa divām 6 × 6 ribām katras kājas augšā, X un Y virzienā. Virsmas vertikālo slodzi nes četras 20 × 20 plāksnes; kokskrūves notur virsmu pie pamatnes.',
        '- Kokskrūve 4 − P01 0,8 − paplāksne 0,2 = 3 cm kokā; nomināli 2 cm līdz augšpusei. Priekšurbumam dziļuma ierobežotājs 3,2. Pārbaudīt īstās skrūves un priekšurbuma diametru atgriezumā.',
        '- Pirms virsmas uzlikšanas pārbaudīt tukšās pamatnes šūpošanos. Pēc uzlikšanas pārbaudīt vēlreiz, stingri spiežot abos virzienos un stūros. Visas pēdas uz grīdas, kontruzgriežņi pievilkti; šuves un galvu savienojumi nekustas.',
        '- Absolūta nulles kustība nav garantēta: iespējama elastīga izliece un slīdēšana uz konkrētas grīdas. Ja galds slīd, risināt pēdu saķeri vai grīdas fiksāciju, nevis slēpt vaļīgu mezglu ar papildu māla svaru.',
        '', '## Plaukta siju orientējošs aprēķins', '',
        'Divas RHS 8 × 4 × 0,3 ar 8 vertikāli. Katras sijas vidū pielikta puse no 260 kg (200 kg maisi un rezerve paša plaukta masai); laidums 210. Šī vienkāršotā shēma saglabāta no iepriekšējās versijas.',
        f'- I={fmt(I)} cm⁴; E=21000000 N/cm²; spriegums FL/(4×I/4) ap {fmt(stress)} MPa; elastīgā izliece FL³/(48EI) ap {fmt(deflection)} cm.',
        '- Tas nav metinājumu, kājas sienas, kokskrūvju vai visas konstrukcijas nestspējas aprēķins. Vienai līstei 200 kg punktveida slodze nav paredzēta.',
        '', '## Ko jāpārbauda darbnīcā', '',
        '- 200 kg vienmērīgi uz plaukta un 200 kg vienmērīgi uz virsmas saglabāti kā projektēšanas mērķi, nevis sertificēta nestspēja. Četros punktos balstītās saplākšņa plātnes izliece un visu savienojumu izturība nav pilnībā aprēķināta.',
        '- Šuves apskatīt pirms slogošanas; nepārliecinošas šuves parādīt pieredzējušam metinātājam. Slodzi likt pakāpeniski, pēc katra posma pārbaudot šuves, kājas un virsmas/plaukta lieci. Pie plaisām, kustības vai paliekošas deformācijas pārtraukt.',
        '- Smago galdu celt aiz tērauda pamatnes vai noņemt virsmu. Pamatne nav izjaucama: 230 × 105 × 73 cm ar nominālajām pēdām.',
        '- Modelī nav šuvju vaļņu vai reālas koka vītnes. OpenSCAD teksts ģenerēts, bet tā kompilācija nav veikta.',
        '', '## Materiāla atsauce', '',
        'Ražotāja bērza saplākšņa un stiprināšanas informācija: https://www.finieris.com/products/riga-ply/ un https://www.finieris.com/wp-content/uploads/2026/05/RigaWood_PlywoodHandbook.pdf . Ražotāja loksnes dati paši par sevi nav šī galda nestspējas apstiprinājums.']
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
        if p.get('triangle'):size='Katetes 6 un 6; biezums 0,6'
        rows.append([p['mark'],p['name'],p['section'],p['qty'],size])
    story.append(table(['Poz.','Detaļa','Profils, cm','Gab.','Gatavais izmērs, cm'],rows,[15,59,40,12,48]))
    story += [PageBreak(),Paragraph('Cauruļu sagatavju sadalījums',styles['Big']),Paragraph('600 cm sagataves; 0,3 cm zāģējums katrai detaļai; kopā 2 cm rezervē galiem. Plakandzelzs un trīsstūru sagataves aprēķina atsevišķi.',styles['Text'])]
    story.append(table(['Profils, cm / sagatave','Gatavie garumi, cm','Atlikums, cm'],[[b['section']+' / '+str(b['bar']),'; '.join(f'{m}: {fmt(L)}' for m,L in b['pieces']),fmt(600-b['used'])] for b in stock_nesting()],[48,101,25]))
    story += [Spacer(1,0.9*cm),Paragraph('Norādes piegādātājam',styles['H']),Paragraph('Visi norādītie izmēri ir gatavie detaļu izmēri centimetros. Pieskaitīt faktisko zāģējumu, saglabājot detaļu garumus. Marķēt detaļu pozīcijas un noņemt atskabargas. Ja zāģējumam vai galu apgriešanai vajadzīga lielāka rezerve, sadalījumu pārrēķināt.',styles['Text']),Paragraph('Atsevišķi precizēt maksu par pilnām sagatavēm, plakandzelzs minimumus, trīsstūru griešanu un piegādi. Apmaksātos atlikumus atdot pasūtītājam. Pievienotajā nesūtītajā pieprasījumā vēl jāieraksta pasūtītāja kontaktinformācija.',styles['Text'])]
    story += [PageBreak(),Paragraph('Stiprinājumi un saplāksnis',styles['Big']),Paragraph('Pirms urbšanas izvēlēties īstos balstus, metināmos uzgriežņus un kokskrūves ar paplāksnēm. Sausajā montāžā pārbaudīt skrūvju garumus. Skaits gabalos.',styles['Text'])]
    story.append(table(['Poz.','Sk.','Apraksts','Montāžas un iegādes piezīme'],[[m,q,d,n] for m,q,d,n in HARDWARE],[15,14,68,77]))
    story += [PageBreak(),Paragraph('Pārbaudes un aprēķini',styles['Big'])]
    for line in (ROOT/'verification.md').read_text(encoding='utf-8').splitlines():
        if line.startswith('## '):story.append(Paragraph(inline(line[3:]),styles['H']))
        elif line.startswith('- '):story.append(Paragraph('• '+inline(line[2:]),styles['BulletText']))
        elif line and not line.startswith('#') and not line.startswith('Redakcija'):story.append(Paragraph(inline(line),styles['Text']))
    story += [PageBreak(),Paragraph('Izgatavošanas pārbaudes protokols',styles['Big'])]
    story.append(table(['Pārbaude','Rezultāts / pārbaudītājs / datums'],[['Virsmas biezums / galīgais augstums',''],['Kāju diagonāles / līdzenums',''],['Skrūves, šuves un regulējamie balsti',''],['Stingri piespiest sānos un stūros / šūpošanās',''],['Plaukts 50 / 100 / 150 / 200 kg; izliece',''],['Virsmas un kopējā slodze; paliekoša deformācija','']],[85,89],[1.2*cm]+[3*cm]*6))
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
    drawings.add_metadata({'/Title':'PT-250 keramikas galds — A3 rasējumi','/Author':'Izgatavošanas dokumentācija','/Subject':'Redakcija E / visi izmēri cm'})
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
