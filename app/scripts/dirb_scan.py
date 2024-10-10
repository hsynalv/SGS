import subprocess
import sys
import validators
from datetime import datetime


def validate_url(url):
    """URL'nin geçerli olup olmadığını kontrol eder."""
    if not validators.url(url):
        print("Geçersiz URL. Lütfen geçerli bir URL girin.")
        sys.exit(1)

def run_dirb(url):
    """Dirb aracını belirtilen URL üzerinde çalıştırır ve çıktıyı XML formatında kaydeder."""
    try:
        wordlist = "/usr/share/wordlists/dirb/common.txt"
        # Zaman damgası ile benzersiz bir çıktı dosyası adı oluşturulur
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"dirb_output_{timestamp}.xml"  # Yeni bir çıktı dosyası adı oluşturulur
        command = ["dirb", url, wordlist, "-o", output_file]  # Çıktıyı XML formatında kaydetmek için '-o' kullanılır
        print("\nGizli dizin taraması başlatıldı...\n")

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Dirb çıktısını anlık olarak ekrana yazdır
        while True:
            output = process.stdout.readline()
            if output == b"" and process.poll() is not None:
                break
            if output:
                print(output.decode().strip())

        process.wait()
        if process.returncode == 0:
            print(f"\nDirb taraması tamamlandı. Çıktı dosyası: {output_file}")
        else:
            print("Dirb çalıştırılırken bir hata oluştu.")
            print("Hata kodu:", process.returncode)

    except subprocess.CalledProcessError as e:
        print("Dirb çalıştırılırken bir hata oluştu. Hata kodu:", e.returncode)
        print("Hata mesajı:", e.stderr.decode())
    except KeyboardInterrupt:
        print("\nİşlem kullanıcı tarafından durduruldu.")
        sys.exit(1)
    except Exception as e:
        print("Beklenmeyen bir hata oluştu:", str(e))
        sys.exit(1)

def main():
    if len(sys.argv) != 2:
        print("Kullanım: python3 dirb_scan.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    validate_url(url)
    run_dirb(url)

if __name__ == "__main__":
    main()
