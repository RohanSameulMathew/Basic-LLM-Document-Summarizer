'''
The purpose of this code is to be able to use Groq's LLM model to generate responses to
1. text files
2. html files
3. pdf files
4. images
'''
### Time to import!

import os
from groq import Groq # AI Model
import groq
from dotenv import load_dotenv
import argparse
import sys, pathlib, pymupdf
import base64
import mimetypes
import requests
from bs4 import BeautifulSoup

###### CALLING API KEY
load_dotenv() # Allows protection of API key by calling it from environment
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"), 
)
######

'''
1. TEXT FILES

We start by creating a function to analyse text. This works with both pdf and .txt files. This takes the text as input and returns the LLM response.
'''
def llm(text):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                #prompt is content
                "content": text,
            }
        ],
        model="meta-llama/llama-4-maverick-17b-128e-instruct",
    )
    return chat_completion.choices[0].message.content

'''
2. IMAGE FILES

This function allows the llm to analyse image files
'''

def llm_image(filename):
    # Check if local file exists
    if os.path.exists(filename):
        mime_type, _ = mimetypes.guess_type(filename)
        if not mime_type or not mime_type.startswith("image/"):
            raise ValueError("Unsupported or unrecognized image file type")

        with open(filename, "rb") as img_file:
            image_bytes = img_file.read()
        image_b64 = base64.b64encode(image_bytes).decode("utf-8")
        image_url = f"data:{mime_type};base64,{image_b64}"
    else:
        # Assume it's a remote URL
        image_url = filename

    # Create the LLM call
    completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What's in this image?"},
                    {"type": "image_url", "image_url": {"url": image_url}},
                ]
            }
        ],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,
    )
    return completion.choices[0].message.content


'''
This allows the llm to split the text into chunks and then analyse each chunk
'''
def split_text(text, max_chunk_size=1000):
    '''
    >>> split_text('abcdefg', max_chunk_size=2)
    ['ab', 'cd', 'ef', 'g']
    '''
    accumulator = []
    while len(text) > 0:
        accumulator.append(text[:max_chunk_size])
        text=text[max_chunk_size:]
    return accumulator


### HERE IS WHERE YOU CAN INPUT THE PROMPT
def summarize_text(text):
    prompt = f'''
    Summarize in two sentences or less.
    {text}
    '''
    try:
        output = llm(prompt)
        return output.split('/n')[-1]
    
    except groq.APIStatusError:
        chunks = split_text(text, 10000)
        print('len(chunks)= ', len(chunks))
        accumulator=[]
        output=[]
        for i, chunk in enumerate(chunks):
                print('i= ', i)
                summary = summarize_text(chunk)
                accumulator.append(summary)
                output.append(summary)

        summarized_text = ' '.join(accumulator)
        summarized_text = summarize_text(summary)
        return summarized_text
    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='docsum',
        description='summarize the input document',
    )
    parser.add_argument('filename')
    args = parser.parse_args()

    ext = pathlib.Path(args.filename).suffix.lower()

    if ext in [".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp"]:
        print(llm_image(args.filename))

    elif ext == ".pdf":
        with pymupdf.open(args.filename) as doc:
            text = chr(12).join([page.get_text() for page in doc])
            print(summarize_text(text))

    elif ext in [".html", ".htm"]:
        with open(args.filename, 'r') as fin:
            html = fin.read()
            soup = BeautifulSoup(html, features='lxml')
            text = soup.text
            print(text)
            print(summarize_text(text))

    elif ext == ".txt":
        with open(args.filename, 'r') as fin:
            text = fin.read()
            print(summarize_text(text))

    elif args.filename.startswith("http://") or args.filename.startswith("https://"):
        try:
            response = requests.get(args.filename, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "lxml")
            text = soup.get_text(separator="\n", strip=True)
            print(summarize_text(text))
        except Exception as e:
            print(f"Failed to fetch or process the URL: {e}")
    else:
        print(f"Unsupported file type: {ext}")

