#
# fetch et analyse du contenu d'Outscale
#
from urllib.parse import urlparse, urlunparse, urljoin
from concurrent.futures import ThreadPoolExecutor

import bs4
import os
import re

ROOT_DIRECTORY = "./docs.outscale.com/en/userguide"

# Set the batch size (number of files to process in each batch)
batch_size = 100

def _cleaned_link(url, link):
    link = urljoin(url, link["href"])
    return link

def _cleaned_image(url, image):
    image = urljoin(url, image["src"])
    return image

def _extract_html_docs(url, html):
    print(f"Extracting docs HTML from {url}")
    soup = bs4.BeautifulSoup(html, "html.parser")

    title = ""
    if soup.find("h1") is not None:
        title = soup.find("h1").text.strip()

    parsed = urlparse(url)
    article = soup.find("article", class_="doc")
    cleaned_links = []
    sections = []

    if article is not None:
        links = article.find_all("a")
        for link in links:
            if link.get("href") != None and not link.get("href").startswith("#"):
                cleaned_links.append(_cleaned_link(url, link))
        for section in soup.select("#preamble, .sect1"):
            header = section.find("h2")
            section_links = [
                _cleaned_link(url, link)
                for link in section.find_all("a")
                if link.text != ""
            ]
            anchor = section.find("a", class_="anchor")
            section_url = urlunparse(
                (
                    parsed.scheme,
                    parsed.netloc,
                    parsed.path,
                    parsed.params,
                    parsed.query,
                    anchor.get("href").replace("#", "") if anchor else "preamble",
                )
            )

            code_blocks = []
            for pre in section.find_all("div", class_="listingblock"):
                language = pre.find("code").get("data-lang")
                section_title = pre.find("div", class_="title")
                code = pre.find("code")

                if code:
                    code_blocks.append(
                        {
                            "language": language if language is not None else None,
                            "title": (
                                section_title.text.strip()
                                if section_title is not None
                                else None
                            ),
                            "code": code.text,
                        }
                    )
            sections.append(
                {
                    "url": section_url,
                    "title": header.text.strip() if header is not None else title,
                    "text": re.sub(r"\n+", "\n", section.text).strip(),
                    "anchor": anchor.get("href") if anchor else None,
                    "links": section_links,
                    "images": [
                        _cleaned_image(url, img) for img in section.find_all("img")
                    ],
                    "code": code_blocks,
                }
            )

    return {"url": url, "title": title, "links": cleaned_links, "sections": sections}

# Function to process a batch of files
def _process_batch(url, files):
    print(f"Processing batch {url} of {len(files)} files")
    batch_docs = []
    for file in files:
        with open(file, "rb") as f:
            batch_docs.append(
                _extract_html_docs(
                    f"{url}/{os.path.basename(file)}",
                    f.read().decode("utf-8", "ignore"),
                )
            )
    return batch_docs

def _files_to_process():
    print(f"Processing files in {ROOT_DIRECTORY}")
    # Get the list of files to process
    files_to_process = []
    for root, dirs, files in os.walk(ROOT_DIRECTORY):
        files_to_process.extend(
            [os.path.join(root, file) for file in files if file.lower().endswith(".html")]
        )
    return files_to_process

def process_sections_docs():
    _files = _files_to_process()
    print(f"processing sections HTML")
    print(f"Found {len(_files)} files to process")
    all_sections = []
    docs = []
    # Create a ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor() as executor:
        total_files = len(_files)
        processed_files = 0

        # Iterate through the files in batches
        for i in range(0, total_files, batch_size):
            batch = _files[i: i + batch_size]
            batch_docs = list(
                executor.map(
                    _process_batch, ["https://docs.outscale.com/en/userguide"], [batch]
                )
            )
            for batch_result in batch_docs:
                docs.extend(batch_result)
                processed_files += len(batch)
                print(f"Processed {processed_files} / {total_files} files")

    for doc in docs:
        for section in doc["sections"]:
            current_section = {
                "title": section["title"],
                "content": section["text"],
                "source": section["url"],
            }
            all_sections.append(current_section)

    return all_sections

