#!/usr/bin/env python3

import os
import sys
import re
import subprocess
import xml.etree.ElementTree as ET
from datetime import datetime

def print_help():
    print("\nKullanım: python3 emailfinddomain.py <domain>")

def check_emailharvester_installed():
    """emailharvester aracının yüklü olup olmadığını kontrol eder."""
    try:
        subprocess.run(["emailharvester", "-h"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        print("emailharvester yüklü değil. Lütfen yüklemek için şu komutu çalıştırın:")
        print("sudo apt install emailharvester")
        sys.exit(1)

def is_valid_domain(domain):
    """Domain formatının geçerli olup olmadığını kontrol eder."""
    domain_regex = re.compile(
        r'^(?:[a-zA-Z0-9]'  # domainin ilk karakteri bir harf veya rakam olmalı
        r'(?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)'  # domain adı için geçerli karakterler
        r'+[a-zA-Z]{2,6}$'  # üst seviye domain en az 2 karakterli olmalı
    )
    return re.match(domain_regex, domain) is not None

def run_emailharvester(domain):
    """emailharvester komutunu çalıştırır."""
    try:
        command = ["emailharvester", "-d", domain, "-e", "all", "-r", "dogpile,youtube,googleplus,exalead,baidu,ask"]
        print("\nTarama başlatıldı...\n")
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("--->>>|| Tarama bitti.\n")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Hata oluştu: {e.stderr}")
        sys.exit(1)

def output_to_xml(domain, email_data):
    """Çıktıyı XML formatında döndürür."""
    root = ET.Element("EmailHarvestResult")
    domain_element = ET.SubElement(root, "Domain")
    domain_element.text = domain
    
    if email_data:
        emails_element = ET.SubElement(root, "Emails")
        for email in email_data.splitlines():
            email_element = ET.SubElement(emails_element, "Email")
            email_element.text = email.strip()

    # XML formatına dönüştür
    return ET.tostring(root, encoding="unicode")

def save_xml_to_file(xml_data):
    """XML verisini dosyaya kaydeder."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"emailFindDomain_{timestamp}.xml"
    
    with open(filename, 'w') as xml_file:
        xml_file.write(xml_data)
    
    print(f"Sonuçlar '{filename}' dosyasına kaydedildi.")

def main():
    try:
        if len(sys.argv) != 2:
            print_help()
            sys.exit(1)

        domain = sys.argv[1]

        if domain in ['-h', '--help']:
            print_help()
            sys.exit(0)

        # emailharvester yüklü mü kontrol et
        check_emailharvester_installed()

        # Domainin geçerli olup olmadığını kontrol et
        if not is_valid_domain(domain):
            print(f"Geçersiz domain: {domain}")
            sys.exit(1)

        # emailharvester komutunu çalıştır
        email_data = run_emailharvester(domain)

        # XML formatında çıktı al
        xml_result = output_to_xml(domain, email_data)

        # XML verisini dosyaya kaydet
        save_xml_to_file(xml_result)

    except KeyboardInterrupt:
        print("\nProgram durduruldu.")
        sys.exit(0)
    except Exception as e:
        print(f"Beklenmeyen bir hata oluştu: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
