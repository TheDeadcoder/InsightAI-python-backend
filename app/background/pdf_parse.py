import os
from typing import List, Dict
import json
from llama_parse import LlamaParse
from llama_index.core.schema import TextNode
from app.core.config import settings
import openai
import requests
from app.core.openai import openaiClient
from app.helpers.qdrant_functions import make_collection, upload_to_qdrant,delete_points_by_uuid
from app.core.supabase import supabase

def get_text_nodes(json_list: List[dict]) -> List[TextNode]:
    """Convert JSON list to a list of TextNode objects."""
    text_nodes = []
    for idx, page in enumerate(json_list):
        text_node = TextNode(text=page["md"], metadata={"page": page["page"]})
        text_nodes.append(text_node)
    return text_nodes

def update_file_status(file_id: str, status: str):
    response = supabase.table("files").update({"status": status}).eq("id", file_id).execute()


def get_llama_cloud_keys() -> List[str]:
    """Retrieve all LlamaCloud API keys from settings."""
    return [
        settings.LLAMACLOUD_API_1, settings.LLAMACLOUD_API_2, settings.LLAMACLOUD_API_3,
        settings.LLAMACLOUD_API_4, settings.LLAMACLOUD_API_5, settings.LLAMACLOUD_API_6,
        settings.LLAMACLOUD_API_7, settings.LLAMACLOUD_API_8, settings.LLAMACLOUD_API_9,
        settings.LLAMACLOUD_API_10, settings.LLAMACLOUD_API_11, settings.LLAMACLOUD_API_12,
        settings.LLAMACLOUD_API_13, settings.LLAMACLOUD_API_14, settings.LLAMACLOUD_API_15,
        settings.LLAMACLOUD_API_16, settings.LLAMACLOUD_API_17, settings.LLAMACLOUD_API_18,
        settings.LLAMACLOUD_API_19, settings.LLAMACLOUD_API_20
    ]

def llama_parse_pdf(pdf_path: str) -> List[Dict]:
    """Parse a PDF file using LlamaParse and return extracted text."""
    parsing_instruction = '''
    You will be given a PDF which contains banking information. You have to parse and return it in markdown format.

    **Important instructions:**
    - Output any math equation in LaTeX markdown (between $$).
    - For images, do **not** return URLs or base64 data. Instead, provide a **detailed description** of the image content, explaining what the image represents and how it is relevant to the document content.
    - Preserve the original formatting, headings, and lists as much as possible.
    '''

    llama_keys = get_llama_cloud_keys()

    for key_index, llamacloud_key in enumerate(llama_keys):

        retry_attempts = 3
        for attempt in range(retry_attempts):
            try:
                os.environ["LLAMA_CLOUD_API_KEY"] = llamacloud_key

                parser = LlamaParse(
                    result_type="markdown",
                    use_vendor_multimodal_model=True,
                    vendor_multimodal_model="openai-gpt-4o-mini",
                    invalidate_cache=True,
                    vendor_multimodal_api_key=settings.OPENAI_API_KEY,
                    parsing_instruction=parsing_instruction
                )
                print(f"Using LlamaCloud API Key {key_index + 1}, Attempt {attempt + 1}")
                json_objs = parser.get_json_result(pdf_path)

                # Validate parsing output
                if not json_objs or "pages" not in json_objs[0]:
                    raise ValueError(f"Failed to parse the file: {pdf_path}")

                return json_objs[0]["pages"]

            except Exception as e:
                print(f"Error with LlamaCloud API Key {key_index + 1}, Attempt {attempt + 1}: {str(e)}")

                # If this was the last retry attempt, move on to the next key
                if attempt == retry_attempts - 1:
                    print(f"Moving on to the next API key after {retry_attempts} failed attempts.")
                    break

    # If all keys fail
    raise Exception("All LlamaCloud API keys failed after 3 retries each.")

def generate_summary(page_content: str) -> str:
    """Generate a summary of the extracted text using OpenAI GPT."""
    prompt = f"Summarize the following content from a file:\n\n{page_content}\n\nBriefly summarize this page:"

    # print(page_content)
    
    response = openaiClient.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
        ],
        )
    raw_response = response.choices[0].message.content
    return raw_response

def save_summary_locally(file_id: str, summaries: List[Dict], user_id: str, collection_name: str):
    output_dir = f"./outputs/{user_id}/{collection_name}/"
    os.makedirs(output_dir, exist_ok=True)

    summary_file_path = os.path.join(output_dir, f"{file_id}_summary.json")
    with open(summary_file_path, 'w') as summary_file:
        json.dump(summaries, summary_file, indent=4)

    print(f"Summaries saved to: {summary_file_path}")



def process_pdf_and_generate_summaries(file_url: str, file_id: str, user_id: str, collection_name: str):
    file_path = f"./downloads/{file_id}.pdf"
    try:
        response = requests.get(file_url)
        response.raise_for_status()
        with open(file_path, 'wb') as file:
            file.write(response.content)

        # Parse the PDF
        pages = llama_parse_pdf(file_path)
        summaries = []
        for page in pages:
            page_text = page["md"]
            page_summary = generate_summary(page_text)
            summaries.append({
                "page_number": page["page"],
                "summary": page_summary,
                "content": page_text  # Optionally save the full page content
            })

        # Save the summaries locally
        full_collection_name = f"{user_id}_{collection_name}"

        make_collection(user_id,collection_name)
        for summary in summaries:
            upload_to_qdrant(file_id,file_url,summary["page_number"],summary["content"],summary["summary"],full_collection_name)

        update_file_status(file_id, "Completed")

    except Exception as e:
        print(f"Error while processing the file: {str(e)}")
        full_collection_name = f"{user_id}_{collection_name}"
        delete_points_by_uuid(full_collection_name, file_id)
        update_file_status(file_id, "Failed")
    finally:
        # Cleanup: Remove the downloaded file after processing
        if os.path.exists(file_path):
            os.remove(file_path)
