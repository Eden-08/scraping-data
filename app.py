from flask import Flask, render_template, request, redirect, send_file, jsonify
import pandas as pd
from scraper import set_stop_flag
import threading 
from io import BytesIO, StringIO

app = Flask(__name__)
data = []
scraping_status = {
    'running': False,
    'current': 0,
    'total': 0,
    'done': False,
    'stopped': False
}


@app.route('/', methods=['GET', 'POST'])
def index():
    global data, scraping_status
    scraping_status['done'] = False
    scraping_status['stopped'] = False
    return render_template('index.html', books=data)

@app.route('/start', methods=['POST'])
def start_scraping():
    global data, scraping_status
    url = request.form.get('url')
    try:
        limit = int(request.form.get('limit', 20))
        delay = float(request.form.get('delay', 1))
    except ValueError:
        return "Input tidak valid", 400

    from scraper import reset_stop_flag, scrape_books_thread

    reset_stop_flag()
    data = []
    scraping_status = {
        'running': True,
        'current': 0,
        'total': limit,
        'done': False,
        'stopped': False
    }
    def store_result(result):
        global data, scraping_status
        data = result
        scraping_status['done'] = True
        scraping_status['running'] = False
        scraping_status['stopped'] = False
    def progress_callback(current):
        scraping_status['current'] = current
        if current >= scraping_status['total']:
            scraping_status['done'] = True
            scraping_status['running'] = False

    # Start background thread
    threading.Thread(
        target=scrape_books_thread,
        args=(url, limit, delay, store_result, progress_callback),
        daemon=True
    ).start()

    return redirect('/')
@app.route('/status')
def get_status():
    print("[DEBUG] Status sent:", scraping_status)  # ✅ Tambahkan ini untuk cek realtime
    return jsonify(scraping_status)

@app.route('/stop')
def stop_scraping():
    global scraping_status
    set_stop_flag()
    scraping_status['stopped'] = True      # ✅ PASTIKAN baris ini ADA
    scraping_status['running'] = False     # ✅ pastikan juga ini
    print("[INFO] STOP called - status updated:", scraping_status)  # ✅ Tambahkan ini
    return redirect('/')

@app.route('/delete/<int:index>')
def delete(index):
    global data
    if not (0 <= index < len(data)):
        return "Index tidak valid", 404
    data.pop(index)
    return redirect('/')

@app.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit(index):
    global data
    if not (0 <= index < len(data)):
        return "Index tidak valid", 404
    if request.method == 'POST':
        data[index] = {
            'title': request.form['title'],
            'price': request.form['price'],
            'rating': request.form['rating'],
            'availability': request.form['availability']
        }
        return redirect('/')
    return render_template('edit.html', book=data[index], index=index)

@app.route('/download/<filetype>')
def download(filetype):
    df = pd.DataFrame(data)

    if filetype == 'csv':
        buffer = StringIO()
        df.to_csv(buffer, index=False)
        buffer.seek(0)
        return send_file(BytesIO(buffer.getvalue().encode()), download_name="books.csv", as_attachment=True)

    elif filetype == 'excel':
        buffer = BytesIO()
        df.to_excel(buffer, index=False, engine='openpyxl')
        buffer.seek(0)
        return send_file(buffer, download_name="books.xlsx", as_attachment=True)
    
    

    return redirect('/')

@app.route('/debug-data')
def debug_data():
    global data
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
