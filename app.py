import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os

visited = set()

def scrape_website(url):
    if url in visited:
        return ""
    visited.add(url)

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        text = soup.get_text(separator='\n', strip=True)
        report = f"\n\n---\nURL: {url}\n---\n{text}"

        # Find subpage links
        links = soup.find_all('a', href=True)
        for link in links:
            full_url = urljoin(url, link['href'])
            if url in full_url:  # Stay within domain
                report += scrape_website(full_url)

        return report
    except Exception as e:
        return f"\nError scraping {url}: {str(e)}"

st.title("🌐 Web Scraper App")

url = st.text_input("Enter a website URL to scrape")

if st.button("Scrape"):
    if url:
        report = scrape_website(url)

        with open("scrape_report.txt", "w", encoding="utf-8") as f:
            f.write(report)

        st.success("Scraping Complete ✅")
        st.download_button("Download Report", data=report, file_name="scrape_report.txt")
    else:
        st.warning("Please enter a valid URL.")
