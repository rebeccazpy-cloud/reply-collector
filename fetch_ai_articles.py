#!/usr/bin/env python3
"""
Fetch latest AI-related high-quality articles from OPML RSS feeds
"""

import feedparser
import requests
from datetime import datetime, timezone
from collections import defaultdict
import json
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

# OPML feed URLs extracted from the gist
FEED_URLS = [
    "https://simonwillison.net/atom/everything/",
    "https://www.jeffgeerling.com/blog.xml",
    "https://www.seangoedecke.com/rss.xml",
    "https://krebsonsecurity.com/feed/",
    "https://daringfireball.net/feeds/main",
    "https://ericmigi.com/rss.xml",
    "http://antirez.com/rss",
    "https://idiallo.com/feed.rss",
    "https://maurycyz.com/index.xml",
    "https://pluralistic.net/feed/",
    "https://shkspr.mobi/blog/feed/",
    "https://lcamtuf.substack.com/feed",
    "https://mitchellh.com/feed.xml",
    "https://dynomight.net/feed.xml",
    "https://utcc.utoronto.ca/~cks/space/blog/?atom",
    "https://xeiaso.net/blog.rss",
    "https://devblogs.microsoft.com/oldnewthing/feed",
    "https://www.righto.com/feeds/posts/default",
    "https://lucumr.pocoo.org/feed.atom",
    "https://skyfall.dev/rss.xml",
    "https://garymarcus.substack.com/feed",
    "https://rachelbythebay.com/w/atom.xml",
    "https://overreacted.io/rss.xml",
    "https://timsh.org/rss/",
    "https://www.johndcook.com/blog/feed/",
    "https://gilesthomas.com/feed/rss.xml",
    "https://matklad.github.io/feed.xml",
    "https://www.theatlantic.com/feed/author/derek-thompson/",
    "https://evanhahn.com/feed.xml",
    "https://terriblesoftware.org/feed/",
    "https://rakhim.exotext.com/rss.xml",
    "https://joanwestenberg.com/rss",
    "https://xania.org/feed",
    "https://micahflee.com/feed/",
    "https://nesbitt.io/feed.xml",
    "https://www.construction-physics.com/feed",
    "https://feed.tedium.co/",
    "https://susam.net/feed.xml",
    "https://entropicthoughts.com/feed.xml",
    "https://buttondown.com/hillelwayne/rss",
    "https://www.dwarkeshpatel.com/feed",
    "https://borretti.me/feed.xml",
    "https://www.wheresyoured.at/rss/",
    "https://jayd.ml/feed.xml",
    "https://minimaxir.com/index.xml",
    "https://geohot.github.io/blog/feed.xml",
    "http://www.aaronsw.com/2002/feeds/pgessays.rss",
    "https://www.filfre.net/feed/",
    "https://blog.jim-nielsen.com/feed.xml",
    "https://dfarq.homeip.net/feed/",
    "https://jyn.dev/atom.xml",
    "https://www.geoffreylitt.com/feed.xml",
    "https://www.downtowndougbrown.com/feed/",
    "https://brutecat.com/rss.xml",
    "https://eli.thegreenplace.net/feeds/all.atom.xml",
    "https://www.abortretry.fail/feed",
    "https://fabiensanglard.net/rss.xml",
    "https://oldvcr.blogspot.com/feeds/posts/default",
    "https://bogdanthegeek.github.io/blog/index.xml",
    "https://hugotunius.se/feed.xml",
    "https://gwern.substack.com/feed",
    "https://berthub.eu/articles/index.xml",
    "https://chadnauseam.com/rss.xml",
    "https://simone.org/feed/",
    "https://it-notes.dragas.net/feed/",
    "https://beej.us/blog/rss.xml",
    "https://hey.paris/index.xml",
    "https://danielwirtz.com/rss.xml",
    "https://matduggan.com/rss/",
    "https://refactoringenglish.com/index.xml",
    "https://worksonmymachine.substack.com/feed",
    "https://philiplaine.com/index.xml",
    "https://steveblank.com/feed/",
    "https://bernsteinbear.com/feed.xml",
    "https://danieldelaney.net/feed",
    "https://www.troyhunt.com/rss/",
    "https://herman.bearblog.dev/feed/",
    "https://tomrenner.com/index.xml",
    "https://blog.pixelmelt.dev/rss/",
    "https://martinalderson.com/feed.xml",
    "https://danielchasehooper.com/feed.xml",
    "https://www.chiark.greenend.org.uk/~sgtatham/quasiblog/feed.xml",
    "https://grantslatton.com/rss.xml",
    "https://www.experimental-history.com/feed",
    "https://anildash.com/feed.xml",
    "https://aresluna.org/main.rss",
    "https://michael.stapelberg.ch/feed.xml",
    "https://blog.miguelgrinberg.com/feed",
    "https://keygen.sh/blog/feed.xml",
    "https://mjg59.dreamwidth.org/data/rss",
    "https://computer.rip/rss.xml",
    "https://www.tedunangst.com/flak/rss",
]

# AI-related keywords for filtering
AI_KEYWORDS = [
    'ai', 'artificial intelligence', 'machine learning', 'ml', 'deep learning',
    'neural network', 'llm', 'large language model', 'gpt', 'chatgpt', 'claude',
    'openai', 'anthropic', 'gemini', 'copilot', 'agentic', 'agent', 'agi',
    'generative', 'transformer', 'diffusion', 'stable diffusion', 'midjourney',
    'dall-e', 'nlp', 'natural language', 'computer vision', 'reinforcement learning',
    'training data', 'model', 'inference', 'embedding', 'vector', 'rag',
    'retrieval augmented', 'fine-tuning', 'prompt', 'reasoning', 'hallucination',
    'alignment', 'safety', 'bias', 'ethics', 'superintelligence'
]


def fetch_feed(url):
    """Fetch a single RSS feed"""
    try:
        print(f"Fetching: {url}")
        response = requests.get(url, timeout=10)
        feed = feedparser.parse(response.content)
        return feed
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


def is_ai_related(text):
    """Check if text contains AI-related keywords"""
    if not text:
        return False
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in AI_KEYWORDS)


def calculate_quality_score(entry, feed_title=""):
    """
    Calculate a quality score for an article based on various factors
    Higher score = higher quality
    """
    score = 0
    
    # Base score
    score += 10
    
    # Title length (prefer substantial titles)
    title = entry.get('title', '')
    if 20 <= len(title) <= 100:
        score += 5
    elif len(title) > 100:
        score += 2
    
    # Summary/content length (prefer articles with substantial content)
    summary = entry.get('summary', '') or entry.get('description', '')
    if len(summary) > 500:
        score += 10
    elif len(summary) > 200:
        score += 5
    
    # Has author
    if entry.get('author'):
        score += 3
    
    # Recent articles get bonus
    pub_date = entry.get('published_parsed') or entry.get('updated_parsed')
    if pub_date:
        try:
            article_date = datetime(*pub_date[:6], tzinfo=timezone.utc)
            days_old = (datetime.now(timezone.utc) - article_date).days
            if days_old <= 7:
                score += 15
            elif days_old <= 30:
                score += 10
            elif days_old <= 90:
                score += 5
        except:
            pass
    
    # Popular blog sources get bonus (based on known quality sources)
    quality_sources = ['simonwillison', 'paulgraham', 'mitchellh', 'overreacted', 
                       'garymarcus', 'pluralistic', 'krebsonsecurity', 'troyhunt',
                       'matklad', 'gwern', 'dynomight', 'lucumr']
    feed_lower = feed_title.lower()
    if any(source in feed_lower for source in quality_sources):
        score += 8
    
    # AI-related content gets extra bonus
    if is_ai_related(title + ' ' + summary):
        score += 20  # Big bonus for AI content
    
    return score


def extract_articles():
    """Fetch and rank AI-related articles from all feeds"""
    all_articles = []
    
    # Fetch feeds in parallel for speed
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(fetch_feed, url): url for url in FEED_URLS}
        
        for future in as_completed(future_to_url):
            feed = future.result()
            if feed and hasattr(feed, 'entries'):
                feed_title = feed.feed.get('title', '') if hasattr(feed, 'feed') else ''
                
                for entry in feed.entries:
                    # Get title and summary for AI filtering
                    title = entry.get('title', '')
                    summary = entry.get('summary', '') or entry.get('description', '')
                    
                    # Only include AI-related articles
                    if not is_ai_related(title + ' ' + summary):
                        continue
                    
                    # Calculate quality score
                    quality_score = calculate_quality_score(entry, feed_title)
                    
                    # Get publication date
                    pub_date = entry.get('published_parsed') or entry.get('updated_parsed')
                    date_str = ""
                    if pub_date:
                        try:
                            date_str = datetime(*pub_date[:6]).strftime('%Y-%m-%d')
                        except:
                            date_str = "Unknown date"
                    
                    # Extract article info
                    article = {
                        'title': title or 'No title',
                        'link': entry.get('link', ''),
                        'author': entry.get('author', feed_title),
                        'published': date_str,
                        'summary': summary[:300],
                        'source': feed_title,
                        'quality_score': quality_score
                    }
                    
                    all_articles.append(article)
    
    # Sort by quality score
    all_articles.sort(key=lambda x: x['quality_score'], reverse=True)
    
    return all_articles


def main():
    print("🤖 Fetching AI-related articles from RSS feeds...")
    print(f"📡 Processing {len(FEED_URLS)} feeds\n")
    
    articles = extract_articles()
    
    print(f"\n✅ Found {len(articles)} AI-related articles")
    print(f"🎯 Selecting top 20 high-quality AI articles\n")
    
    # Get top 20
    top_articles = articles[:20]
    
    # Save to JSON
    output_file = '/Volumes/T7 Shield/reply-collector/ai_articles.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(top_articles, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Saved to: {output_file}\n")
    
    # Print results
    print("=" * 80)
    print("TOP 20 AI-RELATED HIGH-QUALITY ARTICLES")
    print("=" * 80)
    
    for i, article in enumerate(top_articles, 1):
        print(f"\n{i}. {article['title']}")
        print(f"   📅 {article['published']} | ✍️  {article['author']} | 🎯 Score: {article['quality_score']}")
        print(f"   🔗 {article['link']}")
        if article['summary']:
            summary = article['summary'].replace('\n', ' ').strip()[:150]
            print(f"   📝 {summary}...")
        print("-" * 80)
    
    return top_articles


if __name__ == "__main__":
    main()
