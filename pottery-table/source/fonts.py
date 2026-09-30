"""Use an installed Unicode font on both Windows and Linux."""
from pathlib import Path
import os

def register_fonts():
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from svglib.fonts import register_font
    candidates=[Path('/usr/share/fonts/truetype/dejavu'),Path(os.environ.get('WINDIR','C:/Windows'))/'Fonts']
    for folder in candidates:
        regular,bold=('DejaVuSans.ttf','DejaVuSans-Bold.ttf') if folder.name!='Fonts' else ('arial.ttf','arialbd.ttf')
        if (folder/regular).is_file() and (folder/bold).is_file():break
    else:raise RuntimeError('Install DejaVu Sans or Arial for Latvian PDF text.')
    for name,file in [('Body',regular),('BodyBold',bold),('DejaVu Sans',regular),('DejaVu Sans-Bold',bold)]:
        pdfmetrics.registerFont(TTFont(name,str(folder/file)))
    pdfmetrics.registerFontFamily('Body',normal='Body',bold='BodyBold',italic='Body',boldItalic='BodyBold')
    pdfmetrics.registerFontFamily('DejaVu Sans',normal='DejaVu Sans',bold='DejaVu Sans-Bold',italic='DejaVu Sans',boldItalic='DejaVu Sans-Bold')
    # svglib maintains its own font lookup; ReportLab registration alone falls
    # back to Helvetica on Windows and loses Latvian glyphs in the drawings.
    for weight,file in [('normal',regular),('bold',bold)]:
        register_font('DejaVu Sans',str(folder/file),weight=weight)
