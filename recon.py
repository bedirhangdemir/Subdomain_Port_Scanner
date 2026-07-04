import argparse
import sys
import requests
import nmap
import json

def get_arguments():
    parser = argparse.ArgumentParser(description="Otomatize Bilgi Toplama (Recon) Aracı")
    parser.add_argument("-d", "--domain", dest="domain", help="Hedef alan adı (Örn: hedef.com)", required=True)
    parser.add_argument("-o", "--output", dest="output", help="Çıktı dosyasının adı", default="rapor.json")
    return parser.parse_args()

def fallback_hackertarget(domain):
    print(f"[*] Yedek API (HackerTarget) devreye alınıyor...")
    subdomains = set()
    url = f"https://api.hackertarget.com/hostsearch/?q={domain}"
    
    try:
        response = requests.get(url, timeout=20)
        if response.status_code == 200:
            # Eğer API hata metni döndürürse (örn: rate limit) iptal et
            if "error" in response.text.lower():
                print("    [-] HackerTarget API kullanım sınırı aşılmış veya hata döndürdü.")
                return []
                
            # Gelen metni satır satır oku ve virgülle ayırıp sadece domaini al
            lines = response.text.split('\n')
            for line in lines:
                if ',' in line:
                    sub = line.split(',')[0].strip()
                    # Sadece hedef domain ile bitenleri listeye ekle (Alakasız verileri filtrele)
                    if sub.endswith(domain):
                        subdomains.add(sub)
            
            print(f"    [+] Toplam {len(subdomains)} adet alt alan adı bulundu (HackerTarget).")
            return list(subdomains)
        else:
            print(f"    [-] HackerTarget da yanıt vermedi. Durum Kodu: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"    [!] HackerTarget bağlantı hatası: {e}")
        return []

def get_subdomains(domain):
    print(f"[*] {domain} için crt.sh üzerinden alt alan adları aranıyor...")
    subdomains = set()
    url = f"https://crt.sh/?q=%.{domain}&output=json"
    
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            for entry in data:
                name_value = entry['name_value']
                for sub in name_value.split('\n'):
                    clean_sub = sub.replace('*.', '').strip()
                    if clean_sub:
                        subdomains.add(clean_sub)
            print(f"    [+] Toplam {len(subdomains)} adet alt alan adı bulundu (crt.sh).")
            return list(subdomains)
        else:
            print(f"    [-] crt.sh API hatası (Durum Kodu: {response.status_code}).")
            return fallback_hackertarget(domain) # crt.sh çökerse yedeği çağır
            
    except requests.exceptions.RequestException as e:
        print(f"    [!] crt.sh bağlantı hatası veya zaman aşımı yaşandı.")
        return fallback_hackertarget(domain) # crt.sh zaman aşımına uğrarsa yedeği çağır

def scan_ports(domain):
    print(f"[*] {domain} için Nmap ile açık portlar taranıyor...")
    nm = nmap.PortScanner()
    open_ports = []
    
    try:
        nm.scan(hosts=domain, arguments='-F -T4')
        for host in nm.all_hosts():
            for proto in nm[host].all_protocols():
                ports = nm[host][proto].keys()
                for port in ports:
                    if nm[host][proto][port]['state'] == 'open':
                        open_ports.append(port)
                        print(f"    [+] Açık Port Bulundu: {port}/{proto}")
                        
        if not open_ports:
            print("    [-] Açık port bulunamadı veya sunucu taramayı engelledi.")
    except Exception as e:
        print(f"    [!] Nmap tarama hatası: {e}")
        
    return open_ports

def save_report(data, output_file):
    print(f"[*] Sonuçlar {output_file} dosyasına kaydediliyor...")
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"    [+] Dosya başarıyla oluşturuldu: {output_file}")
    except Exception as e:
        print(f"    [!] Dosya kaydedilirken hata oluştu: {e}")

def main():
    args = get_arguments()
    target_domain = args.domain
    output_file = args.output

    print(f"\n--- Recon Başlatıldı: {target_domain} ---\n")
    
    subdomains = get_subdomains(target_domain)
    ports = scan_ports(target_domain)
    
    report_data = {
        "hedef": target_domain,
        "alt_alan_adlari": subdomains,
        "acik_portlar": ports
    }
    
    print()
    save_report(report_data, output_file)
    print("\n--- Recon Tamamlandı ---")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] İşlem kullanıcı tarafından iptal edildi.")
        sys.exit(1)
