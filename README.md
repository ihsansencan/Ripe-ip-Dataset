# 🌍 RIPE IP Dataset

Dünya genelindeki ülke/bölgelerin IPv4 ve IPv6 CIDR blokları. RIPE NCC, APNIC, ARIN, LACNIC ve AFRINIC verilerinden derlenmiştir.

---

## 📊 Veri Seti

| Veri | Açıklama | Dosya Sayısı |
|------|----------|--------------|
| **IPv4 CIDR** | Tüm dünya ülke/bölgeleri | 238 |
| **IPv6 CIDR** | IPv6 blokları | 110 |
| **JSON Özet** | RIPE NCC ülkeleri | 150 |

---

## 📁 Klasör Yapısı

```
┌──(root)-[/Ripe-ip-Dataset]
├── LICENSE
├── README.md
├── create_ip_list.py
└── data/
    ├── cidr_world/        # 238 IPv4 CIDR
    ├── cidr_ipv6/         # 110 IPv6 CIDR
    ├── ripe_json/         # 150 JSON
    └── ips/               # Örnek IP listeleri (.gz)
        ├── IL_ips.gz      # İsrail (16.1 MB)
        └── IR_ips.gz      # İran (22.9 MB)
```

---

## 🚀 Kullanım

```bash
┌──(root)-[/Ripe-ip-Dataset]
└─# python create_ip_list.py

📄 KULLANIM:
  python3 create_ip.py <ülke_kodu>              # IPv4
  python3 create_ip.py <ülke_kodu> --compress   # Sıkıştırılmış (.gz)
  python3 create_ip.py all                      # Tüm ülkeler
  python3 create_ip.py all --compress           # Tüm ülkeler (sıkıştırılmış)
  python3 create_ip.py list                     # Ülkeleri listele
  python3 create_ip.py IR                       # (IR) İran

💡 Örnek: python3 create_ip.py IR --compress
```


## 📄 Çıktı

```bash
┌──(root)-[/Ripe-ip-Dataset]
└─# python create_ip_list.py IL --compress

📄 IL IP listesi
   ├─ Toplam IP    : 8,035,200
   ├─ Tahmini Boyut: 14.9 MB (sıkıştırılmış)
   ├─ Açık Hali     : 114.9 MB
   ├─ Çıkış Formatı: .gz (sıkıştırılmış)
   └─ Örnek Bloklar: 2.52.0.0/262144, 2.57.228.0/1024, 5.22.128.0/2048

❓ Bu dosyayı oluşturmak istediğinize emin misiniz? (y/n): y

🚀 IL IPleri oluşturuluyor...

✅ IL IP listesi oluşturuldu!
   ├─ Toplam IP: 7,845,652
   ├─ Dosya Boyutu: 15.4 MB
   ├─ Geçen Süre: 11.6 saniye
   └─ Dosya: data/ips/IL_ips.gz

┌──(root)-[/Ripe-ip-Dataset]
└─# python create_ip_list.py IR --compress

📄 IR IP listesi
   ├─ Toplam IP    : 10,831,872
   ├─ Tahmini Boyut: 20.1 MB (sıkıştırılmış)
   ├─ Açık Hali     : 155.0 MB
   ├─ Çıkış Formatı: .gz (sıkıştırılmış)
   └─ Örnek Bloklar: 2.57.3.0/256, 2.144.0.0/262144, 2.176.0.0/1048576

❓ Bu dosyayı oluşturmak istediğinize emin misiniz? (y/n): y

🚀 IR IPleri oluşturuluyor...

✅ IR IP listesi oluşturuldu!
   ├─ Toplam IP: 10,825,666
   ├─ Dosya Boyutu: 21.9 MB
   ├─ Geçen Süre: 15.8 saniye
   └─ Dosya: data/ips/IR_ips.gz

┌──(root)-[/Ripe-ip-Dataset]
└─#
```
---

## 📅 Kaynaklar

- [RIPE NCC](https://ftp.ripe.net/pub/stats/ripencc/)
- [APNIC](https://ftp.apnic.net/pub/stats/apnic/)
- [ARIN](https://ftp.arin.net/pub/stats/arin/)
- [LACNIC](https://ftp.lacnic.net/pub/stats/lacnic/)
- [AFRINIC](https://ftp.afrinic.net/pub/stats/afrinic/)

---

## 📝 Lisans

MIT License - Özgürce kullanabilirsiniz.
