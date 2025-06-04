import os
import subprocess
import sys
import socket

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'outputs')
os.makedirs(OUTPUT_DIR, exist_ok=True)

def check_emailfinder_installed():
    """Emailfinder aracının yüklü olup olmadığını kontrol eder."""
    try:
        subprocess.run(["emailfinder", "-h"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print("Emailfinder yüklü, ancak çalıştırılamadı. Hata:", e)
        sys.exit(1)
    except FileNotFoundError:
        print("Emailfinder aracı yüklü değil. Lütfen aracı yükleyin.")
        sys.exit(1)

def validate_domain(domain):
    """Verilen domain'in geçerli olup olmadığını DNS çözümlemesi yaparak kontrol eder."""
    try:
        socket.gethostbyname(domain)
        return True
    except socket.gaierror:
        return False

def run_emailfinder(domain):
    """Emailfinder aracını belirtilen domain üzerinde çalıştırır."""
    try:
        output_file = os.path.join(OUTPUT_DIR, "emailfinder_out.txt")
        command = ["emailfinder", "-d", domain]
        print("\nTarama başlatıldı, email bilgileri tespit ediliyor...\n")
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        with open(output_file, "w") as f:
            f.write(result.stdout.decode())
        print(f"Emailfinder çalışması tamamlandı. Çıktı dosyası: {os.path.abspath(output_file)}")
    except subprocess.CalledProcessError as e:
        print("Emailfinder çalıştırılırken bir hata oluştu. Hata kodu:", e.returncode)
        print("Hata mesajı:", e.stderr.decode())
    except KeyboardInterrupt:
        print("\nİşlem kullanıcı tarafından durduruldu.")
        sys.exit(1)
    except Exception as e:
        print("Beklenmeyen bir hata oluştu:", str(e))
        sys.exit(1)

def main():
    if len(sys.argv) != 2 or sys.argv[1] == "-h":
        print("\nKullanım: python emailfinder_script.py <domain>\n")
        sys.exit(1)

    domain = sys.argv[1]

    # Domain'in geçerli olup olmadığını kontrol et
    if not validate_domain(domain):
        print(f"\nGeçersiz domain: {domain}\n")
        print("Lütfen geçerli bir domain girin (örneğin: example.com).")
        print("\nKullanım: python emailfinder_script.py <domain>\n")
        sys.exit(1)

    # Emailfinder'ın yüklü olup olmadığını kontrol et
    check_emailfinder_installed()

    # Emailfinder ile taramayı gerçekleştir
    run_emailfinder(domain)

if __name__ == "__main__":
    main()
