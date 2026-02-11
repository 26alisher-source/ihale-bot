import requests
from bs4 import BeautifulSoup
import json

def get_live_data(filters):
    """
    Goszakup sitesine canlı bağlanır ve sadece istenen 4 veriyi çeker.
   
    """
    # Kullanıcının web sayfasından seçtiği filtreler
    keyword = filters.get('keyword', 'ремонт')
    city = filters.get('city', 'г. Караганда')
    status = filters.get('status', '350')
    method = filters.get('method', '2')

    print(f"🔍 Canlı arama yapılıyor: {city} | {keyword}")

    # Goszakup arama URL'si
    url = f"https://goszakup.gov.kz/ru/search/anno?filter[name]={keyword}&filter[kato]={city}&filter[status]={status}&filter[method]={method}"
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        tenders = []
        rows = soup.find_all('tr')[1:6] # İlk 5 sonucu alalım
        
        for row in rows:
            cols = row.find_all('td')
            if len(cols) > 5:
                # KYMBAT'IN İSTEDİĞİ 4 ÖZEL VERİ
                tenders.append({
                    "price": cols[5].text.strip(),       # 1. İHALE DEĞERİ
                    "title": cols[3].text.strip(),       # 2. TAM İHALE İSMİ
                    "method": method_label(method),      # 3. İHALE TÜRÜ
                    "status": status_label(status),      # 4. İHALE DURUMU
                    "no": cols[1].text.strip()
                })
        return tenders
    except:
        return []

def method_label(m):
    return {"2": "Открытый конкурс", "3": "Запрос ценовых предложений"}.get(m, "Другой")

def status_label(s):
    return {"350": "Завершено", "210": "Опубликовано"}.get(s, "Другой")

# Örnek çalıştırma
if __name__ == "__main__":
    sample_filters = {"city": "г. Караганда", "keyword": "дорог", "status": "350", "method": "2"}
    print(get_live_data(sample_filters))