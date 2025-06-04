import os
import subprocess
import sys
import re
import time

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'outputs')
os.makedirs(OUTPUT_DIR, exist_ok=True)

def check_zap_installed():
    """ZAP aracının yüklü olup olmadığını kontrol eder."""
    try:
        subprocess.run(["zap.sh", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        return False

def validate_url(url):
    """URL'nin geçerli bir formatta olup olmadığını kontrol eder."""
    domain_pattern = re.compile(r'^(http://|https://)[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$')
    ip_pattern = re.compile(r'^(http://|https://)\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(/.*)?$')
    
    if re.match(domain_pattern, url) or re.match(ip_pattern, url):
        return True
    else:
        return False

def run_zap(url):
    """ZAP aracını kullanarak URL taraması gerçekleştirir."""
    print("\nTarama Başlatılıyor...")
    time.sleep(2)

    output_file = os.path.join(OUTPUT_DIR, "owaspZap_scanResult.xml")

    try:
        # ZAP'ı başlat ve taramayı gerçekleştir
        command = f"zap.sh -daemon -quickurl {url} -quickout {output_file} -quickprogress"
        subprocess.run(command, shell=True, check=True)

        print(f"\nTarama başarıyla tamamlandı ve sonuçlar {output_file} dosyasına kaydedildi: {url}\n")
    except KeyboardInterrupt:
        print("\nProgram Sonlandırıldı...\n")
    except subprocess.CalledProcessError as e:
        print(f"\nTarama sırasında bir hata oluştu: {e}\n")
    except Exception as e:
        print(f"\nBeklenmedik bir hata oluştu: {e}\n")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("\nKullanım: python3 owaspZap_script.py <url>\n")
        sys.exit(1)

    url = sys.argv[1]

    if not validate_url(url):
        print("\nGeçersiz URL formatı. Lütfen geçerli bir URL girin.\n")
        sys.exit(1)

    if not check_zap_installed():
        print("\nZAP aracı yüklü değil. Lütfen önce ZAP'ı yükleyin.\n")
        print("sudo apt install zaproxy")
        sys.exit(1)

    run_zap(url)
