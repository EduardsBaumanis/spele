# Keramikas darba galds — vietne GitHub Pages

Latviska izgatavošanas dokumentācija galdam 250 × 125 cm. Redakcija D: plaukts stiprinās pie četrām kājām; četras šķērslīstes un divas garensijas balsta pieskrūvētu 154 × 39 × 3 cm bērza saplākšņa klāju ar 2 cm pārkari pār centrālo 150 × 35 cm balsta zonu. Klāja augša nomināli 26,2 cm virs grīdas. Visi lineārie izmēri centimetros.

Atveriet **[index.html](index.html)**. Vietnē ir 3D modelis, visi trīs PDF un septiņi SVG rasējumi ar lapu izvēli un tuvināšanu, detaļu tabula un lasāms apraksts. PDF priekšskatījumi ir lokāli attēli; vietnei nav vajadzīgs servera kods, ārējas bibliotēkas vai pārlūka PDF spraudnis. Oriģinālie PDF un SVG ir pieejami lejupielādei.

3D skatā poga **Sadalīt detaļās** atdala visas 75 tērauda detaļas, abus saplākšņa klājus un četras pēdas; skats automātiski ietilpina visu konstrukciju. Detaļu izmēri saglabājas, atdalījuma attālumi ir ilustratīvi. Poga **Samontēts** atjauno salikto galdu. Atsevišķais slīdnis joprojām paredzēts lielo montāžas mezglu atdalīšanai.

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

Ģenerēšanai vajadzīgs Python 3, `reportlab`, `cairosvg`, `pypdf`, Cairo, DejaVu Sans un `pdftoppm` no `poppler-utils`. No repozitorija saknes:

```sh
python3 pottery-table/source/build.py
```

Komanda atjauno CSV, CAD, visus PDF un SVG, PDF priekšskatījumus, vietni un `pottery-table-workshop-package.zip`. Priekšskatījumi tiek pārrenderēti, ja PDF lapu saturs mainās. Pēc ģenerēšanas publicējiet arī atjaunotos statiskos failus.

Plaukta 200 kg slodze ir projektēšanas un pieņemšanas mērķis, nevis sertificēta nestspēja. Pirms lietošanas jāpārbauda izgatavotie mezgli un pakāpeniska slogošana; pilnas norādes aprakstā.
