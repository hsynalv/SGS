from flask import Blueprint, render_template, redirect, url_for, send_from_directory, json, Response
# import google.generativeai as genai
import openai
from . import socketio
import threading
import subprocess
import logging
import time
import os
import requests

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('home.html')

@main_bp.route('/scan')
def scan():
    return render_template('scan.html')

@main_bp.route('/scan_status')
def scan_status():
    return render_template('scan_status.html')

# Arka planda çalışacak tarama işlemi
# long_task fonksiyonuna tarama tamamlandıktan sonra completed event'i gönderiyoruz
def long_task(command, tool_name, domain_or_url):
    try:
        logging.info(f'{tool_name} taraması başladı: {domain_or_url}')
        socketio.emit('progress', {'status': f'{tool_name} taraması başladı: {domain_or_url}'})

        # Tarama uzun sürerse her 10 saniyede bir hala devam ettiğini bildiren bir mesaj gönder
        for i in range(0, 100, 10):
            time.sleep(10)  # 10 saniye bekle
            socketio.emit('progress', {'status': f'{tool_name} taraması devam ediyor... {i}%'})

        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        logging.info(f'{tool_name} taraması tamamlandı: {domain_or_url}')
        socketio.emit('progress', {'status': f'{tool_name} taraması tamamlandı: {domain_or_url}'})
        socketio.emit('completed', {'status': f'{tool_name} taraması tamamlandı.'})  # Tamamlama mesajı
    except subprocess.CalledProcessError as e:
        logging.error(f'{tool_name} taraması başarısız oldu: {domain_or_url}, Hata: {str(e)}')
        socketio.emit('progress', {'status': f'{tool_name} taraması başarısız oldu: {domain_or_url}. Hata: {str(e)}'})



# WebSocket ile tarama işlemini başlatma
@socketio.on('start_scan')
def start_scan(data):
    tool = data.get('tool')

    # Seçilen araca göre uygun komutu çalıştırıyoruz
    if tool == 'nikto':
        domain = data.get('domain')
        port = data.get('port')
        ssl_option = data.get('ssl_option')
        command = ['python3', 'app/scripts/nikto_script.py', domain, port, ssl_option]
        print(command)
        threading.Thread(target=long_task, args=(command, 'Nikto', domain)).start()

    elif tool == 'nmap':
        domain = data.get('domain')
        scan_type = data.get('scan_type')
        command = ['python3', 'app/scripts/nmap_script.py', domain, scan_type]
        print(command)
        threading.Thread(target=long_task, args=(command, 'Nmap', domain)).start()

    elif tool == 'raccoon':
        domain = data.get('domain')
        command = ['python3', 'app/scripts/raccoon_script.py', domain]
        print(command)
        threading.Thread(target=long_task, args=(command, 'Raccoon', domain)).start()

    elif tool == 'skipfish':
        url = data.get('url')
        command = ['python3', 'app/scripts/skipfish_script.py', url]
        print(command)
        threading.Thread(target=long_task, args=(command, 'Skipfish', url)).start()

    elif tool == 'wapiti':
        url = data.get('url')
        command = ['python3', 'app/scripts/wapiti_script.py', url]
        print(command)
        threading.Thread(target=long_task, args=(command, 'Wapiti', url)).start()

    elif tool == 'dirb':
        url = data.get('url')
        command = ['python3', 'app/scripts/dirb_scan.py', url]
        print(command)
        threading.Thread(target=long_task, args=(command, 'Dirb', url)).start()

    elif tool == 'google_dork':
        domain = data.get('domain')
        command = ['python3', 'app/scripts/googleDork.py', domain]
        threading.Thread(target=long_task, args=(command, 'Google Dork', domain)).start()

    elif tool == 'slowloris_ddos':
        url = data.get('url')
        command = ['python3', 'app/scripts/slowlorisDDOS.py', url]
        print(command)
        threading.Thread(target=long_task, args=(command, 'Slowloris DDOS', url)).start()

    elif tool == 'sublist3r':
        domain = data.get('domain')
        command = ['python3', 'app/scripts/subdomain_detect.py', domain]
        print(command)
        threading.Thread(target=long_task, args=(command, 'Sublist3r', domain)).start()

    elif tool == 'dork_intelligence_name':
        name = data.get('name')
        command = ['python3', 'app/scripts/dorkIntellegenceName.py', name]
        print(command)
        threading.Thread(target=long_task, args=(command, 'Google Dork Intelligence (Name)', name)).start()

    elif tool == 'email_find_domain':
        domain = data.get('domain')
        command = ['python3', 'app/scripts/emailfinddomain.py', domain]
        print(command)
        threading.Thread(target=long_task, args=(command, 'Email Find Domain', domain)).start()

    elif tool == 'local_exploredevice':
        interface = data.get('interface')
        ip_cidr = data.get('ip_cidr')
        command = ['python3', 'app/scripts/localExploredevice.py', interface, ip_cidr]
        print(command)
        threading.Thread(target=long_task, args=(command, 'Local Explore Device', interface)).start()

    # Social Analyzer aracı seçildiyse
    elif tool == 'social_analyzer_name':
        target_name = data.get('target_name')
        command = ['python3', 'app/scripts/socialAnalyzerName.py', target_name]
        print(command)
        threading.Thread(target=long_task, args=(command, 'Social Analyzer', target_name)).start()

    # Taramanın başlatıldığını bildiriyoruz
    socketio.emit('progress', {'status': 'Tarama başlatıldı!'})
    # Yönlendirme işlemi
    socketio.emit('redirect', {'url': '/scan_status'})


# Tarama değerlendirme sayfası
@main_bp.route('/scanning-evaluation')
def tarama_degerlendirme():
    outputs_dir = os.path.join(os.getcwd(), 'outputs')

    # Tüm .xml dosyalarını listeleyelim
    xml_files = []
    if os.path.exists(outputs_dir):
        xml_files = [f for f in os.listdir(outputs_dir) if f.endswith('.xml')]

    # Dosyaları kategorize etme (örneğin tool ismine göre)
    categorized_files = {}
    for file in xml_files:
        tool_name = file.split('_')[0]  # Dosya ismi tool ismiyle başlıyorsa
        if tool_name not in categorized_files:
            categorized_files[tool_name] = []
        categorized_files[tool_name].append(file)

    return render_template('scanning-evaluation.html', categorized_files=categorized_files)


@main_bp.route('/start_scan_and_redirect')
def start_scan_and_redirect():
    # Tarama işlemi burada başlatılabilir (şimdilik yönlendirme yapıyoruz)
    return redirect(url_for('main.tarama_degerlendirme'))

@main_bp.route('/download/<filename>')
def download_file(filename):
    outputs_dir = os.path.join(os.getcwd(), 'outputs')
    return send_from_directory(directory=outputs_dir, path=filename, as_attachment=True)

@main_bp.route('/show/<filename>')
def show_file(filename):
    outputs_dir = os.path.join(os.getcwd(), 'outputs')
    return send_from_directory(directory=outputs_dir, path=filename, as_attachment=False)

@main_bp.route('/evaluate_scan/<filename>', methods=['GET'])
def evaluate_scan(filename):
    # API anahtarını çevresel değişkenden alma
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
    
    # API anahtarı yoksa hata mesajı döndür
    if not OPENAI_API_KEY:
        return Response(json.dumps({"evaluation": "API anahtarı bulunamadı. Lütfen OPENAI_API_KEY çevresel değişkenini ayarlayın."}, ensure_ascii=False), 
                      content_type="application/json; charset=utf-8")
    
    openai.api_key = OPENAI_API_KEY
    
    # XML dosyasının içeriğini okuma
    file_path = f"outputs/{filename}"
    with open(file_path, 'r') as file:
        file_content = file.read()

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Sen bir siber güvenlik uzmanısın. Verilen tarama çıktılarını detaylı ve profesyonel bir şekilde analiz edip, belirli bir formatta cevap vermelisin. Risk puanı verirken zaafiyetlerin ciddiyetini, sayısını ve potansiyel etkilerini dikkate almalısın."},
                {"role": "user", "content": f"""Sana linux güvenlik tarama araçlarıyla yapılan web sitesi taramasının çıktılarını gönderiyorum. Bu çıktıları detaylı bir şekilde analiz et ve aşağıdaki formatta cevap ver:

**RİSK PUANI: [0-100]**
(Bu puan sistemdeki zaafiyetlere göre belirlenecek. Puanı hesaplarken şu faktörleri dikkate al:
- Bulunan zaafiyetlerin sayısı ve ciddiyeti
- Kritik zaafiyetler (RCE, SQL Injection vb.) 25-35 puan arttırır
- Yüksek seviye zaafiyetler 15-25 puan arttırır
- Orta seviye zaafiyetler 5-15 puan arttırır
- Düşük seviye zaafiyetler 1-5 puan arttırır
- Zaafiyetlerin birleştirilip bir saldırı zinciri oluşturma potansiyeli
- SSL/TLS eksiklikleri, güncel olmayan servisler
- Zaafiyetlerin gerçekten istismar edilebilirliği
100 puan en riskli durumu gösterir, 0 puan ise hiçbir risk olmadığını gösterir.)

**RİSK SEVİYESİ: [Düşük/Orta/Yüksek/Kritik]**
(0-25: Düşük, 26-50: Orta, 51-75: Yüksek, 76-100: Kritik)

**ÖZET:**
(Tarama sonucunun kısa özeti)

**BULUNAN ZAAFİYETLER:**
1. [Zaafiyet Adı 1] - [Risk Seviyesi]
   - Açıklama: [Zaafiyet açıklaması]
   - Etki: [Olası etkiler]
   - Çözüm: [Çözüm önerisi]

2. [Zaafiyet Adı 2] - [Risk Seviyesi]
   - Açıklama: [Zaafiyet açıklaması]
   - Etki: [Olası etkiler]
   - Çözüm: [Çözüm önerisi]

**GENEL ÖNERİLER:**
(Sistemin genel güvenliğini artırmak için öneriler)

Tarama çıktısı: {filename}
Tool Çıktısı: {file_content}"""}
            ],
            max_tokens=2000
        )
        
        # Yanıtı text formatında al
        evaluation = response.choices[0].message.content
        evaluation = evaluation.replace("\n", "<br>")
    except Exception as e:
        evaluation = f"API hatası: {str(e)}"
    
    response_data = json.dumps({"evaluation": evaluation}, ensure_ascii=False)
    return Response(response_data, content_type="application/json; charset=utf-8")