# Keramikas darba galds — vietne GitHub Pages

Latviska dokumentācija galdam 250 × 125 cm. Redakcija E: viena metināta pamatne, 5 cm bērza virsma ar kokskrūvēm no apakšas, astoņas mazas ribas un regulējamas pēdas. Augšējā rāmja nav. Metāla plaukts piemetināts kājām. Visi izgatavošanas izmēri centimetros.

Atveriet **[index.html](index.html)**. Vietnē ir 3D modelis, visi trīs PDF un septiņi SVG rasējumi ar lapu izvēli un tuvināšanu, detaļu tabula un lasāms apraksts. PDF priekšskatījumi ir lokāli attēli; vietnei nav vajadzīgs servera kods, ārējas bibliotēkas vai pārlūka PDF spraudnis. Oriģinālie PDF un SVG ir pieejami lejupielādei.

## Publicēšana GitHub Pages

1. Pievienojiet repozitorijam `index.html`, `.nojekyll`, visu `site-assets/` un `pottery-table/` mapi. Lietojiet šeit esošo mapju struktūru. ZIP arhīvs publicēšanai nav nepieciešams.
2. Nosūtiet šos failus uz sava repozitorija `main` zaru.
3. GitHub atveriet **Settings → Pages → Build and deployment**.
4. Izvēlieties **Deploy from a branch**, zaru **main** un mapi **/(root)**, tad **Save**.
5. Sagaidiet GitHub norādīto vietnes adresi. Projekta vietnei tā parasti ir `https://LIETOTĀJS.github.io/REPOZITORIJS/`.

Visas vietējās saites ir relatīvas, tāpēc vietne darbojas arī repozitorija apakšceļā. Nav vajadzīgs domēns vai GitHub Actions konfigurācija. Šajā uzdevumā vietne ir sagatavota; tā nav nosūtīta uz GitHub vai publicēta.

[GitHub oficiālā publicēšanas instrukcija](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).

## Lokāla apskate

Var atvērt `index.html` tieši pārlūkā. Lai pārbaudītu tāpat kā tīmeklī, no šīs mapes palaidiet:

```sh
python3 -m http.server 8000
```

Tad atveriet `http://localhost:8000`. Vietne nelieto `fetch`, tādēļ lokālajiem datiem nav nepieciešams ārējs serveris.

## Dokumentācijas atjaunošana

Izmēri un modeļa dati: `pottery-table/source/design.py`. Rasējumi: `pottery-table/source/drawings.py`. Apraksts: `pottery-table/construction-guide.md`. Vietnes avoti: `pottery-table/source/site/` un `pottery-table/source/website.py`.

Ģenerēšanai vajadzīgs Python 3, `reportlab`, `svglib`, `pypdf`, `pymupdf` un DejaVu Sans vai Windows Arial. No repozitorija saknes:

```sh
python -m pip install -r pottery-table/source/requirements.txt
python -X utf8 pottery-table/source/build.py
```

Komanda atjauno CSV, CAD, visus PDF un SVG, PDF priekšskatījumus, vietni un `pottery-table-workshop-package.zip`. Priekšskatījumi tiek pārrenderēti, ja PDF lapu saturs mainās. Pēc ģenerēšanas publicējiet arī atjaunotos statiskos failus.

Plaukta 200 kg slodze ir projektēšanas un pieņemšanas mērķis, nevis sertificēta nestspēja. Pirms lietošanas jāpārbauda izgatavotie mezgli un pakāpeniska slogošana; pilnas norādes aprakstā.

Pamatne nav izjaucama (230 × 105 × 73 cm); virsma ir noņemama. Pirms izgatavošanas pārbaudiet pārvietošanas ceļu. Gatavam galdam pārbaudiet šuves, pēdu līmeni un šūpošanos, pēc tam slodzi palieliniet pakāpeniski.
