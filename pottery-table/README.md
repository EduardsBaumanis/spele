# Keramikas darba galds — redakcija D

Atjaunots 2026. gada 30. septembrī. Dokumentācija latviešu valodā; visi izgatavošanas izmēri centimetros.

Plaukts ar četriem skrūvētiem mezgliem pievienots galda kājām. Projektēšanas mērķis ir 200 kg vienmērīgi izvietotu māla maisu. Metāla režģa zona 150 × 35 cm, nomināli 23 cm virs grīdas; 13 šķērslīstes ar 6 cm brīvām spraugām. Saplākšņa klāja nav. Režģi nes divas RHS 8 × 4 × 0,3 cm garensijas un divas gala šķērssijas ar 8 cm vertikāli. Augšējā rāmja nav; 5 cm virsma tieši stiprināta četrām 30 × 30 cm kāju galvām ar ribām abos virzienos un 16 caurejošiem M10.

- [Pilnā izgatavošanas dokumentācija PDF](workshop-package.pdf) — apraksts, saraksti, aprēķini un septiņas A3 rasējumu lapas.
- [Rasējumi PDF](drawings.pdf) — S01 kopskats; S02 tiešie virsmas balsti; S03 sānskati; S04 kāju augšējie mezgli; S05 plaukts; S06 saplāksnis; S07 plaukta savienojumi ar kājām.
- [Bezsaistes 3D skatītājs](index.html) — atvērt pārlūkā; var noņemt virsmu, paslēpt plauktu, pagriezt un izvērst mezglus.
- [Izgatavošanas apraksts](construction-guide.md) un [pārbaudes protokols](verification.md).
- [Tērauda detaļas](cutting-list.csv), [stiprinājumi](hardware-list.csv), [sagatavju sadalījums](stock-cutting.csv), [urbumu koordinātas](drilling-coordinates.csv).
- [Nesūtīts cenas pieprasījums](supplier-quote-lv.txt) latviešu valodā. Nekas nav pasūtīts vai nosūtīts piegādātājam.
- [OpenSCAD modelis](model/table.scad), [modeļa dati](model/design.json), [atsauces foto](reference/Table.jpeg).

Visi PDF, CSV un modeļa izmēri ir cm. CSV atdalītājs ir semikols, decimālatdalītājs komats. JSON un OpenSCAD viena vienība ir 1 cm; programmēšanas sintaksē decimālatdalītājs ir punkts. M10, M12 un M16 ir standarta vītņu apzīmējumi, nevis pārrēķināti garumi. Skrūvju garumi norādīti atsevišķi cm. Rasējumus izdrukāt faktiskajā izmērā uz A3; pārbaudīt 5 cm kontroles līniju.

Nesošie plaukta mezgli pie galda galiem samazina vietu pēdām. Ar īstajiem krēsliem jāpārbauda visas astoņas darba vietas. 200 kg plauktam un 200 kg virsmai ir projektēšanas un pieņemšanas mērķi, nevis sertificēta nestspēja. Pirms lietošanas jāpārbauda faktiskie metinājumi, savienojumi, stabilitāte un pakāpeniska slogošana. Tukša galda masas aplēse dota verification.md.

## Vietne

Atveriet [dokumentu vietni](../index.html): visi PDF un SVG vienā skatītājā, lapu izvēle, tuvināšana un lasāms apraksts. [GitHub Pages publicēšanas norādes](../README.md).

## Atkārtota ģenerēšana

Python 3 ar reportlab, svglib, pypdf un pymupdf; DejaVu Sans vai Windows Arial fonts. Izmēru avots ir source/design.py; rasējumu izkārtojums source/drawings.py; apraksts construction-guide.md. Komanda no projekta vecākmapes:

```sh
python -m pip install -r pottery-table/source/requirements.txt
python -X utf8 pottery-table/source/build.py
```

Ģenerēšana pārbauda ģeometriju, izveido PDF, modeļus, CSV, skatītāju un pottery-table-workshop-package.zip. OpenSCAD modelis nav šajā vidē kompilēts; precīzie urbumi modelēti tekstā, pārlūka vizualizācijā stiprinājumi un cauruļu stūri ir vienkāršoti. Iepriekšējo redakciju A, B un C sarakstus izmantot nedrīkst.

Redakcijas D stabilitātes pieņemšana: arī tukšam galdam 300 N abos horizontālajos virzienos un stūros, nobīdes mērķis ≤0,1 cm. Faktiskās plātnes un mezglu novērtējums un fiziska pārbaude obligāti pirms lietošanas; absolūts nekustīgums nav pierādīts. Ja nepieļaujama pārbīde, vajadzīga grīdai atbilstoša mehāniska fiksācija.
