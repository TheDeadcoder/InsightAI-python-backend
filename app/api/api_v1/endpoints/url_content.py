from fastapi import FastAPI, HTTPException
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File as FastAPIFile, Form
from bs4 import BeautifulSoup
import requests
from app.schemas.urlschema import URLRequest
from app.helpers.openai_functions import clean_content

router = APIRouter()

@router.post("/")
async def extract_text(request: URLRequest):
    url = request.url

    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error if the request fails

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract the text content from the page
        text_content = soup.get_text(separator="\n", strip=True)

        ret_content = clean_content(request.url, text_content)

        # Return the text content
        return {"text_content": ret_content}

    except requests.exceptions.RequestException as e:
        # If there is any request-related error, return a 400 status code
        raise HTTPException(status_code=400, detail=f"Failed to retrieve content: {str(e)}")

