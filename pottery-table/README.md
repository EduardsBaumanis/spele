# Keramikas galds — vienkāršā redakcija F

Virsma 200 × 100 × 5 cm, augstums 78 cm. Viena sametināta tērauda pamatne ar plauktu, četras balsta plāksnes, astoņas nelielas ribas un parastas kokskrūves no apakšas. Augšējā rāmja, frēzētu ielaidumu un skrūvētu plaukta savienojumu nav. Kopā 37 tērauda detaļas.

Atveriet [dokumentu vietni](../index.html) vai [3D modeli](index.html). Virsmu var noņemt; kājas un plaukts neizjaucas. Pirms izgatavošanas pārbaudiet viengabala pamatnes 180 × 80 × 73 cm pārvietošanas ceļu.

- [Pilnais PDF](workshop-package.pdf) un [septiņi A3 rasējumi](drawings.pdf).
- [Vienkāršā būvēšanas secība](construction-guide.md) un [izmēru pārbaude](verification.md).
- [Tērauda detaļas](cutting-list.csv), [skrūves un pēdas](hardware-list.csv), [sagatavju sadalījums](stock-cutting.csv), [urbumi](drilling-coordinates.csv).
- [Nesūtīts cenu pieprasījuma melnraksts](supplier-quote-lv.txt).
- [OpenSCAD modelis](model/table.scad) un [modeļa dati](model/design.json).

Visi izgatavošanas izmēri cm. CSV semikols un decimālais komats; JSON/CAD decimālais punkts. Rasējumi: S01 kopskats, S02 balsti, S03 augstumi, S04 kāju galvas, S05 plaukts, S06 kokskrūves, S07 metināšanas secība. Izmantojiet tikai redakciju F.

200 kg plauktam un 200 kg vienmērīgi uz virsmas ir projektēšanas mērķi, nevis sertificēta nestspēja. Pārbaudiet šuves, pēdu saskari un tukša galda šūpošanos; slodzi palieliniet pakāpeniski. Šaubīgas šuves parādiet pieredzējušam metinātājam. Masa un pārbaudes robežas dotas verification.md.

## Atkārtota ģenerēšana

Python 3; reportlab, svglib, pypdf un pymupdf; DejaVu Sans vai Windows Arial. No projekta saknes:

```sh
python -m pip install -r pottery-table/source/requirements.txt
python -X utf8 pottery-table/source/build.py
```

Komanda atjauno CSV, modeli, vietni, PDF, SVG, priekšskatījumus un ZIP. Avoti source/design.py, source/drawings.py un construction-guide.md. 3D skatā poga **Sadalīt detaļās** atdala visas 37 tērauda detaļas, virsmu un četras pēdas, automātiski ietilpinot tās skatā. **Samontēts** atjauno salikto galdu. Detaļu izmēri nemainās; sadalījums ir tikai ilustrācija, jo pamatne ir sametināta. Atsevišķais slīdnis paceļ tikai noņemamo virsmu. OpenSCAD modelis šajā vidē nav kompilēts.
