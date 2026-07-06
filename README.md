# AutoRecon: Passive & Active Reconnaissance Tool

Bu proje, sızma testi (penetration testing) süreçlerinin ilk aşaması olan "Bilgi Toplama (Reconnaissance)" adımlarını otomatize etmek amacıyla geliştirilmiş bir güvenlik aracıdır.

## 🎯 Projenin Amacı ve Özellikleri
Açık kaynak istihbaratı (OSINT) ve aktif ağ taramalarını birleştirerek sistemlerin dışarıya açık yüzeyini (Attack Surface) haritalandırır.

*   **Pasif Subdomain Keşfi:** `crt.sh` (Certificate Transparency logs) üzerinden hedefin tüm alt alan adlarını (subdomain) trafiğe iz bırakmadan tespit eder.
*   **Hata Toleransı (Fallback Mechanism):** `crt.sh` API'sinin çökmesi veya zaman aşımına uğraması durumunda otomatik olarak `HackerTarget` API'sini devreye sokarak sürecin kesintisiz devam etmesini sağlar.
*   **Aktif Port Taraması:** Nmap entegrasyonu ile tespit edilen ana hedefin en kritik 100 portunu hızlıca (`-F -T4`) tarar.
*   **Formatlı Raporlama:** Elde edilen tüm verileri diğer siber güvenlik araçlarıyla (örn: Burp Suite) entegre edilebilmesi için yapılandırılmış JSON formatında çıktılar.

## 🛠️ Kurulum
Bu araç, Python 3 ve Nmap bağımlılıklarına ihtiyaç duyar.

```bash
# Nmap kurulumu (Eğer yüklü değilse)
sudo apt update && sudo apt install nmap -y

# Repoyu klonlama ve bağımlılıkların kurulumu
git clone https://github.com/bedirhangdemir/Subdomain_Port_Scanner.git
cd Subdomain_Port_Scanner
sudo apt install python3-requests python3-nmap -y

# Temel kullanım (Varsayılan olarak rapor.json oluşturur)
python3 recon.py -d ornekhedef.com

# Farklı isimde bir çıktı dosyası oluşturmak için
python3 recon.py -d ornekhedef.com -o sonuc_ornekhedef.json

##⚠️ Yasal Uyarı
Bu araç tamamen eğitim amaçlıdır ve yetkili sızma testleri için tasarlanmıştır. Sahip olmadığınız veya açık yetkiniz bulunmayan sistemler üzerinde kullanmayın.

Bedirhan Gökdemir tarafından siber güvenlik pratiği için geliştirilmiştir.

## Usage

```bash
python3 main.py
```
