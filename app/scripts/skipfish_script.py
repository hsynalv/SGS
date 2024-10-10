import subprocess
import sys
import shutil

def check_skipfish_installed():
    skipfish_path = shutil.which('skipfish')
    if skipfish_path:
        print("\nSkipfish aracı yüklü.\n")
    else:
        print("Skipfish aracı yüklü değil. Lütfen aşağıdaki komutu çalıştırarak yükleyin:")
        print("sudo apt-get install skipfish")  # Debian tabanlı sistemler için
        sys.exit(1)

def perform_scan(url):
    output_file = "/home/kali/Documents/BilfenProject/skipfish"
    
    try:
        # Skipfish ile tarama yap ve sonuçları XML dosyasına kaydet
        print(f"{url} için tarama başlatılıyor...\n")
        command = ['skipfish', '-o', output_file, '-u', url]
        subprocess.run(command, check=True)
        print(f"Tarama tamamlandı. Sonuçlar {output_file} dosyasına kaydedildi.")
    except KeyboardInterrupt:
        print("\nTarama kullanıcı tarafından durduruldu. Çıkış yapılıyor...")
        print(f"Sonuçlar {output_file} dosyasına kaydedildi.")
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

    # Skipfish aracının yüklü olup olmadığını kontrol et
    check_skipfish_installed()
    
    # URL üzerinde tarama yap ve sonuçları XML olarak kaydet
    perform_scan(url)
