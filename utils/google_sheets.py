"""
Google Sheets logging utility - adapted from Streamlit version.

Important:
- Opening spreadsheets by *name* is ambiguous if there are multiple files with the same title.
- Prefer setting GOOGLE_SHEET_ID (spreadsheet ID from the URL) so logs always land in the correct sheet.
"""
import os
import json
from datetime import datetime

# Try to import Google Sheets dependencies
try:
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
    SHEETS_AVAILABLE = True
except ImportError:
    SHEETS_AVAILABLE = False

LOGGING_ENABLED = False
_sheets_client = None
_search_sheet = None
_perioperative_sheet = None


def initialize_sheets():
    """Initialize Google Sheets client if credentials are available"""
    global LOGGING_ENABLED, _sheets_client, _search_sheet, _perioperative_sheet
    
    if not SHEETS_AVAILABLE:
        return False
    
    try:
        # Get Google Service Account JSON from environment variable
        google_creds_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
        
        if not google_creds_json:
            print("⚠️  GOOGLE_SERVICE_ACCOUNT_JSON not set. Logging to Google Sheets disabled.")
            return False
        
        # Parse the JSON string (same format as Streamlit secrets)
        try:
            creds_dict = json.loads(google_creds_json)
        except json.JSONDecodeError:
            # If it's already a dict string, try eval (for backwards compatibility)
            try:
                creds_dict = eval(google_creds_json)
            except:
                print("⚠️  Invalid GOOGLE_SERVICE_ACCOUNT_JSON format. Logging disabled.")
                return False
        
        # Authenticate using the same method as old Streamlit code
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        _sheets_client = gspread.authorize(creds)
        
        # Open the spreadsheet
        # Prefer an explicit spreadsheet ID to avoid ambiguity when multiple files share the same name.
        spreadsheet_id = os.getenv("GOOGLE_SHEET_ID")
        spreadsheet_name = os.getenv("GOOGLE_SHEET_NAME", "Search_Log")

        try:
            if spreadsheet_id:
                spreadsheet = _sheets_client.open_by_key(spreadsheet_id)
                print(f"✅ Connected to Google Sheet by ID: {spreadsheet_id}")
            else:
                spreadsheet = _sheets_client.open(spreadsheet_name)
                print(f"✅ Connected to Google Sheet by name: {spreadsheet_name}")

            # Resource Finder logs to the first tab (same behavior as old implementation)
            _search_sheet = spreadsheet.sheet1
        except gspread.SpreadsheetNotFound:
            print(f"⚠️  Google Sheet not found (name={spreadsheet_name}).")
            print("⚠️  Tip: set GOOGLE_SHEET_ID to the spreadsheet ID from the URL to avoid name collisions.")
            return False
        
        # Try to find or create Perioperative log tab in the same spreadsheet
        try:
            all_sheets = spreadsheet.worksheets()
            if len(all_sheets) > 1:
                _perioperative_sheet = all_sheets[1]  # Use second sheet/tab
            else:
                # Create a new sheet/tab for perioperative logs
                _perioperative_sheet = spreadsheet.add_worksheet(
                    title="Perioperative_Log",
                    rows=1000,
                    cols=10
                )
                # Add header row
                _perioperative_sheet.append_row([
                    "Timestamp", "Instruction Type", "Language", "Reading Level", "Procedure"
                ])
        except Exception as e:
            print(f"⚠️  Could not set up Perioperative log sheet: {e}")
            _perioperative_sheet = None
        
        LOGGING_ENABLED = True
        print("✅ Google Sheets logging initialized successfully")
        return True
        
    except Exception as e:
        print(f"⚠️  Error initializing Google Sheets: {e}. Logging disabled.")
        return False


def log_resource_search(zip_code: str, category: str, language: str = "English"):
    """Log a resource finder search to Google Sheets (same format as old implementation)"""
    if not LOGGING_ENABLED:
        print("⚠️  Logging disabled - GOOGLE_SERVICE_ACCOUNT_JSON not set")
        return False
    
    if not _search_sheet:
        print("⚠️  Search sheet not initialized")
        return False
    
    try:
        # Same format as old Streamlit code: timestamp, zip_code, category
        # Adding language as 4th column for new data
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        _search_sheet.append_row([timestamp, zip_code, category, language])
        print(f"✅ Logged search: {zip_code}, {category}, {language}")
        return True
    except Exception as e:
        print(f"⚠️  Error logging resource search: {e}")
        import traceback
        traceback.print_exc()
        return False


def log_perioperative_usage(
    instruction_type: str,
    language: str,
    reading_level: str,
    procedure: str
):
    """Log a perioperative translator usage to Google Sheets"""
    if not LOGGING_ENABLED or not _perioperative_sheet:
        return False
    
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        _perioperative_sheet.append_row([
            timestamp,
            instruction_type,
            language,
            reading_level,
            procedure
        ])
        return True
    except Exception as e:
        print(f"⚠️  Error logging perioperative usage: {e}")
        return False


# Initialize on module import
if SHEETS_AVAILABLE:
    initialize_sheets()
