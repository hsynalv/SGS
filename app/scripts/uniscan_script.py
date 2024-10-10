import os
import subprocess
import sys
import re
import time

def check_uniscan_installed():
    """Uniscan aracının yüklü olup olmadığını kontrol eder."""
    try:
        subprocess.run(["uniscan", "-h"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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

def run_uniscan(url):
    """Uniscan aracını kullanarak URL taraması gerçekleştirir."""
    print("Tarama Başlatılıyor...")
    time.sleep(2)

    output_file = "uniscan_output.xml"
    
    try:
        # Uniscan komutunu çalıştır ve çıktıyı XML formatında kaydet
        command = ["uniscan", "-u", url, "-qwedsio", "-o", output_file]
        subprocess.run(command, check=True)
        print(f"\nTarama başarıyla tamamlandı ve sonuçlar {output_file} dosyasına kaydedildi: {url}\n")
    except KeyboardInterrupt:
        print("\n\nProgram Sonlandırıldı...\n")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"\nTarama sırasında bir hata oluştu: {e}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\nBeklenmedik bir hata oluştu: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] == "-h":
        print("\nKullanım: python3 uniscan_script.py <url>\n")
        sys.exit(1)

    url = sys.argv[1]

    if not validate_url(url):
        print("\nGeçersiz URL formatı. Lütfen geçerli bir URL girin.\n")
        sys.exit(1)

    if not check_uniscan_installed():
        print("\nUniscan aracı yüklü değil. Lütfen önce Uniscan'ı yükleyin.\n")
        print("\nsudo apt install uniscan\n")
        sys.exit(1)

    run_uniscan(url)
