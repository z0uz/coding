"""This Python script performs several tasks related to web scraping, subdomain enumeration,
directory scanning, and extracting phone numbers from HTML content."""

import requests
from bs4 import BeautifulSoup
import re
import subprocess
import os

def fetch_metadata(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve webpage: {e}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    metadata = {}

    # Extract metadata
    title = soup.find('title')
    if title:
        metadata['title'] = title.text.strip()
    
    description = soup.find('meta', attrs={'name': 'description'})
    if description:
        metadata['description'] = description['content'].strip()
    
    keywords = soup.find('meta', attrs={'name': 'keywords'})
    if keywords:
        metadata['keywords'] = keywords['content'].strip()

    # Extract headers
    headers = {}
    for tag in ['h1', 'h2', 'h3']:
        headers[tag] = [header.text.strip() for header in soup.find_all(tag)]

    # Extract paragraphs
    paragraphs = [p.text.strip() for p in soup.find_all('p')]

    # Extract links
    links = [{'text': link.text.strip(), 'url': link['href']} for link in soup.find_all('a', href=True)]

    # Extract images
    images = [{'alt': img.get('alt', '').strip(), 'url': img['src']} for img in soup.find_all('img', src=True)]

    metadata['headers'] = headers
    metadata['paragraphs'] = paragraphs
    metadata['links'] = links
    metadata['images'] = images

    return metadata

def extract_phone_numbers(html_content):
    # Using regular expressions to find phone numbers
    phone_pattern = re.compile(r'(\+\d{1,2}\s*)?(\(\d{3}\)|\d{3})[\s.-]?\d{3}[\s.-]?\d{4}')
    phone_numbers = phone_pattern.findall(html_content)
    return phone_numbers

def find_subdomains(domain):
    subdomains = []

    # Using sublist3r tool to find subdomains
    result = subprocess.run(['sublist3r', '-d', domain], capture_output=True, text=True)
    if result.returncode == 0:
        subdomains = result.stdout.splitlines()

    return subdomains

def scan_for_folders(url):
    folders = []

    # Using dirsearch tool to scan for folders
    result = subprocess.run(['dirsearch', '-u', url, '-e', '*', '-x', '400,403,404'], capture_output=True, text=True)
    if result.returncode == 0:
        output_lines = result.stdout.splitlines()
        for line in output_lines:
            if line.startswith('[+]'):
                folder = line.split()[-1]
                folders.append(folder)

    return folders

def main():
    url = input("Please enter the website URL: ")
    metadata = fetch_metadata(url)
    if metadata is None:
        print("Failed to fetch website data.")
        return

    phone_numbers = extract_phone_numbers(metadata.get('html_content', ''))
    subdomains = find_subdomains(url)
    folders = scan_for_folders(url)

    print("Website Metadata:")
    for key, value in metadata.items():
        if key in ['headers', 'paragraphs', 'links', 'images']:
            print(f"{key.capitalize()}:")
            for item in value:
                if isinstance(item, dict):
                    print(f"- {item['text']} ({item['url']})")
                else:
                    print(f"- {item}")
        else:
            print(f"{key.capitalize()}: {value}")

    print("\nPhone Numbers:")
    for phone_number in phone_numbers:
        print(phone_number)

    print("\nSubdomains:")
    for subdomain in subdomains:
        print(subdomain)

    print("\nFolders:")
    for folder in folders:
        print(folder)

if __name__ == "__main__":
    main()
