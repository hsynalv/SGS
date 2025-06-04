#!/usr/bin/env python3

import os
import sys
import subprocess
import xml.etree.ElementTree as ET
import time

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'outputs')
os.makedirs(OUTPUT_DIR, exist_ok=True)

def print_help():
    print("\nKullanım: python3 socialAnalyzerName.py <target_name>\n")

def check_social_analyzer_installed():
    """social-analyzer aracının yüklü olup olmadığını kontrol eder."""
    try:
        subprocess.run(['social-analyzer', '--help'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        print("social-analyzer yüklü değil. Yükleniyor...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'social-analyzer'])

def perform_social_analysis(target_name):
    """Verilen hedef için sosyal medya analizini gerçekleştirir."""
    try:
        print("Tarama başlıyor...\n")
        time.sleep(1)
        result = subprocess.run(['social-analyzer', '--username', target_name], check=True, text=True, capture_output=True)
        print("\n----->>>|| Tarama bitti\n")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Analiz sırasında hata oluştu: {e}")
        return None

def output_to_xml(target_name, data):
    """Sonuçları XML formatında kaydeder."""
    root = ET.Element("SocialAnalyzerResults")
    target_element = ET.SubElement(root, "Target")
    target_element.text = target_name
    
    data_element = ET.SubElement(root, "Data")
    data_element.text = data.strip()  # Strip to remove extra newlines

    # XML formatına dönüştür
    xml_string = ET.tostring(root, encoding="unicode")

    # XML dosyasını kaydet
    filename = os.path.join(OUTPUT_DIR, f"SocialAnalyzerResults_{target_name.replace(' ', '_')}.xml")
    with open(filename, 'w') as xml_file:
        xml_file.write(xml_string)

    print(f"Sonuçlar {filename} dosyasına kaydedildi.")

def main():
    try:
        if len(sys.argv) != 2:
            print_help()
            sys.exit(1)

        target_name = sys.argv[1]

        if target_name in ['-h', '--help']:
            print_help()
            sys.exit(0)

        # social-analyzer'ın yüklü olup olmadığını kontrol et
        check_social_analyzer_installed()

        # Sosyal medya analizini gerçekleştir
        analysis_result = perform_social_analysis(target_name)

        if analysis_result:
            # XML formatında çıktı al
            output_to_xml(target_name, analysis_result)

    except KeyboardInterrupt:
        print("\nProgram durduruldu.")
        sys.exit(0)
    except Exception as e:
        print(f"Beklenmeyen bir hata oluştu: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
