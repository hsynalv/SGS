import os
import subprocess
import sys
import time

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'outputs')
os.makedirs(OUTPUT_DIR, exist_ok=True)

def check_raccoon_installed():
    try:
        # Raccoon aracının yüklü olup olmadığını kontrol et
        subprocess.run(['raccoon', '--help'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("\nRaccoon aracı yüklü.\n")
    except subprocess.CalledProcessError:
        print("Raccoon aracı yüklü değil. Lütfen aşağıdaki komutu çalıştırarak yükleyin:")
        print("pip install raccoon-scanner")
        sys.exit(1)
    except FileNotFoundError:
        print("Raccoon aracı yüklü değil. Lütfen aşağıdaki komutu çalıştırarak yükleyin:")
        print("pip install raccoon-scanner")
        sys.exit(1)

def perform_scan(domain):
    output_file = os.path.join(OUTPUT_DIR, f"{domain}_scan.xml")
    
    try:
        # Raccoon ile tarama yap ve sonuçları XML dosyasına kaydet
        print(f"{domain} için tarama başlatılıyor...\n")
        time.sleep(1)
        subprocess.run(['raccoon', '-f', domain, '-o', output_file], check=True)   # -f --> full scan
        print(f"Tarama tamamlandı. Sonuçlar {output_file} dosyasına kaydedildi.")
    except KeyboardInterrupt:
        print("Çıkış Yapıldı...")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Tarama sırasında bir hata oluştu: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Tarama sırasında bir hata oluştu: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("\nKullanım: python script.py <domain>")
        sys.exit(1)
    
    domain = sys.argv[1]
    
    # Raccoon aracının yüklü olup olmadığını kontrol et
    check_raccoon_installed()
    
    # Domain üzerinde tarama yap ve sonuçları XML olarak kaydet
    perform_scan(domain)
