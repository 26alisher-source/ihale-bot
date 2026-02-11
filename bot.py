import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Web sayfasının bota erişmesine izin verir

def get_goszakup_data(city, keyword, status):
    # Dinamik Filtreleme: Seçtiğin şehri (Kato) ve kelimeyi URL'ye ekler
    print(f"🔍 Canlı Sorgu: {city} | {keyword}")
    url = f"https://goszakup.gov.kz/ru/search/anno?filter[kato]={city}&filter[name]={keyword}&filter[status]={status}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        tenders = []
        rows = soup.find_all('tr')[1:6] # İlk 5 sonucu getir
        
        for row in rows:
            cols = row.find_all('td')
            if len(cols) > 5:
                # Kymbat'ın İstediği 4 Veri
                tenders.append({
                    "price": cols[5].text.strip(), # 1. İhale Değeri
                    "title": cols[3].text.strip(), # 2. İhale İsmi
                    "no": cols[1].text.strip(),    # 3. İhale Numarası
                    "status": "Завершен" if status == "350" else "Опубликован" # 4. Durum
                })
        return tenders
    except Exception as e:
        print(f"Hata oluştu: {e}")
        return []

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    results = get_goszakup_data(data['city'], data['keyword'], data['status'])
    return jsonify(results)

if __name__ == "__main__":
    # Botu 5000 portunda başlatır
    app.run(port=5000)
