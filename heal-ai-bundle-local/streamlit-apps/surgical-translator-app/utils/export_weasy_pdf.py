
from weasyprint import HTML, CSS
import uuid
import os

def export_instruction_to_pdf(text: str, title="Instructions") -> str:
    # Convert newlines and simple markers into HTML
    html_lines = []
    for line in text.split("\n"):
        line = line.strip()
        if line.startswith("**") and line.endswith("**"):
            html_lines.append(f"<h2>{line.strip('**').strip()}</h2>")
        elif line.startswith("- "):
            html_lines.append(f"<li>{line[2:]}</li>")
        elif line == "":
            html_lines.append("<br>")
        else:
            html_lines.append(f"<p>{line}</p>")

    # Wrap in full HTML
    html_content = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: 'Noto Sans', sans-serif;
                font-size: 14px;
                line-height: 1.6;
                color: #1e1e1e;
                padding: 2rem;
            }}
            h2 {{
                color: #003366;
                margin-top: 1.5rem;
            }}
            li {{
                margin-left: 1.5rem;
            }}
        </style>
    </head>
    <body>
        <h1>{title}</h1>
        {''.join(html_lines)}
    </body>
    </html>
    """

    # Create temp file
    filename = f"/tmp/{uuid.uuid4().hex}.pdf"
    HTML(string=html_content).write_pdf(filename)
    return filename
