"""
Google Sheets logging utility - adapted from Streamlit version
Logs to existing "Search_Log" sheet to preserve old data
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
        
        # Use the same sheet names as the old implementation
        try:
            # Resource Finder logs to "Search_Log" (existing sheet with old data)
            _search_sheet = _sheets_client.open("Search_Log").sheet1
            print("✅ Connected to existing Search_Log sheet")
        except gspread.SpreadsheetNotFound:
            print("⚠️  Google Sheet 'Search_Log' not found. Please create it and share with service account.")
            return False
        
        # Try to find or create Perioperative log sheet
        try:
            perioperative_spreadsheet = _sheets_client.open("Search_Log")
            # Try to get a second sheet for perioperative, or use sheet1 if only one exists
            all_sheets = perioperative_spreadsheet.worksheets()
            if len(all_sheets) > 1:
                _perioperative_sheet = all_sheets[1]  # Use second sheet/tab
            else:
                # Create a new sheet/tab for perioperative logs
                _perioperative_sheet = perioperative_spreadsheet.add_worksheet(
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
    if not LOGGING_ENABLED or not _search_sheet:
        return False
    
    try:
        # Same format as old Streamlit code: timestamp, zip_code, category
        # Adding language as 4th column for new data
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        _search_sheet.append_row([timestamp, zip_code, category, language])
        return True
    except Exception as e:
        print(f"⚠️  Error logging resource search: {e}")
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
