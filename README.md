# InsightAI Backend

![InsightAI Logo](https://dxpcgmtdvyvcxbaffqmt.supabase.co/storage/v1/object/public/demo/insightAI%20logo%20(2).png)

## Overview

Welcome to the backend of **InsightAI**, an application designed to revolutionize your banking experience. This backend is built using FastAPI, providing a robust and efficient structure for our application.

## Technologies Used

- **FastAPI**: A modern, fast (high-performance), web framework for building APIs with Python 3.6+.
- **LLAMAPARSE**: For document parsing 
- **Serper**: For Web-search
- **Qdrant**: For Vector Database
- **OpenAI**: As Ai model
- **Structured-output**: For structuring openai response
- **beautifulsoup4**: For scraping web content
- **Roboflow**: For generating embedding for image
- **Supabase**: Used for database hosting and authentication.

## Getting Started

### Making the Environment

To make a virtual environment, use the following command:

```bash
python3 -m venv .venv
```

Activate the virtual Environment:

```bash
source .venv/bin/activate
```

### Install the Requirements:

Install The requirements with the following command:

```bash
pip install -r requirements.txt
```

It may lag. So better add a timeout

```bash
pip install -r requirements.txt --timeout=1000
```

### Running the Backend

To run the backend server, use the following command:

```bash
uvicorn app.main:app --reload
```

The app will start:

```bash
http://127.0.0.1:8000/
```

Once the application is running, you can access the API documentation provided by Swagger at:

```bash
http://127.0.0.1:8000/docs
```

Here, you can explore and interact with the various API endpoints.

Changes will migrate automatically

## Endpoints
Endpoints are defined in api/api_v1/endpoints/

## Helper functions
Helper functions are defined in /helpers. Most **LLM Tasks** will be performed here

## Environment File
It will be provided **Privately**

## Deployment

The application is hosted in Render
- [Deployment](https://insightai-6hp4.onrender.com).
- [Deployment Docs](https://insightai-6hp4.onrender.com/docs).