# RAG using OpenAI API

This repository offers a hands-on tutorial for developing Retrieval-Augmented Generation (RAG) systems utilizing OpenAI API, with PDF documents serving as the primary data source. It guides developers through the entire process — enabling the efficient implementation of RAG-based solutions.

## Prerequisites

- An OpenAI API Key
- PDF documents to serve as the knowledge base

## Installation

1. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

2. Add your OpenAI API key to the `.env` file in the same directory as `main.py`:
    ```
    OPENAI_API_KEY=your_openai_api_key_here
    ```

## Setting Up

1. Place your PDF documents in `Upload` folder in the same directory as `main.py`.
2. The environment variables will be loaded from the `.env` file, and the script will automatically interact with the OpenAI API.
**※ The .env file can be downloaded from the link below.**
https://drive.google.com/file/d/1HjwRNZxBVN4xz8rFZdH8LgToXDezjh_q/view?usp=sharing


## Practice

- Ensure PDFs are well-structured and relevant to the domain for improved performance.
- Use meaningful filenames and metadata for better file management.
- Tune parameters like `temperature` and `top_p` for the assistant based on your specific use case.
- Utilize query augmentation and context to improve the retrieval quality in RAG systems.


