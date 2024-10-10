import subprocess
import sys

def check_sublist3r_installed():
    """Sublist3r aracının yüklü olup olmadığını kontrol eder."""
    try:
        subprocess.run(["sublist3r", "-h"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print("Sublist3r yüklü, ancak çalıştırılamadı. Hata:", e)
        sys.exit(1)
    except FileNotFoundError:
        print("Sublist3r aracı yüklü değil. Lütfen aracı yükleyin.")
        sys.exit(1)

def run_sublist3r(domain):
    """Sublist3r aracını belirtilen domain üzerinde çalıştırır ve sonuçları bir XML dosyasına kaydeder."""
    try:
        output_file = "subdomain.xml"
        command = ["sublist3r", "-v", "-d", domain, "-o", output_file]
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Sublist3r çalışması tamamlandı. Çıktı dosyası: {output_file}")
    except subprocess.CalledProcessError as e:
        print("Sublist3r çalıştırılırken bir hata oluştu. Hata kodu:", e.returncode)
        print("Hata mesajı:", e.stderr.decode())
    except KeyboardInterrupt:
        print("\nİşlem kullanıcı tarafından durduruldu.")
        sys.exit(1)
    except Exception as e:
        print("Beklenmeyen bir hata oluştu:", str(e))
        sys.exit(1)

def main():
    # Komut satırı argümanlarının kontrolü
    if len(sys.argv) != 2 or sys.argv[1] in ['-h', '--help']:
        print("Kullanım: python3 subdomain_detect.py <domain>")
        sys.exit(1)

    domain = sys.argv[1]
    check_sublist3r_installed()
    run_sublist3r(domain)

if __name__ == "__main__":
    main()
