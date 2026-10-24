import os
import sys
import json
from datetime import datetime
import urllib.request
import requests

def get_config():
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID', '5189419163')
    
    # Fallback to local .env if run locally
    if not token and os.path.exists('D:/AI_WORKSPACE/00_SYSTEM/CODEX_TELEGRAM/.env'):
        with open('D:/AI_WORKSPACE/00_SYSTEM/CODEX_TELEGRAM/.env', encoding='utf-8') as f:
            for line in f:
                if line.startswith('TELEGRAM_BOT_TOKEN='):
                    val = line.split('=', 1)[1].strip()
                    token = val.replace('"', '').replace("'", '')
                    
    if not token:
        raise ValueError('Missing TELEGRAM_BOT_TOKEN environment variable.')
    return token, chat_id

def fetch_hn_ai_news():
    url = 'https://hn.algolia.com/api/v1/search?tags=story&query=AI+OR+LLM+OR+Agent&numericFilters=points>15&hitsPerPage=8'
    headers = {'User-Agent': 'DailyAINewsBot/1.0', 'Accept': 'application/json'}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode('utf-8'))
    
    items = data.get('hits', [])[:5]
    res = []
    for h in items:
        title = h.get('title', '')
        url_link = h.get('url') or f"https://news.ycombinator.com/item?id={h.get('objectID')}"
        points = h.get('points', 0)
        comments = h.get('num_comments', 0)
        author = h.get('author', 'unknown')
        res.append({
            'title': title,
            'url': url_link,
            'points': points,
            'comments': comments,
            'author': author
        })
    return res

def fetch_hf_papers():
    url = 'https://huggingface.co/api/daily_papers'
    headers = {'User-Agent': 'DailyAINewsBot/1.0'}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        res = []
        for p in data[:3]:
            paper = p.get('paper', {})
            title = paper.get('title', '')
            paper_id = paper.get('id', '')
            upvotes = p.get('upvotes', 0)
            res.append({
                'title': title,
                'url': f'https://huggingface.co/papers/{paper_id}',
                'upvotes': upvotes
            })
        return res
    except Exception:
        return []

import html

def build_message(hn_items, hf_items):
    today = datetime.now().strftime('%d/%m/%Y')
    lines = [f"⚡ <b>[ĐIỂM TIN AI HÀNG NGÀY - {today}]</b>\n"]
    
    lines.append("🔥 <b>Tin tức & Công cụ AI thảo luận nhiều nhất:</b>")
    for i, item in enumerate(hn_items, 1):
        safe_title = html.escape(item['title'])
        safe_url = item['url']
        safe_author = html.escape(item['author'])
        lines.append(f'{i}. <a href="{safe_url}"><b>{safe_title}</b></a>')
        lines.append(f"   ⭐ {item['points']} điểm | 💬 {item['comments']} bình luận (@{safe_author})")
    
    if hf_items:
        lines.append("\n📑 <b>Nghiên cứu AI mới nhất (Hugging Face Papers):</b>")
        for i, item in enumerate(hf_items, 1):
            safe_title = html.escape(item['title'])
            safe_url = item['url']
            lines.append(f'- <a href="{safe_url}">{safe_title}</a> (👍 {item["upvotes"]})')
            
    lines.append("\n<i>Tự động gửi từ GitHub Actions (24/7 Cloud)</i>")
    return '\n'.join(lines)

def send_telegram(token, chat_id, text):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML',
        'disable_web_page_preview': False
    }
    resp = requests.post(url, json=payload, timeout=20)
    resp.raise_for_status()
    return resp.json()

def main():
    print('Starting Daily AI News Bot...')
    token, chat_id = get_config()
    print('Fetching Hacker News AI stories...')
    hn_items = fetch_hn_ai_news()
    print(f'Found {len(hn_items)} stories.')
    
    print('Fetching Hugging Face trending papers...')
    hf_items = fetch_hf_papers()
    print(f'Found {len(hf_items)} papers.')
    
    msg = build_message(hn_items, hf_items)
    print('Sending to Telegram...')
    send_telegram(token, chat_id, msg)
    print('Message delivered successfully!')

if __name__ == '__main__':
    main()
