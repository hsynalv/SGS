
import subprocess
import sys

def check_nikto_installed():
    try:
        # Nikto aracının yüklü olup olmadığını kontrol et
        subprocess.run(['nikto', '-h', 'localhost'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Nikto aracı yüklü.\n")
    except subprocess.CalledProcessError:
        print("Nikto aracı yüklü değil. Lütfen aşağıdaki komutu çalıştırarak yükleyin:")
        print("sudo apt-get install nikto")  # Debian tabanlı sistemler için
        sys.exit(1)
    except FileNotFoundError:
        print("Nikto aracı yüklü değil. Lütfen aşağıdaki komutu çalıştırarak yükleyin:")
        print("sudo apt-get install nikto")  # Debian tabanlı sistemler için
        sys.exit(1)

def perform_scan(domain, port, ssl_option):
    output_file = f"{domain}_nikto_scan.xml"
    ssl_flag = '-ssl' if ssl_option == 'ssl' else '-nossl'
    
    try:
        # Nikto ile tarama yap ve sonuçları XML dosyasına kaydet
        print(f"{domain} için tarama başlatılıyor...\n")
        command = ['nikto', '-h', domain, '-p', str(port), ssl_flag, '-e', '167', '-output', output_file, '-Format', 'xml']
        subprocess.run(command, check=True)
        print(f"Tarama tamamlandı. Sonuçlar {output_file} dosyasına kaydedildi.")
    except KeyboardInterrupt:
        print("\nTarama kullanıcı tarafından durduruldu. Çıkış yapılıyor...")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Tarama sırasında bir hata oluştu: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Tarama sırasında bir hata oluştu: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Kullanım: python script.py <domain> <port> <ssl_or_nossl>")
        print("<port> 80 veya 443")
        print("<ssl_or_nossl> ssl veya nossl")
        sys.exit(1)
    
    domain = sys.argv[1]
    port = sys.argv[2]
    ssl_option = sys.argv[3].lower()

    # Parametre doğrulama
    if port not in ['80', '443']:
        print("Geçersiz port. Port 80 veya 443 olmalıdır.")
        sys.exit(1)
    
    if ssl_option not in ['ssl', 'nossl']:
        print("Geçersiz SSL seçeneği. 'ssl' veya 'nossl' olmalıdır.")
        sys.exit(1)
    
    # Nikto aracının yüklü olup olmadığını kontrol et
    check_nikto_installed()
    
    # Domain üzerinde tarama yap ve sonuçları XML olarak kaydet
    perform_scan(domain, port, ssl_option)
