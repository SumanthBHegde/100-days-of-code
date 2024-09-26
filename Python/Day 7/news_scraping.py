# A program to demonstrate web scraping by scaping articles

import requests
from bs4 import BeautifulSoup
import csv
import os

class NewsScrapper:
    #initialising the class object
    def __init__(self, base_url, num_articles = 10, output_file='scraped_articles.csv'):
        self.base_url = base_url
        self.num_articles = num_articles
        self.output_file = output_file
        self.articles = []
        
    #Fetching the url for scraping
    def fetch_url(self, url):
        try:
            response =requests.get(url)
            if response.status_code == 200:
                return response.text
            else:
                print(f"Error fetching page: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error during requests to {url}: {e}")
        return None
    
    #Extracts the article's details such as title, URL, author, date, and summary.
    def parse_article(self, article_soup):
        
        #to find the article title
        title_tag = article_soup.find('h3') or article_soup.find('h2') 
        title = title_tag.get_text(strip=True) if title_tag else 'No Title'
        
        #to find the article link
        link_tag = article_soup.find('a', href=True)
        link = link_tag['href'] if link_tag else 'No URL'
        full_link = link if link.startswith('http') else os.path.join(self.base_url, link)
        
        #Assuming the first paragraph is the summary
        summary_tag = article_soup.find('p')
        summary = summary_tag.get_text(strip=True) if summary_tag else 'No Summary'
        
        #Adjusting based on website used
        author_tag = article_soup.find('span', class_='author')
        author = author_tag.get_text(strip=True) if author_tag else 'Unknown Author'
        
        date_tag = article_soup.find('time')
        date = date_tag['datetime'] if date_tag else 'Unknown Date'
        
        return title, full_link, author, date, summary
    
    #scrap single page for articles
    def scrape_page(self, url):
        html_content = self.fetch_url(url)
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            #Finding articles based on the page, adjusting based on actual website
            articles = soup.find_all('articles')
            
            for article_soup in articles:
                if len(self.articles) >= self.num_articles:
                    return #stop we have reached the requested number of articles
                article = self.parse_article(article_soup)
                self.articles.append(article)
     
    #Scrap across multiple pages or categories       
    def scrape_multiple_pages(self):
        page_number = 1
        while len(self.articles) < self.num_articles:
            
            #adjust it according to the website
            page_url = f"{self.base_url}/{page_number}"
            print(f"Scaraping Page: {page_url}")
            self.scrape_page(page_url)
            page_number += 1
            
            #preventing infinite loop by setting base case
            if page_number > 10:
                break
    
    #Save scraped articles to a CSV file
    def save_to_csv(self):
        with open(self.output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            #file header
            writer.writerow(['Title', 'URL', 'Author', 'Date', 'Summary'])
            
            #writing article data
            writer.writerows(self.articles)
                
    def scrape(self):
        print(f"Starting to scrape: {self.base_url}")
        self.scrape_multiple_pages()
        if self.articles:
            print(f"Scraped {len(self.articles)} aricles. Saving to {self.output_file}...")
            self.save_to_csv()
            print("Scraping Complete.")
        else:
            print("No Articles found.")
    
def main():
        base_url = input("Enter the news website URL to scrape: ").strip() or "https://www.deccanherald.com/archives"
        num_articles = int(input("How many articles do you want to scrape? ").strip() or 10)
        
        scraper = NewsScrapper(base_url, num_articles)
        scraper.scrape()
        
if __name__ == "__main__":
    main()
        
        