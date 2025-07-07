import requests
import time
from bs4 import BeautifulSoup

stop_flag = False

def set_stop_flag():
    global stop_flag
    stop_flag = True
    print("[INFO] Stop flag set")

def reset_stop_flag():
    global stop_flag
    stop_flag = False

def scrape_books_thread(start_url, max_items=20, delay=1, callback=None, progress_callback=None):
    global stop_flag
    books = []
    url = start_url

    while url and len(books) < max_items and not stop_flag:
        try:
            print(f"[SCRAPER] Scraping: {url}")
            response = requests.get(url)
            if response.status_code != 200:
                print(f"[ERROR] HTTP {response.status_code} saat akses {url}")
                break
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.select('.product_pod')

            for article in articles:
                if len(books) >= max_items or stop_flag:
                    break
                title = article.h3.a['title']
                price = article.select_one('.price_color').text.strip()
                rating = article.p['class'][1]
                availability = article.select_one('.instock.availability').text.strip()

                books.append({
                    'title': title,
                    'price': price,
                    'rating': rating,
                    'availability': availability
                })

                if progress_callback:
                    progress_callback(len(books))

            next_btn = soup.select_one('.next > a')
            if next_btn:
                next_href = next_btn['href']
                base_url = '/'.join(url.split('/')[:-1])
                url = f"{base_url}/{next_href}"
                time.sleep(delay)
            else:
                break

        except Exception as e:
            print(f"[ERROR] {e}")
            break

    if callback:
        callback(books)
    # Pastikan progress_callback dipanggil terakhir agar progres bar 100% saat selesai
    if progress_callback:
        progress_callback(len(books))
