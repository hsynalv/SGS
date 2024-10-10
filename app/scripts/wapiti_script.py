import subprocess
import sys
import shutil

def check_wapiti_installed():
    wapiti_path = shutil.which('wapiti')
    if wapiti_path:
        print("Wapiti aracı yüklü.\n")
    else:
        print("Wapiti aracı yüklü değil. Lütfen aşağıdaki komutu çalıştırarak yükleyin:")
        print("sudo apt-get install wapiti")  # Debian tabanlı sistemler için
        sys.exit(1)

def perform_scan(url):
    output_dir = '/home/kali/Documents/BilfenProject/wapitiScan'
    output_file = f"{output_dir}/{url.split('//')[-1].replace('/', '_')}_wapiti.xml"
    
    try:
        # Wapiti ile tarama yap ve sonuçları XML dosyasına kaydet
        print(f"{url} için tarama başlatılıyor...\n")
        command = ['wapiti', '-u', url, '-o', output_file, '--color', '--scan-force', 'normal', '-m', 'common', '-v', '1']
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
    if len(sys.argv) != 2:
        print("Kullanım: python script.py <url>")
        sys.exit(1)
    
    url = sys.argv[1]

    # Wapiti aracının yüklü olup olmadığını kontrol et
    check_wapiti_installed()
    
    # URL üzerinde tarama yap ve sonuçları XML olarak kaydet
    perform_scan(url)
