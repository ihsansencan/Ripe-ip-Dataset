#!/usr/bin/env python3
"""
create_ip.py - Ülke bazlı IPv4 IP listesi oluşturur

KULLANIM:
  python3 create_ip.py TR              # Türkiye
  python3 create_ip.py TR --compress   # Sıkıştırılmış çıktı (.gz)
  python3 create_ip.py all             # Tüm ülkeler
  python3 create_ip.py all --compress  # Tüm ülkeler (sıkıştırılmış)
  python3 create_ip.py list            # Ülkeleri listele
  python3 create_ip.py IR              # (IR) İran
"""

import ipaddress
import math
import os
import sys
import glob
import gzip
import signal
from datetime import datetime

# Ctrl+C
def signal_handler(sig, frame):
    print("\n\n⚠️ İşlem kullanıcı tarafından iptal edildi.")
    print("📁 Oluşturulan dosyalar kaydedildi.")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Renk
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_color(text, color=Colors.RESET, end='\n'):
    if sys.stdout.isatty():
        print(f"{color}{text}{Colors.RESET}", end=end)
    else:
        print(text, end=end)

def format_size(bytes_size):
    """Dosya boyutu"""
    if bytes_size < 0:
        return "0 B"
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} PB"

def estimate_ips_and_size(country):
    """Dosya boyutunu tahmin"""
    input_file = f'data/cidr_world/{country}_cidr.txt'
    
    if not os.path.exists(input_file):
        return None, None, None, None
    
    total_ips = 0
    sample_blocks = []
    
    try:
        with open(input_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or ':' in line:
                    continue
                try:
                    ip_str, size_str = line.split('/')
                    size = int(size_str)
                    if size > 0:
                        total_ips += size
                        if len(sample_blocks) < 3:
                            sample_blocks.append(f"{ip_str}/{size}")
                except:
                    continue
    except Exception:
        return None, None, None, None
    
    # Tahmin
    txt_size = total_ips * 15
    gz_size = txt_size * 0.13
    
    return total_ips, txt_size, gz_size, sample_blocks

def create_ip(country, compress=False, force=False):
    """Tek ülke için IP listesi oluşturur"""
    
    input_file = f'data/cidr_world/{country}_cidr.txt'
    output_dir = 'data/ips'
    os.makedirs(output_dir, exist_ok=True)
    
    # Dosya var mı kontrol et
    if not os.path.exists(input_file):
        print_color(f"❌ '{country}' ülkesi bulunamadı!", Colors.RED)
        print_color(f"📋 Mevcut ülkeleri görmek için: python3 create_ip.py list", Colors.YELLOW)
        return False
    
    # Tahmin
    total_ips, txt_size, gz_size, sample_blocks = estimate_ips_and_size(country)
    
    if total_ips is None or total_ips == 0:
        print_color(f"⚠️ '{country}' için IP bulunamadı!", Colors.YELLOW)
        return False
    
    # Output dosya adı
    ext = '.gz' if compress else '.txt'
    output_file = f'{output_dir}/{country}_ips{ext}'
    
    # Bilgileri göster
    print_color(f"\n📄 {country} IP listesi", Colors.CYAN)
    print(f"   ├─ Toplam IP    : {total_ips:,}")
    if compress:
        print(f"   ├─ Tahmini Boyut: {format_size(gz_size)} (sıkıştırılmış)")
        print(f"   ├─ Açık Hali     : {format_size(txt_size)}")
    else:
        print(f"   ├─ Tahmini Boyut: {format_size(txt_size)}")
    print(f"   ├─ Çıkış Formatı: {'.gz (sıkıştırılmış)' if compress else '.txt (düz metin)'}")
    print(f"   └─ Örnek Bloklar: {', '.join(sample_blocks[:3])}")
    
    # Uyarı
    check_size = gz_size if compress else txt_size
    if check_size > 100 * 1024 * 1024:  # 100 MB
        print_color(f"\n⚠️ BUYUK DOSYA UYARISI!", Colors.YELLOW)
        print(f"   Bu dosya yaklaşık {format_size(check_size)} olacak.")
        if compress:
            print(f"   Açık hali {format_size(txt_size)} olacak, sıkıştırılmış hali {format_size(gz_size)}.")
        print(f"   Oluşturulması birkaç dakika sürebilir.")
    
    # Onay
    if not force:
        print_color(f"\n❓ Bu dosyayı oluşturmak istediğinize emin misiniz? (y/n): ", Colors.CYAN, end='')
        response = input().strip().lower()
        if response not in ['y', 'yes', 'e', 'evet']:
            print_color("⏹️ İşlem iptal edildi.", Colors.YELLOW)
            return False
    
    # IP'leri oluştur
    print_color(f"\n🚀 {country} IP'leri oluşturuluyor...", Colors.GREEN)
    start_time = datetime.now()
    
    try:
        # Dosyayı aç (sıkıştırmalı veya düz)
        if compress:
            outfile = gzip.open(output_file, 'wt', encoding='utf-8', compresslevel=6)
        else:
            outfile = open(output_file, 'w', encoding='utf-8')
        
        with outfile:
            processed = 0
            with open(input_file, 'r') as infile:
                for line in infile:
                    line = line.strip()
                    if not line or ':' in line:
                        continue
                    
                    try:
                        ip_str, size_str = line.split('/')
                        size = int(size_str)
                        
                        # Prefix'i hesapla
                        if size > 0 and (size & (size - 1)) == 0:  # 2'nin kuvveti mi?
                            prefix = 32 - int(math.log2(size))
                            network = ipaddress.ip_network(f"{ip_str}/{prefix}", strict=False)
                            for ip in network.hosts():
                                outfile.write(f"{ip}\n")
                                processed += 1
                        else:
                            outfile.write(f"# {line}\n")
                    except Exception as e:
                        continue
                    
                    if processed % 100000 == 0 and processed > 0:
                        progress = (processed / total_ips) * 100
                        elapsed = (datetime.now() - start_time).total_seconds()
                        eta = (elapsed / processed) * (total_ips - processed) if processed > 0 else 0
                        print(f"  📊 İlerleme: {progress:.1f}% ({processed:,}/{total_ips:,}) - Geçen: {elapsed:.0f}s - Kalan: {eta:.0f}s")
        
        # Sonuç
        elapsed = (datetime.now() - start_time).total_seconds()
        file_size = os.path.getsize(output_file)
        print_color(f"\n✅ {country} IP listesi oluşturuldu!", Colors.GREEN)
        print(f"   ├─ Toplam IP: {processed:,}")
        print(f"   ├─ Dosya Boyutu: {format_size(file_size)}")
        print(f"   ├─ Geçen Süre: {elapsed:.1f} saniye")
        print(f"   └─ Dosya: {output_file}")
        return True
        
    except Exception as e:
        print_color(f"\n❌ Hata oluştu: {str(e)}", Colors.RED)
        return False

def create_all(compress=False, force=False):
    """Tüm ülkelerin IP listelerini oluşturur"""
    
    files = glob.glob('data/cidr_world/*_cidr.txt')
    
    if not files:
        print_color("❌ CIDR dosyası bulunamadı!", Colors.RED)
        return
    
    total_countries = len(files)
    
    print_color(f"\n🌍 Tüm ülkelerin IP listeleri oluşturulacak.", Colors.CYAN)
    print(f"   ├─ Ülke Sayısı: {total_countries}")
    print(f"   ├─ Çıkış Formatı: {'.gz (sıkıştırılmış)' if compress else '.txt (düz metin)'}")
    print(f"   └─ Bu işlem çok uzun sürebilir (saatler)!")
    
    if not force:
        print_color(f"\n❓ Devam etmek istediğinize emin misiniz? (y/n): ", Colors.CYAN, end='')
        response = input().strip().lower()
        if response not in ['y', 'yes', 'e', 'evet']:
            print_color("⏹️ İşlem iptal edildi.", Colors.YELLOW)
            return
    
    print_color(f"\n🚀 IP listeleri oluşturuluyor...", Colors.GREEN)
    
    success = 0
    for i, file in enumerate(sorted(files), 1):
        country = os.path.basename(file).replace('_cidr.txt', '')
        print_color(f"\n📄 {country} ({i}/{total_countries})", Colors.BLUE)
        if create_ip(country, compress, force=True):
            success += 1
    
    print_color(f"\n✅ TAMAMLANDI! {success}/{total_countries} ülke başarıyla oluşturuldu.", Colors.GREEN)

def list_countries():
    """Mevcut ülkeleri listeler"""
    files = glob.glob('data/cidr_world/*_cidr.txt')
    countries = sorted([os.path.basename(f).replace('_cidr.txt', '') for f in files])
    
    print_color(f"\n📋 MEVCUT ÜLKELER", Colors.CYAN)
    print(f"========================================")
    print(f"├─ Toplam Ülke Sayısı: {len(countries)}")
    print(f"\n📌 İlk 20 Ülke:")
    for i, country in enumerate(countries[:20], 1):
        print(f"  {i:>2}. {country}")
    if len(countries) > 20:
        print(f"  ... ve {len(countries) - 20} ülke daha")

def main():
    """Ana fonksiyon"""
    
    # Kullanım
    if len(sys.argv) < 2:
        print_color(f"\n📄 KULLANIM:", Colors.CYAN)
        print("  python3 create_ip.py <ülke_kodu>              # IPv4")
        print("  python3 create_ip.py <ülke_kodu> --compress   # Sıkıştırılmış (.gz)")
        print("  python3 create_ip.py all                      # Tüm ülkeler")
        print("  python3 create_ip.py all --compress           # Tüm ülkeler (sıkıştırılmış)")
        print("  python3 create_ip.py list                     # Ülkeleri listele")
        print("  python3 create_ip.py IR                       # (IR) İran")
        print(f"\n💡 Örnek: python3 create_ip.py IR --compress")
        sys.exit(0)
    
    # Parse
    args = sys.argv[1:]
    country = args[0].upper() if not args[0].startswith('--') else None
    flags = [arg for arg in args if arg.startswith('--')]
    
    compress = '--compress' in flags
    force = '--force' in flags
    
    # Listeleme
    if country == 'LIST':
        list_countries()
        return
    
    # Tüm ülkeler
    if country == 'ALL':
        create_all(compress, force)
        return
    
    # Tek ülke
    create_ip(country, compress, force)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print_color("\n\n⚠️ İşlem kullanıcı tarafından iptal edildi.", Colors.YELLOW)
        print("📁 Oluşturulan dosyalar kaydedildi.")
        sys.exit(0)
    except Exception as e:
        print_color(f"\n❌ Beklenmeyen hata: {str(e)}", Colors.RED)
        sys.exit(1)