from abc import ABC
from typing import List
from superagi.tools.base_tool import BaseTool, BaseToolkit, ToolConfiguration
from superagi.tools.google_docs.googledoc_reader import GoogleDocReaderTool
from superagi.types.key_type import ToolConfigKeyType
from superagi.models.tool_config import ToolConfig


class GoogleDocToolkit(BaseToolkit, ABC):
    name: str = "Google Doc Toolkit"
    description: str = "Toolkit containing tools for working with google docs"

    def get_tools(self) -> List[BaseTool]:
        return [
            GoogleDocReaderTool()
        ]

    def get_env_keys(self) -> List[ToolConfiguration]:
        return [
            ToolConfiguration(key="SERVICE_ACCOUNT_DETAILS", key_type=ToolConfigKeyType.STRING, is_required= True, is_secret = False)
            
        ]
