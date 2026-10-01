"""Statiskā vietne: PDF priekšskatījumi, SVG lasītājs un apraksts GitHub Pages."""
from pathlib import Path
from html import escape
import hashlib, json, re, shutil, subprocess
from pypdf import PdfReader
from design import ROOT, REV, DATE, PARAMS, CUTS, fmt

SHEETS=[
 ('S01','Kopskats un galvenie izmēri','Galda izskats, izmēri un pārvadāšanas mezgli.'),
 ('S02','Tiešie virsmas balsti','Četras stingras kāju galvas; bez augšējā rāmja.'),
 ('S03','Sānskati un augstumi','Galda un metāla plaukta augstumu ķēde.'),
 ('S04','Kāju mezgli un pēdas','Augšējās plāksnes, stiprinājuma ribas un regulējamie balsti.'),
 ('S05','Plaukta metāla rāmis','13 šķērslīstes, 6 cm spraugas; maisi balstās uz metāla.'),
 ('S06','Galda virsmas stiprinājumi','16 parastas kokskrūves no apakšas; augšpuse gluda.'),
 ('S07','Pamatnes metināšanas secība','Plaukts piemetināts kājām; vienkārši, pieejami savienojumi.'),
]

def inline(text):
    text=escape(text)
    # Preserve URLs before bold markup; all input is our local authored Markdown.
    text=re.sub(r'https://[^\s]+',lambda m:f'<a href="{m.group(0)}" target="_blank" rel="noopener">{m.group(0)}</a>',text)
    text=re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',text)
    return re.sub(r'`([^`]+)`',r'<code>\1</code>',text)

def guide_html():
    out=['<div class="guide-intro">'];paragraph=[];in_list=False;in_section=False;section=0
    def flush():
        if paragraph:out.append('<p>'+inline(' '.join(paragraph))+'</p>');paragraph.clear()
    def end_list():
        nonlocal in_list
        if in_list:out.append('</ul>');in_list=False
    for line in (ROOT/'construction-guide.md').read_text(encoding='utf-8').splitlines():
        if line.startswith('# '):continue
        if line.startswith('## '):
            flush();end_list();out.append('</div></details>' if in_section else '</div>')
            section+=1;out.append(f'<details id="guide-{section}"><summary>{escape(line[3:])}</summary><div class="guide-body">');in_section=True
        elif line.startswith('- '):
            flush()
            if not in_list:out.append('<ul>');in_list=True
            out.append('<li>'+inline(line[2:])+'</li>')
        elif not line.strip():flush();end_list()
        else:end_list();paragraph.append(line)
    flush();end_list();out.append('</div></details>' if in_section else '</div>')
    return '\n'.join(out)

def build_website():
    site=ROOT.parent;assets=site/'site-assets';pages=assets/'pdf-pages';pages.mkdir(parents=True,exist_ok=True)
    guide=ROOT/'construction-guide.pdf';reader=PdfReader(guide)
    # Hash the content streams, not PDF creation timestamps, to avoid re-rendering identical pages.
    streams=b''.join(p.get_contents().get_data() for p in reader.pages)
    digest=hashlib.sha256(b'preview-1600-pymupdf-v2'+streams).hexdigest()
    stamp=pages/'manifest.json'
    old=json.loads(stamp.read_text(encoding='utf-8')) if stamp.exists() else {}
    page_files=[pages/f'guide-{i:02d}.png' for i in range(1,len(reader.pages)+1)]
    if old.get('digest')!=digest or not all(p.exists() for p in page_files):
        import pymupdf
        # Delete only obsolete previews in this fixed, resolved output directory.
        with pymupdf.open(guide) as pdf:
            for page,path in zip(pdf,page_files):
                page.get_pixmap(matrix=pymupdf.Matrix(1600/page.rect.width,1600/page.rect.width),alpha=False).save(path)
        for path in pages.glob('guide-*.png'):
            if path not in page_files:path.unlink()
        stamp.write_text(json.dumps(dict(digest=digest,pages=len(reader.pages)),indent=2)+'\n',encoding='utf-8')
    guide_pages=[str(p.relative_to(site)) for p in page_files]
    drawing_pages=[f'pottery-table/drawings/{sid}.svg' for sid,_,_ in SHEETS]
    docs=[
        dict(id='guide',type='PDF',title='Izgatavošanas apraksts',description='Darbu secība, izmēri, detaļu saraksti un pārbaudes.',file='pottery-table/construction-guide.pdf',pages=guide_pages,keywords='plāns instrukcija'),
        dict(id='drawings',type='PDF',title='Visi rasējumi',description='Septiņas A3 lapas ar izgatavošanas izmēriem centimetros.',file='pottery-table/drawings.pdf',pages=drawing_pages,keywords='rāmis plaukts kājas'),
        dict(id='complete',type='PDF',title='Pilnā dokumentācija',description='Izgatavošanas apraksts un visi septiņi rasējumi vienā PDF.',file='pottery-table/workshop-package.pdf',pages=guide_pages+drawing_pages,keywords='pilns plāns'),
    ]+[dict(id=sid,type='SVG',title=title,description=description,file=f'pottery-table/drawings/{sid}.svg',pages=[f'pottery-table/drawings/{sid}.svg'],keywords=sid) for sid,title,description in SHEETS]
    assert len(PdfReader(ROOT/'workshop-package.pdf').pages)==len(guide_pages)+len(drawing_pages)
    links=[]
    for doc in docs:
        badge=doc['id'] if doc['type']=='SVG' else 'PDF'
        note=f"{doc['type']} · A3 · cm" if doc['type']=='SVG' else f"PDF · {len(doc['pages'])} lapas"
        current=' aria-current="true"' if doc['id']=='guide' else ''
        links.append(f'<a class="document-link" href="{doc["file"]}" data-document="{doc["id"]}"{current}><span class="document-symbol" aria-hidden="true">{badge}</span><span><strong>{escape(doc["title"])}</strong><small>{note}</small></span></a>')
    rows=[]
    for p in CUTS:
        size=fmt(p['length']) if p['wall'] else ' × '.join(fmt(p[k]) for k in ['length','a','b'])
        if p.get('triangle'):size='Katetes 6 un 6; biezums 0,6'
        row=[p['mark'],p['name'],p['section'],p['qty'],size]
        rows.append('<tr>'+''.join('<td>'+escape(str(v))+'</td>' for v in row)+'</tr>')
    table='<table><caption class="sr-only">Tērauda griešanas saraksts, izmēri cm</caption><thead><tr>'+''.join(f'<th scope="col">{h}</th>' for h in ['Pozīcija','Detaļa','Profils, cm','Skaits','Gatavais izmērs, cm'])+'</tr></thead><tbody>'+''.join(rows)+'</tbody></table>'
    viewer=(ROOT/'index.html').read_text(encoding='utf-8')
    workspace=viewer.split('<div class="workspace">',1)[1].split('<div class="downloads">',1)[0]
    viewer_script=viewer.split('<script>',1)[1].split('</script>',1)[0]
    template=(ROOT/'source'/'site'/'page.html').read_text(encoding='utf-8')
    values=dict(REV=REV,DATE=DATE,LENGTH=str(PARAMS['length']),WIDTH=str(PARAMS['width']),VIEWER='<div class="workspace">'+workspace,VIEWER_SCRIPT=viewer_script,
        DOCUMENT_LINKS='\n'.join(links),FIRST_PAGE=guide_pages[0],DOCUMENT_DATA=json.dumps(docs,ensure_ascii=False),CUT_TABLE=table,GUIDE_HTML=guide_html())
    for name,value in values.items():template=template.replace('__'+name+'__',value)
    assert not re.search(r'__[A-Z_]+__',template),'Vietnē palicis neaizpildīts lauks'
    (site/'index.html').write_text(template,encoding='utf-8')
    (site/'.nojekyll').write_text('')
    for name in ['site.css','site.js']:shutil.copy2(ROOT/'source'/'site'/name,assets/name)
    return len(docs),len(guide_pages)
