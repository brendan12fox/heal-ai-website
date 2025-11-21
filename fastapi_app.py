from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv
import uvicorn
from utils.pdf_export import create_pdf_from_text

load_dotenv()

app = FastAPI()

# Templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# OpenAI client
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable must be set")
client = OpenAI(api_key=openai_api_key)

# Request models
class ResourceRequest(BaseModel):
    category: str
    zip_code: str
    language: str = "English"

class ResourcePDFRequest(BaseModel):
    category: str
    zip_code: str
    language: str
    result: str

class InstructionRequest(BaseModel):
    instruction_type: str
    language: str
    reading_level: str
    procedure: str

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/resource-finder", response_class=HTMLResponse)
async def resource_finder(request: Request):
    return templates.TemplateResponse("resource_finder.html", {"request": request})

@app.get("/perioperative", response_class=HTMLResponse)
async def perioperative(request: Request):
    return templates.TemplateResponse("perioperative.html", {"request": request})

@app.post("/api/find-resources")
async def find_resources(request: ResourceRequest):
    """Find community resources using OpenAI"""
    language_instruction = f"Translate the output into {request.language}." if request.language != "English" else "Present the output in English."
    
    prompt = f"""You are acting as a clinical social work assistant helping a healthcare provider identify free or low-cost hyperlocal community resources for vulnerable adults.

Return a list of 3 to 5 unique, verifiable services that provide assistance in the category of **{request.category}**, specifically located in **ZIP Code {request.zip_code}** (and surrounding neighborhoods if necessary).

Requirements:
- Only include local or regional nonprofits, public agencies, health systems, or government-run services.
- Each entry must include:
  • Service Name  
  • One-sentence description  
  • Contact Info: Address (with ZIP), phone (if available), website (if available)

Strict Guidelines:
- Avoid listing national hotlines or broad advice like "try local churches."
- Do not list duplicate organizations.
- If no services are found, return: "No appropriate services found."
- {language_instruction}

Present results as a clean numbered list or table, readable for both patients and care staff."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that finds local community resources."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )
        result = response.choices[0].message.content.strip()
        return JSONResponse({"success": True, "result": result})
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)

@app.post("/api/generate-instructions")
async def generate_instructions(request: InstructionRequest):
    """Generate perioperative instructions using OpenAI"""
    base_behavior = (
        "You are a medical communication expert. Your task is to translate clinical documents "
        "into plain language for patients with limited health literacy. Your tone should be clear, empathetic, and respectful. "
        "Avoid medical jargon unless defined simply. Use short sentences, bullet points, and bold section headers."
    )

    if request.instruction_type == "Post-Op":
        prompt = (
            f"{base_behavior} Rewrite the post-operative instructions for a {request.procedure}. "
            f"Translate the output into {request.language} at a {request.reading_level} reading level. "
            "Include the following sections: 1) Wound Care, 2) Pain Management, 3) Activity Restrictions, "
            "4) Diet, 5) When to Call the Doctor (Red Flag Symptoms), and 6) Follow-Up Instructions. "
            "Make the instructions actionable and easy to follow at home."
        )
    else:
        prompt = (
            f"{base_behavior} Write a simplified pre-operative surgical consent explanation for a {request.procedure}. "
            f"Translate the output into {request.language} at a {request.reading_level} reading level. "
            "Include the following sections: 1) What the procedure is, 2) Why it is needed, "
            "3) Risks and complications, 4) Benefits, 5) Alternatives (including doing nothing), "
            "6) Recovery expectations, and 7) Patient rights (right to ask questions and refuse). "
            "Use language a family member without medical training can understand."
        )

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a medical writer helping patients understand surgical instructions."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )
        result = response.choices[0].message.content.strip()
        return JSONResponse({"success": True, "result": result})
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)

@app.post("/api/generate-pdf")
async def generate_pdf(request: InstructionRequest):
    """Generate PDF from instructions"""
    base_behavior = (
        "You are a medical communication expert. Your task is to translate clinical documents "
        "into plain language for patients with limited health literacy. Your tone should be clear, empathetic, and respectful. "
        "Avoid medical jargon unless defined simply. Use short sentences, bullet points, and bold section headers."
    )

    if request.instruction_type == "Post-Op":
        prompt = (
            f"{base_behavior} Rewrite the post-operative instructions for a {request.procedure}. "
            f"Translate the output into {request.language} at a {request.reading_level} reading level. "
            "Include the following sections: 1) Wound Care, 2) Pain Management, 3) Activity Restrictions, "
            "4) Diet, 5) When to Call the Doctor (Red Flag Symptoms), and 6) Follow-Up Instructions. "
            "Make the instructions actionable and easy to follow at home."
        )
    else:
        prompt = (
            f"{base_behavior} Write a simplified pre-operative surgical consent explanation for a {request.procedure}. "
            f"Translate the output into {request.language} at a {request.reading_level} reading level. "
            "Include the following sections: 1) What the procedure is, 2) Why it is needed, "
            "3) Risks and complications, 4) Benefits, 5) Alternatives (including doing nothing), "
            "6) Recovery expectations, and 7) Patient rights (right to ask questions and refuse). "
            "Use language a family member without medical training can understand."
        )

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a medical writer helping patients understand surgical instructions."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )
        result = response.choices[0].message.content.strip()
        
        # Generate PDF
        title = f"{request.instruction_type} Instructions: {request.procedure}"
        pdf_path = create_pdf_from_text(result, title=title)
        
        # Return PDF file
        filename = f"{request.instruction_type.lower()}_{request.procedure.replace(' ', '_')}.pdf"
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=filename
        )
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)

@app.post("/api/generate-resource-pdf")
async def generate_resource_pdf(request: ResourcePDFRequest):
    """Generate PDF from resource finder results"""
    try:
        # Generate PDF from the resource results
        title = f"Community Resources: {request.category} - ZIP {request.zip_code}"
        pdf_path = create_pdf_from_text(request.result, title=title)
        
        # Return PDF file
        filename = f"resources_{request.category.replace(' ', '_')}_{request.zip_code}.pdf"
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=filename
        )
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8502)

