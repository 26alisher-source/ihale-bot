import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_goszakup_data(city, keyword, status):
    print(f"🔍 Ищем в Goszakup: {city} | {keyword}") #
    url = f"https://goszakup.gov.kz/ru/search/anno?filter[kato]={city}&filter[name]={keyword}&filter[status]={status}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        tenders = []
        rows = soup.find_all('tr')[1:6]
        for row in rows:
            cols = row.find_all('td')
            if len(cols) > 5:
                # İstenen 4 Veri: Değer, İsim, Tür, Durum
                tenders.append({
                    "price": cols[5].text.strip(),
                    "title": cols[3].text.strip(),
                    "no": cols[1].text.strip(),
                    "status": "Активен" if status == "210" else "Завершен"
                })
        return tenders
    except:
        return []

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    results = get_goszakup_data(data['city'], data['keyword'], data['status'])
    return jsonify(results)

if __name__ == "__main__":
    app.run(port=5000) #
