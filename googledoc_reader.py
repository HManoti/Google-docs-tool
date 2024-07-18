from google.oauth2 import service_account
from typing import Any, Type
from pydantic import BaseModel, Field
from superagi.tools.base_tool import BaseTool
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.discovery import build


class GoogleDocArgs(BaseModel):
    document_id: str = Field(..., description= "1Oai5kbMmP_DCCv7mqmZW7e_xR9tt8Qw7bpgwp-PodZY")

class GoogleDocReaderTool(BaseTool):
    name: str = "Google Doc Reader Tool"
    args_schema: Type[BaseModel] = GoogleDocArgs
    description: str = "Tool to read the content of a Google Doc file."
    
    def read_doc(self,elements):
        text = ''
        for value in elements:
            if 'paragraph' in value:
                elements = value.get('paragraph').get('elements')
                for elem in elements:
                    text_run = elem.get('textRun')
                    if text_run:
                        text += text_run.get('content')
        return text


    def _execute(self, document_id: str) -> str:
        try:
            SERVICE_ACCOUNT_FILE = r'C:\Users\HP\Downloads\client_secret_213184423882-fhal1gs6h9uth21fmr04nm9i908o4tf0.apps.googleusercontent.com.json'
            document_id = document_id
            SCOPES = ['https://www.googleapis.com/auth/documents.readonly']

            credentials = service_account.Credentials.from_service_account_info(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
            service = build('docs', 'v1', credentials=credentials)
            document = service.documents().get(documentId=document_id).execute()
            content = document.get('body').get('content')

            doc_text = self.read_doc(content)

            return doc_text
        except Exception as err:
            return f"Error:{err}"

    