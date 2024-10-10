import nmap
import sys
import time

def perform_scan(domain, scan_type):
    nm = nmap.PortScanner()
    output_file = f"{domain}_nmap_scan.xml"
    
    try:
        if scan_type == '1':
            # Hafif, hızlı ve güvenli tarama (kısa tarama süresi ve temel port taraması)
            print("Hafif tarama başlatılıyor...\n\n")
            time.sleep(1)
            nm.scan(hosts=domain, arguments='-sC -sV -n -T4 -vv')
        elif scan_type == '2':
            # Yavaş, IDS atlatmalı ve web ile ilgili tüm scriptleri tarayan tarama
            print("Detaylı tarama başlatılıyor...\n\n")
            nm.scan(hosts=domain, arguments='-sV -Pn -f -n --data-length 176 -g 53 -T3 --script=vuln -vv')
        else:
            print("Geçersiz tarama türü seçimi.")
            return

        # Tarama sonuçlarını normal Nmap çıktısı gibi yazdırma
        for host in nm.all_hosts():
            print(f"\nHost: {host} ({nm[host].hostname()})")
            print(f"State: {nm[host].state()}")
            
            for proto in nm[host].all_protocols():
                print(f"\nProtocol: {proto}")
                ports = nm[host][proto].keys()
                for port in sorted(ports):
                    port_info = nm[host][proto][port]
                    print(f"Port: {port}\tState: {port_info['state']}\tService: {port_info['name']}\tVersion: {port_info.get('version', 'N/A')}")
                    
                    # Eğer bir script sonucu varsa, onu da yazdır
                    if 'script' in port_info:
                        print("Script Results:")
                        for script_id, output in port_info['script'].items():
                            print(f"{script_id}: {output}")

        # XML formatında sonuçları kaydet
        with open(output_file, 'wb') as f:
            f.write(nm.get_nmap_last_output())
        print(f"\nTarama tamamlandı. Sonuçlar {output_file} dosyasına kaydedildi.")

    except KeyboardInterrupt:
        print("\nTarama kullanıcı tarafından durduruldu. Çıkış yapılıyor...")
        sys.exit(1)
    except Exception as e:
        print(f"Tarama sırasında bir hata oluştu: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Kullanım: python nmap_script.py <domain> <scan_type>")
        print("\n<scan_type> 1: Hafif tarama, 2: Detaylı tarama(Uzun sürebilir!)")
        sys.exit(1)
    
    domain = sys.argv[1]
    scan_type = sys.argv[2]
    
    perform_scan(domain, scan_type)
