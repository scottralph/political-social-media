import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Open the Google Sheet found here:
# https://docs.google.com/spreadsheets/d/1LbE5qJswHY45yNLoZesaipFHkTgkDcaqtoTbUrd9fdY/edit?usp=sharing
# Enabled Google Drive API, and Google sheets API
CREDENTIALS_FILE = '/home/scott/Documents/credentials/scott-ralph-politics-457fe68ac9fd.json'
SHEET_NAME = 'U.S. House of Representatives Social Media'


def twitter_name_from_handle(handle):
    stripped = handle.strip()
    if stripped.startswith('@'):
        return stripped[1:]
    return None


class LegislatorSocialMediaSource:

    def __init__(self, credentials_file, sheet_name):
        self.credentials_file = credentials_file
        self.sheet_name = sheet_name
        self.client = None
        self.sheet = None
        self.sheet_values = None

    def authorize(self):
        scope = ['http://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(self.credentials_file, scope)
        self.client = gspread.authorize(credentials)
        self.sheet = self.client.open(self.sheet_name).sheet1
        self.sheet_values = self.sheet.get_all_values()

    def get_legislators(self):
        iter_sheet = iter(self.sheet_values)
        # Skip the header
        next(iter_sheet)
        values = [{'state': x[0], 'name': x[1], 'twitter': twitter_name_from_handle(x[2])} for x in iter_sheet]
        pass
        return values


if __name__ == "__main__":
    handles = LegislatorSocialMediaSource(CREDENTIALS_FILE, SHEET_NAME)
    handles.authorize()
    x = handles.get_legislators()
    pass
