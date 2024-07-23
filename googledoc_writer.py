from typing import Any, Type
from pydantic import BaseModel, Field
from superagi.tools.base_tool import BaseTool
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account

class GoogleDocArgs(BaseModel):
    document_id: str = Field(..., description="ID of the Google Doc to read and write.")
    prompt: str = Field(..., description="Prompt to process the content of the Google Doc.")

class GoogleDocWriterTool(BaseTool):
    name: str = "Google Doc Writer Tool"
    args_schema: Type[BaseModel] = GoogleDocArgs
    description: str = "Tool to read and write content in a Google Doc file."

    def read_doc(self, elements):
        text = ''
        for value in elements:
            if 'paragraph' in value:
                elements = value.get('paragraph').get('elements')
                for elem in elements:
                    text_run = elem.get('textRun')
                    if text_run:
                        text += text_run.get('content')
        return text

    def process_content(self, content: str, prompt: str) -> str:
        processed_content = content + "\n\n" + prompt
        return processed_content

    def write_doc(self, service, document_id: str, content: str):
        requests = [
            {
                'insertText': {
                    'location': {
                        'index': 1,  
                    },
                    'text': content
                }
            }
        ]
        result = service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()
        return result

    def _execute(self, document_id: str, prompt: str) -> str:
        try:
            SERVICE_ACCOUNT_FILE = { "type": "service_account", "project_id": "spatial-thinker-404111", "private_key_id": "27b1c4ecfbbd6e6d80d327d17191f1e89a0e717e", "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDIebot88jQyljR\n/DiPj47AkJ2DhF49bzt987xNJF0KT7PJMZtw+nh6vWG1xjhM1ulyYVjy7I3w9kgm\nr7rQpMgNxDVynKLWCmbHYZpscDAM56CaNDstkqOqtFAPRTXyq1QPHmMUYA8Sy1JC\n5/UlW5H5D9abIppqEbt74YTPIpmm70u9Hw5WTDA79zlPFIYdSywFNSGOU7H1j1B/\njRTANtiCJpCNGMi0P7MnFPC3jVGBkybxp4KpzdCaR7DoUi1agrFkN1In0oH4WxOb\nSrjsXL4+gXRkJ42O+J5qsbj8oAdRqqcvrGOCCpo8ArSo2/3eSAgPhOph1u53G2Xx\nsefUPN1LAgMBAAECggEAMTNOsgBmhHdknQRdjT4aNsBHKAPQbRtjamHrELOf8evl\nn7cBAxU1hEn+NPJU1ubXnC6v+c58d2q6AmSWYKZQQrCovVwbypP67WvSzlIqOMCP\n9chjzadza22dSGIf/1J06tD2WAXLLT2hDrKGw4hZptpwPNqdMvLvJFQQmBVRyFn6\n4osEq4xG0My+dNzy8MUAf7x3iSXvP4ynAZz0WDFsZJsyOBxJhGTY9j9cydUz+Q6Q\n+Dxb8GOwk5Paf1srBtcBmhUdAHR76wDsxvjlX796GD47mUAsx6RNHYuLR/utDbyr\ncick25nqXAKCIvFO8ZZH6qbWnnajmBwQGTYf+UicgQKBgQDrE1OqETyH5lNFhlb5\nRL4aL0YxRapy+rIKPXD/YY3goGMF2vPJ/NAa3bVx2r7bWmIS/1BX7J62kDdKyC9y\nRNA2k6WtiJxyWFVyIm//4VP0kagkSVEQsx/HZFQ6roi0Ui82G73TPWsjDVJ98X1Y\nNHKyD7bzCq6uLmcR3oQK9/fokQKBgQDaUfgY+dtZsLCBmxn++KO26MNW0tsnVhlV\nkM0bVgl56zFiR3boKwPqHIwTsaxO1dmh8LpKr/KKSy/xsYWQ16eFryozZjTou8RQ\nLCyXatZ2Z6OU30ATr5UGG67ICZp1i8Yqnl0aYQmQroPuj1Uxzy+GwJqx7I+MQdV+\nte/lp9z2GwKBgQDJ7N0WHh43wnJPK1l0X0dIqMkLtAL5Jz1eLG7u//ZmOH823WBC\nZkbAfSfJ+BOvypCqLuPt0tR2j6TfONwAtPmBmAxd5xYz5ornMouwafa7A49CNDRN\nOwCWPylXCutksZ/aQ7QoSv7Hqj7s7k40QUEwkO0fElMATd29bL1RyrUJ8QKBgClA\nOa+GblLJFuC2TLgnhM+HtXkPSEdrdkf7nzWeERZPQTp/pFED565xjGogNR2EPKXj\nlV+NVTeaM0nosAMJLGcPDNs/YZnj+Jjpb9eAYVtoA7maYUIW+AJ6cpDrd5rkOSJO\nX+sfEK6cuuL1hDRwIFvGwrQBrbHjspJJkDWFfTOnAoGAFzdqA3BIM7Rfhpqpp4j5\nTohii5DdQ5WWLIrK15cKq+L9kSXi11EFBxiYavS2lkWxoSEoT1VVsQP4PVtthjJ9\nlsmKObGtu38IAVpupVvUBWMTZK5wdzYbKFV8FYgBAgDxEmfAl1xI/cfo1F2Pt1a6\nlD62+ldxxoV0xuVdrURwjfc=\n-----END PRIVATE KEY-----\n", "client_email": "hitiksha@spatial-thinker-404111.iam.gserviceaccount.com","client_id": "110599327920595761650","auth_uri": "https://accounts.google.com/o/oauth2/auth","token_uri": "https://oauth2.googleapis.com/token","auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs","client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/hitiksha%40spatial-thinker-404111.iam.gserviceaccount.com","universe_domain": "googleapis.com" }  
            SCOPES = ['https://www.googleapis.com/auth/documents']

            credentials = service_account.Credentials.from_service_account_info(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
            service = build('docs', 'v1', credentials=credentials)
            document = service.documents().get(documentId=document_id).execute()
            content = document.get('body').get('content')

            doc_text = self.read_doc(content)
            processed_text = self.process_content(doc_text, prompt)
            self.write_doc(service, document_id, processed_text)

            return "Document updated successfully."
        except Exception as err:
            return f"Error: {err}"
