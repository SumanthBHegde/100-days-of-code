import newspaper
from newspaper import Article
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
import nltk

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

# Define URLs for Indian news sources
news_sources = {
    "The Times of India": "https://timesofindia.indiatimes.com",
    "The Hindu": "https://www.thehindu.com",
    "NDTV": "https://www.ndtv.com",
}

# Function to fetch and summarize news articles
def fetch_and_summarize_articles(url):
    paper = newspaper.build(url, memoize_articles=False)
    summaries = []
    
    # Limit to first 10 articles for quick testing
    for article in paper.articles[:10]:
        try:
            article.download()
            article.parse()
            article.nlp()
            
            # Create summary using NLTK tokenization
            sentences = sent_tokenize(article.text)
            important_sentences = [sent for sent in sentences if any(word in sent for word in article.keywords)]
            summary = ''.join(important_sentences[:3]) # Choose top 3 relevant sentences
            
            summaries.append({
                "title": article.title,
                "authors": article.authors,
                "date": article.publish_date,
                "summary": summary,
                "url": article.url
            })
        
        except Exception as e:
            print(f"Error processing articles: {e}")
    
    return summaries

# Fetch and print summaries in each source
for source, url in news_sources.items():
    print(f"---- {source} ----")
    summaries = fetch_and_summarize_articles(url)
    for article in summaries:
        print(f"Title: {article['title']}")
        print(f"Authors: {article['authors']}")
        print(f"Date: {article['date']}")
        print(f"Summary: {article['summary']}")
        print(f"Read more: {article['url']}\n")