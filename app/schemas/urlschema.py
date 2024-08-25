from pydantic import BaseModel

# Pydantic model to validate the incoming URL data
class URLRequest(BaseModel):
    url: str