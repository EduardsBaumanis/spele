# Keramikas darba galds — redakcija B

Atjaunots 2026. gada 28. septembrī. Dokumentācija latviešu valodā; visi izgatavošanas izmēri centimetros.

Plaukts ar četriem skrūvētiem mezgliem pievienots galda kājām. Projektēšanas mērķis ir 200 kg vienmērīgi izvietotu māla maisu. Klājs 150 × 35 × 1,8 cm, nomināli 25 cm virs grīdas. To nes divas RHS 8 × 4 × 0,3 cm garensijas un divas gala šķērssijas ar 8 cm vertikāli. Nav piekaru pie augšējā rāmja.

- [Pilnā izgatavošanas dokumentācija PDF](workshop-package.pdf) — apraksts, saraksti, aprēķini un septiņas A3 rasējumu lapas.
- [Rasējumi PDF](drawings.pdf) — S01 kopskats; S02 augšējais rāmis; S03 sānskati; S04 kāju augšējie mezgli; S05 plaukts; S06 saplāksnis; S07 plaukta savienojumi ar kājām.
- [Bezsaistes 3D skatītājs](index.html) — atvērt pārlūkā; var noņemt virsmu, paslēpt plauktu, pagriezt un izvērst mezglus.
- [Izgatavošanas apraksts](construction-guide.md) un [pārbaudes protokols](verification.md).
- [Tērauda detaļas](cutting-list.csv), [stiprinājumi](hardware-list.csv), [sagatavju sadalījums](stock-cutting.csv), [urbumu koordinātas](drilling-coordinates.csv).
- [Nesūtīts cenas pieprasījums](supplier-quote-lv.txt) latviešu valodā. Nekas nav pasūtīts vai nosūtīts piegādātājam.
- [OpenSCAD modelis](model/table.scad), [modeļa dati](model/design.json), [atsauces foto](reference/Table.jpeg).

Visi PDF, CSV un modeļa izmēri ir cm. CSV atdalītājs ir semikols, decimālatdalītājs komats. JSON un OpenSCAD viena vienība ir 1 cm; programmēšanas sintaksē decimālatdalītājs ir punkts. M6, M12 un M16 ir standarta vītņu apzīmējumi, nevis pārrēķināti garumi. Skrūvju garumi norādīti atsevišķi cm. Rasējumus izdrukāt faktiskajā izmērā uz A3; pārbaudīt 5 cm kontroles līniju.

Nesošie plaukta mezgli pie galda galiem samazina vietu pēdām. Ar īstajiem krēsliem jāpārbauda visas astoņas darba vietas. 200 kg plauktam un 200 kg virsmai ir projektēšanas un pieņemšanas mērķi, nevis sertificēta nestspēja. Pirms lietošanas jāpārbauda faktiskie metinājumi, savienojumi, stabilitāte un pakāpeniska slogošana. Aptuvenā tukša galda masa 255–280 kg.

## Atkārtota ģenerēšana

Python 3 ar reportlab, cairosvg un pypdf; sistēmā pieejams Cairo un DejaVu Sans fonts. Izmēru avots ir source/design.py; rasējumu izkārtojums source/drawings.py; apraksts construction-guide.md. Komanda no projekta vecākmapes:

```sh
python3 pottery-table/source/build.py
```

Ģenerēšana pārbauda ģeometriju, izveido PDF, modeļus, CSV, skatītāju un pottery-table-workshop-package.zip. OpenSCAD modelis nav šajā vidē kompilēts; precīzie urbumi modelēti tekstā, pārlūka vizualizācijā stiprinājumi un cauruļu stūri ir vienkāršoti. Sākotnējās redakcijas A sarakstus un piekaru izmērus izmantot nedrīkst.
