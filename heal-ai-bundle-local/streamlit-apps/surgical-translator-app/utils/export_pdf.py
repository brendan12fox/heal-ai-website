from fpdf import FPDF
import os
import uuid

font_dir = os.path.join(os.path.dirname(__file__), "fonts")

def create_pdf_from_text(text, title="Translated Instructions"):
    pdf = FPDF()
    pdf.add_page()

    # Add fonts
    pdf.add_font("Noto", "", os.path.join(font_dir, "NotoSans-Regular.ttf"), uni=True)
    pdf.add_font("Arabic", "", os.path.join(font_dir, "NotoSansArabic-Regular.ttf"), uni=True)
    pdf.add_font("Bengali", "", os.path.join(font_dir, "NotoSansBengali-Regular.ttf"), uni=True)

    # Default font
    pdf.set_font("Noto", size=12)

    # Switch font for Arabic/Bengali if needed
    if any("\u0600" <= c <= "\u06FF" for c in text):
        pdf.set_font("Arabic", size=12)
    elif any("\u0980" <= c <= "\u09FF" for c in text):
        pdf.set_font("Bengali", size=12)

    for line in text.split("\n"):
        pdf.multi_cell(0, 10, line)

    file_path = f"/tmp/{uuid.uuid4().hex}.pdf"
    pdf.output(file_path)
    return file_path