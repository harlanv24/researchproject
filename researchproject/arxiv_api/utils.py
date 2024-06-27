import requests
import xml.etree.ElementTree as ET
import imgkit
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def fetch_arxiv_data(query):
    url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=6"
    response = requests.get(url)
    return response.text


def parse_arxiv_response(xml_response):
    root = ET.fromstring(xml_response)
    entries = []
    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        entry_data = {
            'id': entry.find('{http://www.w3.org/2005/Atom}id').text,
            'title': entry.find('{http://www.w3.org/2005/Atom}title').text,
            'summary': entry.find('{http://www.w3.org/2005/Atom}summary').text,
            'link': entry.find("{http://www.w3.org/2005/Atom}link[@rel='alternate']").attrib['href'],
            'pdf_link': entry.find("{http://www.w3.org/2005/Atom}link[@title='pdf']").attrib['href'],
            'authors': [author.find('{http://www.w3.org/2005/Atom}name').text for author in entry.findall('{http://www.w3.org/2005/Atom}author')]
        }
        entries.append(entry_data)
    print(entries)
    return entries

def create_snapshot(title, summary, pdf_link, index):
    try:
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .container {{ max-width: 800px; margin: 0 auto; }}
                .title {{ font-size: 24px; font-weight: bold; }}
                .summary {{ margin-top: 20px; }}
                .link {{ margin-top: 20px; }}
                img {{ max-width: 100%; height: auto; }} /* Ensure image does not overflow the container */
            </style>
        </head>
        <body>
            <div class="container">
                <div class="title">{title}</div>
                <div class="summary">{summary}</div>
            </div>
        </body>
        </html>
        """
        # Ensure the media directory exists
        output_dir = os.path.join(BASE_DIR, 'snapshots')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        options = {
            'width': 800,  # Set the width to match the max-width in the CSS
        }
        img_path = os.path.join(output_dir, f"snapshot{index}.jpg")
        imgkit.from_string(html_content, img_path, options=options)
        print("Created snapshot at:", img_path)
        return img_path
    except Exception as e:
        print("Error creating snapshot:", e)
        return None