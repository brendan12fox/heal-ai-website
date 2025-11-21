from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import tempfile
import re

def create_pdf_from_text(text, title="Surgical Instructions"):
    """
    Create a PDF from text content with proper formatting.
    
    Args:
        text: The text content to convert to PDF
        title: The title of the document
    
    Returns:
        Path to the created PDF file
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
        doc = SimpleDocTemplate(
            f.name, 
            pagesize=letter, 
            topMargin=1*inch, 
            bottomMargin=1*inch,
            leftMargin=0.75*inch,
            rightMargin=0.75*inch
        )
        styles = getSampleStyleSheet()
        
        # Title style
        title_style = ParagraphStyle(
            name='Title',
            parent=styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=0.3*inch,
            alignment=1,  # Centered
            fontName='Helvetica-Bold'
        )
        
        # Section header style
        section_style = ParagraphStyle(
            name='Section',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#333333'),
            spaceBefore=0.2*inch,
            spaceAfter=0.15*inch,
            fontName='Helvetica-Bold'
        )
        
        # Subsection style
        subsection_style = ParagraphStyle(
            name='Subsection',
            parent=styles['Heading3'],
            fontSize=12,
            textColor=colors.HexColor('#555555'),
            spaceBefore=0.15*inch,
            spaceAfter=0.1*inch,
            fontName='Helvetica-Bold'
        )
        
        # Body text style
        body_style = ParagraphStyle(
            name='Body',
            parent=styles['BodyText'],
            fontSize=11,
            leading=14,
            spaceAfter=0.1*inch,
            leftIndent=0,
            rightIndent=0
        )
        
        # Bullet style
        bullet_style = ParagraphStyle(
            name='Bullet',
            parent=body_style,
            leftIndent=0.3*inch,
            bulletIndent=0.15*inch,
            spaceAfter=0.08*inch
        )

        flow = [Paragraph(title, title_style), Spacer(1, 0.2 * inch)]

        lines = text.split("\n")
        in_list = False
        current_list_items = []
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            # Skip empty lines (but add spacing after sections)
            if not line:
                if not in_list and flow and isinstance(flow[-1], Paragraph):
                    flow.append(Spacer(1, 0.1 * inch))
                continue
            
            # Handle numbered lists (1., 2., etc.)
            numbered_match = re.match(r'^(\d+)\.\s+(.+)$', line)
            if numbered_match:
                if in_list:
                    # Close previous list
                    if current_list_items:
                        flow.append(ListFlowable(current_list_items, bulletType='bullet'))
                    current_list_items = []
                    in_list = False
                    flow.append(Spacer(1, 0.1 * inch))
                
                item_text = numbered_match.group(2)
                # Handle bold text in items
                item_text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', item_text)
                flow.append(Paragraph(f"{numbered_match.group(1)}. {item_text}", body_style))
                continue
            
            # Handle bullet points
            if line.startswith("- ") or line.startswith("• "):
                if not in_list:
                    in_list = True
                    current_list_items = []
                
                bullet_text = line[2:].strip()
                # Handle bold text in bullets
                bullet_text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', bullet_text)
                current_list_items.append(ListItem(Paragraph(bullet_text, body_style)))
                continue
            else:
                # Close any open list
                if in_list:
                    if current_list_items:
                        flow.append(ListFlowable(current_list_items, bulletType='bullet'))
                    current_list_items = []
                    in_list = False
                    flow.append(Spacer(1, 0.1 * inch))
            
            # Handle section headers (##)
            if line.startswith("##"):
                header_text = line[2:].strip()
                # Remove markdown bold if present
                header_text = re.sub(r'\*\*(.+?)\*\*', r'\1', header_text)
                flow.append(Paragraph(header_text, subsection_style))
                continue
            
            # Handle main headers (#)
            if line.startswith("#"):
                header_text = line[1:].strip()
                # Remove markdown bold if present
                header_text = re.sub(r'\*\*(.+?)\*\*', r'\1', header_text)
                flow.append(Paragraph(header_text, section_style))
                continue
            
            # Regular paragraph - handle bold text
            para_text = line
            # Convert markdown bold to HTML
            para_text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', para_text)
            # Handle italic
            para_text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', para_text)
            flow.append(Paragraph(para_text, body_style))
        
        # Close any remaining list
        if in_list and current_list_items:
            flow.append(ListFlowable(current_list_items, bulletType='bullet'))

        doc.build(flow)
        return f.name

