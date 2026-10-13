import requests
import json
import os
import re
from datetime import datetime
from bs4 import BeautifulSoup

def should_skip_artikel(title):
    """
    Cek apakah artikel harus di-skip berdasarkan tahun di title
    Skip jika title mengandung tahun 2024 atau lebih lama (2023, 2022, dll)
    Bahkan jika ada tahun yang lebih baru juga (misal: "2024/2025" tetap di-skip)
    """
    if not title:
        return False
    
    # Cari semua tahun 4 digit di title
    years = re.findall(r'\b(19\d{2}|20\d{2})\b', title)
    
    if years:
        # Cek apakah ada tahun yang <= 2024
        # Jika ada, skip (tidak peduli ada tahun yang lebih baru)
        for year in years:
            if int(year) <= 2024:
                return True
    
    return False

def scrape_artikel_content_from_list(artikel_list):
    """
    Ambil konten dari setiap artikel dalam list
    """
    artikel_with_content = []
    total = len(artikel_list)
    
    for idx, artikel in enumerate(artikel_list, 1):
        title = artikel.get('Title', '')
        url = artikel.get('Url', '')
        
        # Skip artikel yang title-nya mengandung tahun 2024 atau lebih lama
        if should_skip_artikel(title):
            print(f"⏭️  [{idx}/{total}] Skip (tahun <= 2024): {title[:50]}...")
            continue
        
        if not url:
            print(f"⚠️  Artikel {idx}/{total}: Skip (tidak ada URL)")
            continue
        
        try:
            print(f"🔄 [{idx}/{total}] Mengambil konten: {title[:50]}...")
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Parse HTML dengan BeautifulSoup
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Cari tag <article>
            article_tag = soup.find('article')
            
            if article_tag:
                # Ambil semua teks dari tag <article>
                article_text = article_tag.get_text(separator=' ', strip=True)
                
                artikel_with_content.append({
                    'Title': title,
                    'Url': url,
                    'Content': article_text
                })
                print(f"✅ [{idx}/{total}] Berhasil mengambil konten")
            else:
                print(f"⚠️  [{idx}/{total}] Tag <article> tidak ditemukan")
                artikel_with_content.append({
                    'Title': title,
                    'Url': url,
                    'Content': ''
                })
                
        except requests.exceptions.RequestException as e:
            print(f"❌ [{idx}/{total}] Error saat mengambil artikel: {e}")
            artikel_with_content.append({
                'Title': title,
                'Url': url,
                'Content': ''
            })
        except Exception as e:
            print(f"❌ [{idx}/{total}] Error tidak terduga: {e}")
            artikel_with_content.append({
                'Title': title,
                'Url': url,
                'Content': ''
            })
    
    return artikel_with_content

def scrape_artikel_content(json_file_path=None):
    """
    Baca file JSON arsip artikel, lalu hit setiap URL artikel
    Ambil teks dari tag <article> dan simpan ke JSON baru
    """
    # Jika tidak ada path, cari file JSON terbaru di direktori yang sama
    if json_file_path is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_files = [f for f in os.listdir(script_dir) if f.startswith('arsip_artikel_') and f.endswith('.json')]
        if not json_files:
            print("❌ Tidak ada file JSON arsip ditemukan!")
            return None, None
        json_file_path = os.path.join(script_dir, sorted(json_files)[-1])  # Ambil yang terbaru
        print(f"📂 Menggunakan file: {os.path.basename(json_file_path)}")
    
    try:
        # Baca file JSON arsip
        with open(json_file_path, 'r', encoding='utf-8') as f:
            arsip_data = json.load(f)
        
        print(f"📖 Membaca {len(arsip_data)} artikel dari file JSON...")
        
        # Process setiap artikel
        artikel_with_content = []
        total = len(arsip_data)
        
        for idx, artikel in enumerate(arsip_data, 1):
            title = artikel.get('Title', '')
            url = artikel.get('Url', '')
            
            # Skip artikel yang title-nya mengandung tahun 2024 atau lebih lama
            if should_skip_artikel(title):
                print(f"⏭️  [{idx}/{total}] Skip (tahun <= 2024): {title[:50]}...")
                continue
            
            if not url:
                print(f"⚠️  Artikel {idx}/{total}: Skip (tidak ada URL)")
                continue
            
            try:
                print(f"🔄 [{idx}/{total}] Mengambil konten: {title[:50]}...")
                response = requests.get(url, timeout=30)
                response.raise_for_status()
                
                # Parse HTML dengan BeautifulSoup
                soup = BeautifulSoup(response.text, 'lxml')
                
                # Cari tag <article>
                article_tag = soup.find('article')
                
                if article_tag:
                    # Ambil semua teks dari tag <article>
                    article_text = article_tag.get_text(separator=' ', strip=True)
                    
                    artikel_with_content.append({
                        'Title': title,
                        'Url': url,
                        'Content': article_text
                    })
                    print(f"✅ [{idx}/{total}] Berhasil mengambil konten")
                else:
                    print(f"⚠️  [{idx}/{total}] Tag <article> tidak ditemukan")
                    artikel_with_content.append({
                        'Title': title,
                        'Url': url,
                        'Content': ''
                    })
                    
            except requests.exceptions.RequestException as e:
                print(f"❌ [{idx}/{total}] Error saat mengambil artikel: {e}")
                artikel_with_content.append({
                    'Title': title,
                    'Url': url,
                    'Content': ''
                })
            except Exception as e:
                print(f"❌ [{idx}/{total}] Error tidak terduga: {e}")
                artikel_with_content.append({
                    'Title': title,
                    'Url': url,
                    'Content': ''
                })
        
        # Simpan hasil ke JSON
        output_filename = f"artikel_content_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        output_path = os.path.join(os.path.dirname(json_file_path), output_filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(artikel_with_content, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Data berhasil disimpan ke {output_filename}")
        print(f"📊 Total artikel yang diproses: {len(artikel_with_content)}")
        print(f"✅ Artikel dengan konten: {sum(1 for a in artikel_with_content if a['Content'])}")
        
        return artikel_with_content, output_path
    
    except FileNotFoundError:
        print(f"❌ File tidak ditemukan: {json_file_path}")
        return None, None
    except json.JSONDecodeError as e:
        print(f"❌ Error saat parsing JSON: {e}")
        return None, None
    except Exception as e:
        print(f"❌ Error tidak terduga: {e}")
        return None, None

def scrape_pipeline():
    """
    Pipeline lengkap: Scrape arsip dari API, lalu langsung ambil konten setiap artikel
    """
    url = "https://daak.amikom.ac.id/api/artikel/arsip"
    
    try:
        # Step 1: Scrape arsip dari API
        print("=" * 60)
        print("📥 STEP 1: Mengambil data arsip dari API...")
        print("=" * 60)
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        print(f"✅ Berhasil mengambil data! Total artikel: {len(data['data'])}")
        
        # Process data: ambil Title dan UrlTitle, lalu transform UrlTitle
        # Filter artikel yang tahunnya <= 2024
        processed_data = []
        skipped_count = 0
        for item in data['data']:
            if 'Title' in item and 'UrlTitle' in item:
                title = item['Title']
                
                # Skip artikel yang title-nya mengandung tahun 2024 atau lebih lama
                if should_skip_artikel(title):
                    skipped_count += 1
                    continue
                
                processed_item = {
                    'Title': title,
                    'Url': f"https://daak.amikom.ac.id/artikel/{item['UrlTitle']}"
                }
                processed_data.append(processed_item)
        
        print(f"📊 Total artikel yang akan diproses: {len(processed_data)}")
        print(f"⏭️  Artikel yang di-skip (tahun <= 2024): {skipped_count}\n")
        
        # Step 2: Scrape konten dari setiap artikel
        print("=" * 60)
        print("📄 STEP 2: Mengambil konten dari setiap artikel...")
        print("=" * 60)
        artikel_with_content = scrape_artikel_content_from_list(processed_data)
        
        # Step 3: Simpan hasil akhir ke JSON
        print("\n" + "=" * 60)
        print("💾 STEP 3: Menyimpan hasil ke JSON...")
        print("=" * 60)
        output_filename = f"artikel_complete_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(script_dir, output_filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(artikel_with_content, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Data berhasil disimpan ke {output_filename}")
        print(f"📊 Total artikel yang diproses: {len(artikel_with_content)}")
        print(f"✅ Artikel dengan konten: {sum(1 for a in artikel_with_content if a['Content'])}")
        print(f"⚠️  Artikel tanpa konten: {sum(1 for a in artikel_with_content if not a['Content'])}")
        
        return artikel_with_content, output_path
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error saat mengambil data dari API: {e}")
        return None, None
    except json.JSONDecodeError as e:
        print(f"❌ Error saat parsing JSON: {e}")
        return None, None
    except Exception as e:
        print(f"❌ Error tidak terduga: {e}")
        return None, None

if __name__ == "__main__":
    scrape_pipeline()
