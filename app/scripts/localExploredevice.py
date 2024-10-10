#!/usr/bin/env python3

import sys
import subprocess
import xml.etree.ElementTree as ET

def print_help():
    print("\nKullanım: python localExploredevice.py <interface> <ip_cidr_notation>\n")

def check_arp_scan_installed():
    """arp-scan aracının yüklü olup olmadığını kontrol eder."""
    try:
        subprocess.run(['arp-scan', '-h'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        print("arp-scan yüklü değil. Lütfen yükleyin.")
        sys.exit(1)

def perform_scan(interface, ip_cidr_notation):
    """Verilen arayüz ve CIDR notasyonu için arp-scan ile tarama yapar."""
    try:
        print(f"Tarama başlıyor: Arayüz: {interface}, CIDR: {ip_cidr_notation}, Paket Sayısı: 8\n")
        
        # arp-scan komutunu oluştur
        command = ['arp-scan', '-I', interface, ip_cidr_notation, '-r', '8']
        
        # subprocess ile komutu çalıştır
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        return result.stdout.decode().strip()  # Sonuçları döndür

    except subprocess.CalledProcessError as e:
        print(f"Hata oluştu: {e.stderr.decode().strip()}")
        sys.exit(1)

def output_to_xml(data):
    """Sonuçları XML formatında kaydeder."""
    root = ET.Element("ArpScanResults")
    
    # Her bir cihaz için bir element oluştur
    for line in data.splitlines():
        if line.strip():  # Boş satırları atla
            device_element = ET.SubElement(root, "Device")
            device_element.text = line.strip()  # Cihaz bilgilerini ekle

    # XML formatına dönüştür
    xml_string = ET.tostring(root, encoding="unicode")

    # XML dosyasını kaydet
    filename = "ArpScanResults.xml"
    with open(filename, 'w') as xml_file:
        xml_file.write(xml_string)

    print(f"Sonuçlar {filename} dosyasına kaydedildi.")

def main():
    if len(sys.argv) != 3:
        print_help()
        sys.exit(1)

    # Komut satırı argümanlarını al
    interface = sys.argv[1]
    ip_cidr_notation = sys.argv[2]

    # arp-scan'ın yüklü olup olmadığını kontrol et
    check_arp_scan_installed()

    try:
        # Tarama işlemini gerçekleştir
        scan_result = perform_scan(interface, ip_cidr_notation)

        # Tarama sonuçlarını XML formatında kaydet
        output_to_xml(scan_result)

    except KeyboardInterrupt:
        print("\nTarama iptal edildi.")
        sys.exit(0)

if __name__ == "__main__":
    main()
