import requests
import sys
import xml.etree.ElementTree as ET
from urllib.parse import quote
import validators

def generate_dork_url(domain, dork):
    """Belirtilen domain ve dork için Google arama URL'sini oluşturur."""
    base_url = "https://www.google.com/search?q="
    query = f"site:{domain} {dork}"
    return base_url + quote(query)

def fetch_dork_results(domain, dorks):
    """Belirtilen domain ve dork'lar için bilgi toplayan fonksiyon."""
    root = ET.Element("domain_info")  # XML kök elementi oluşturuyoruz
    domain_element = ET.SubElement(root, "domain", name=domain)
    print("\nGoogle Dorking taraması başlatıldı...\n")
    
    for dork in dorks:
        url = generate_dork_url(domain, dork)
        try:
            response = requests.get(url)
            if response.status_code == 200:
                # Sonuçları burada işleyebilirsiniz. Örneğin, sadece URL'yi kaydediyoruz
                result_element = ET.SubElement(domain_element, "dork_result", type=dork)
                result_element.text = url
            else:
                ET.SubElement(domain_element, "dork_result", type=dork).text = "Error: Non-200 status code"
        except requests.RequestException as e:
            ET.SubElement(domain_element, "dork_result", type=dork).text = f"Request failed: {str(e)}"
        except KeyboardInterrupt:
            print("\nTarama kullanıcı tarafından durduruldu.")
            sys.exit(1)
        except Exception as e:
            ET.SubElement(domain_element, "dork_result", type=dork).text = f"Unexpected error: {str(e)}"

    tree = ET.ElementTree(root)
    tree.write(f"{domain}_dork_results.xml", encoding='utf-8', xml_declaration=True)
    print(f"Veriler {domain}_dork_results.xml dosyasına kaydedildi.")

def validate_domain(domain):
    """Domain'in geçerli olup olmadığını kontrol eder."""
    if not validators.domain(domain):
        print("Geçersiz domain. Lütfen geçerli bir domain girin.")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Kullanım: python3 googleDork_script.py <domain>")
        sys.exit(1)

    domain = sys.argv[1]
    
    try:
        validate_domain(domain)
    except Exception as e:
        print(f"Domain doğrulama hatası: {str(e)}")
        sys.exit(1)

    dorks = [
        "intitle:index.of",
        "inurl:admin",
        "intext:password",
        "inurl:login",
        "ext:xml | ext:conf | ext:cnf | ext:reg | ext:inf | ext:rdp | ext:cfg | ext:txt | ext:ora | ext:ini",
        "ext:sql | ext:dbf | ext:mdb",
        "inurl:wp- | inurl:wp-content | inurl:plugins | inurl:uploads | inurl:themes | inurl:download",
        "ext:log",
        "ext:bkf | ext:bkp | ext:bak | ext:old | ext:backup",
        'intext:"sql syntax near" | intext:"syntax error has occurred" | intext:"incorrect"',
        "ext:doc | ext:docx | ext:odt | ext:pdf | ext:rtf | ext:sxw | ext:psw | ext:ppt | ext:pptx | ext:pps | ext:csv",
        'ext:php intitle:phpinfo "published by the PHP Group"',
        "inurl:readme | inurl:license | inurl:install | inurl:setup | inurl:config",
        "ext:action | ext:struts | ext:do",
        "inurl:wp-content | inurl:wp-includes"
    ]

    try:
        fetch_dork_results(domain, dorks)
    except KeyboardInterrupt:
        print("\nTarama kullanıcı tarafından durduruldu.")
        sys.exit(1)
    except Exception as e:
        print(f"Bir hata oluştu: {str(e)}")
