from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    return '✅ KSMHA News API is running.'

@app.route('/ksmha-news')
def get_articles():
    url = 'http://www.ksmha.or.kr/bbs/board.php?bo_table=6_6&wr_id=1809'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }

    res = requests.get(url, headers=headers)
    print("🧾 Raw HTML Response:")
    print(res.text)  # ← 여기를 res로 수정!

    soup = BeautifulSoup(res.text, 'html.parser')
    rows = soup.find_all('tr')

    articles = []

    for row in rows:
        subject_td = row.find('td', class_='subject')
        if subject_td and subject_td.a:
            title = subject_td.a.get_text(strip=True)
            link = subject_td.a['href']
            full_link = f"http://www.ksmha.or.kr{link}"
            articles.append({
                "title": title,
                "link": full_link
            })

    return jsonify(articles)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
