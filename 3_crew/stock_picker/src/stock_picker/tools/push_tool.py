from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os
import requests


class MyCustomToolInput(BaseModel):
    """A message to be sent to the user"""
    message: str = Field(..., description="Message to be sent to the user")

class PushNotificationTool(BaseTool):
    name: str = "Send a push notification"
    description: str = (
        "This tool is used to send push notifications to the user"
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, message: str) -> str:
        # Implementation goes here
        pushover_user = os.getenv("PUSHOVER_USER")
        pushover_token = os.getenv("PUSHOVER_TOKEN")
        pushover_url = "https://api.pushover.net/1/message.json"

        print(f"Push: {message}")
        payload = {"user" : pushover_user, "token" : pushover_token, "message" : message}
        requests.post(pushover_url, data=payload)
        return {"notification" : "ok"}
