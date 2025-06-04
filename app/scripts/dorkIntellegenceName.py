#!/usr/bin/env python3

import os
import sys
import subprocess
import xml.etree.ElementTree as ET
import urllib.parse
import time

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'outputs')
os.makedirs(OUTPUT_DIR, exist_ok=True)

def print_help():
    print("\nKullanım: python3 googledork.py <isim>\n")

def perform_google_search(name):
    """Verilen isim için Google Dork aramaları yapar."""
    dorks = [
        f'intitle:"index of" "{name}"',
        f'Inurl:login.rsp "{name}"',
        f'allintext:"*.@gmail.com" OR "{name}" filetype:xlsx',
        f'"{name}" filetype:xlsx',
        f'allinurl:"{name}"',
        f'site:instagram.com "{name}"',
        f'site:x.com "{name}"',
        f'"{name}" "Türkiye"',
        f'inurl:"{name}"',
        f'intitle:"{name}"',
        f'"{name}" "CV"',
        f'"{name}" "resume"',
        f'site:linkedin.com "{name}"',
        f'site:facebook.com "{name}"',
        f'site:twitter.com "{name}"',
        f'site:github.com "{name}"',
        f'filetype:pdf "{name}"',
        f'filetype:doc "{name}"',
        f'filetype:docx "{name}"',
        f'filetype:ppt "{name}"',
        f'intext:"{name}" "contact"',
        f'intext:"{name}" "email"',
        f'intext:"{name}" "phone"',
        f'intext:"{name}" "address"',
        f'site:*.edu "{name}"',
        f'site:*.gov "{name}"',
        f'ext:xls "{name}"',
        f'ext:csv "{name}"',
    ]

    print("Tarama başlatılıyor...\n")
    time.sleep(3)
    search_results = []
    for dork in dorks:
        # URL'yi encode et
        query = urllib.parse.quote(dork)
        url = f'https://www.google.com/search?q={query}'

        try:
            # Burada sadece URL'yi listeleyeceğiz. Gerçek arama yapmak için `requests` gibi bir kütüphane kullanılabilir.
            search_results.append(url)
        except Exception as e:
            print(f"Arama sırasında hata oluştu: {e}")
    
    print("---->>>|| Tarama bitti\n")
    
    return search_results

def output_to_xml(name, results):
    """Sonuçları XML formatında kaydeder."""
    root = ET.Element("GoogleDorkResults")
    name_element = ET.SubElement(root, "Name")
    name_element.text = name
    
    results_element = ET.SubElement(root, "Results")
    for result in results:
        result_element = ET.SubElement(results_element, "Result")
        result_element.text = result

    # XML formatına dönüştür
    xml_string = ET.tostring(root, encoding="unicode")

    # XML dosyasını kaydet
    filename = os.path.join(OUTPUT_DIR, f"GoogleDorkResults_{name.replace(' ', '_')}.xml")
    with open(filename, 'w') as xml_file:
        xml_file.write(xml_string)

    print(f"Sonuçlar {filename} dosyasına kaydedildi.")

def main():
    try:
        if len(sys.argv) != 2:
            print_help()
            sys.exit(1)

        name = sys.argv[1]

        if name in ['-h', '--help']:
            print_help()
            sys.exit(0)

        # Google dork aramasını gerçekleştir
        results = perform_google_search(name)

        # XML formatında çıktı al
        output_to_xml(name, results)

    except KeyboardInterrupt:
        print("\nProgram durduruldu.")
        sys.exit(0)
    except Exception as e:
        print(f"Beklenmeyen bir hata oluştu: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
    
# python3 dorkIntellegenceName.py "john doe"
