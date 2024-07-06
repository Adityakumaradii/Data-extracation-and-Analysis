import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract_article(url, url_id):
    try:
        # Fetch the webpage content
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the webpage content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the article title
        title = soup.find('title').get_text(strip=True)

        # Extract the main article content
        # This step depends on the specific structure of the website.
        # Here are some common tags to check for the main content:
        article_tags = ['article', 'div', 'section']
        article = None
        for tag in article_tags:
            article = soup.find(tag)
            if article:
                break

        if not article:
            print(f"Could not find the article content for URL: {url}")
            return

        # Extract text and clean it
        paragraphs = article.find_all('p')
        article_text = "\n".join(p.get_text(strip=True) for p in paragraphs)

        # Save the extracted content to a text file
        filename = f"{url_id}.txt"
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(f"{title}\n\n{article_text}")

        print(f"Article saved as {filename}")

    except requests.RequestException as e:
        print(f"Error fetching the URL: {url}\n{e}")

def main():
    # Read URLs and IDs from Excel file
    excel_file = 'urls.xlsx'
    df = pd.read_excel(excel_file)

    for index, row in df.iterrows():
        url = row['URL']
        url_id = row['URL_ID']
        extract_article(url, url_id)

if __name__ == "__main__":
    main()
