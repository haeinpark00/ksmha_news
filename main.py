from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/ksmha-news", methods=["GET"])
def get_news():
    url = "http://www.ksmha.or.kr/bbs/board.php?bo_table=6_6&wr_id=1809"
    headers = { "User-Agent": "Mozilla/5.0" }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    news = []
    rows = soup.select("table tbody tr")

    for row in rows:
        a_tag = row.select_one("td.subject a")
        if a_tag:
            title = a_tag.get_text(strip=True)
            link = "http://www.ksmha.or.kr" + a_tag['href']
            news.append({ "title": title, "link": link })

    return jsonify(news[:10])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
