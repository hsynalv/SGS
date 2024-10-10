import subprocess
import sys
import os

def check_metagoofil_installed():
    """Metagoofil aracının yüklü olup olmadığını kontrol eder."""
    try:
        subprocess.run(["metagoofil", "-h"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print("Metagoofil yüklü, ancak çalıştırılamadı. Hata:", e)
        sys.exit(1)
    except FileNotFoundError:
        print("Metagoofil aracı yüklü değil. Lütfen aracı yükleyin.")
        sys.exit(1)

def run_metagoofil(domain):
    """Metagoofil aracını belirtilen domain üzerinde çalıştırır."""
    try:
        command = ["metagoofil", "-d", domain, "-t", "pdf,doc,docx,xlsx","-o","metagoofil_result","-f","metagoofil.html","-e", "2"]
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Metagoofil çıktısı:\n", result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print("Metagoofil çalıştırılırken bir hata oluştu. Hata kodu:", e.returncode)
        print("Hata mesajı:", e.stderr.decode())
    except KeyboardInterrupt:
        print("\nİşlem kullanıcı tarafından durduruldu.")
        sys.exit(1)
    except Exception as e:
        print("Beklenmeyen bir hata oluştu:", str(e))
        sys.exit(1)

def main():
    if len(sys.argv) != 2:
        print("Kullanım: python3 metagoofil_script.py <domain>")
        sys.exit(1)

    domain = sys.argv[1]
    check_metagoofil_installed()
    run_metagoofil(domain)

if __name__ == "__main__":
    main()
