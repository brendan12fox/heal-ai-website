from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import tempfile

def create_pdf_from_text(text, title="Surgical Instructions"):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
        doc = SimpleDocTemplate(f.name, pagesize=letter, topMargin=0.75*inch, bottomMargin=0.75*inch)
        styles = getSampleStyleSheet()
        body_style = styles["BodyText"]
        body_style.spaceAfter = 12

        heading_style = ParagraphStyle(
            name='Heading',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=18,
            alignment=1  # Centered
        )

        flow = [Paragraph(title, heading_style), Spacer(1, 0.25 * inch)]

        for line in text.split("\n"):
            line = line.strip()
            if not line:
                continue
            if line.startswith("- "):  # bullet
                bullet = line[2:].strip()
                flow.append(ListFlowable([ListItem(Paragraph(bullet, body_style))], bulletType='bullet'))
            elif line.startswith("##"):  # subheader
                flow.append(Paragraph(f"<b>{line[2:].strip()}</b>", styles["Heading3"]))
            elif line.startswith("#"):  # main section header
                flow.append(Paragraph(f"<b>{line[1:].strip()}</b>", styles["Heading2"]))
            else:
                flow.append(Paragraph(line, body_style))

        doc.build(flow)
        return f.name