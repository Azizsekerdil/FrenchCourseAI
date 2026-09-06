# French Course AI

French Course AI, Fransızca öğrenimi için yerel veriyi önceleyen bağımsız bir Windows masaüstü uygulamasıdır. Türkçe, English ve Français arayüzleri aynı özellik derinliğini sunar; kelime, aksan, telaffuz ve dilbilgisi içeriği Fransızca için özgün hazırlanmıştır.

> Temel çalışma özellikleri ve öğrenci verileri yereldir. Kaynak bağlantılarını açmak ve isteğe bağlı uzak servisleri kullanmak internet gerektirir; uygulama bu nedenle yanıltıcı bir “%100 çevrimdışı” iddiasında bulunmaz.

## Öne çıkan özellikler

- SM-2 ve Leitner tabanlı aralıklı tekrar; günlük hedef ve seri
- 160'ın üzerinde yerleşik A1 kelime; isimlerde artikel, cinsiyet ve çoğul
- Fransızca-Türkçe-İngilizce sözlük, favoriler ve yanlış kelimeler
- Çift yönlü **Fransızca ↔ İngilizce sözlük** sekmesi: 1.210+ gömülü madde (cinsiyet + düzensiz çoğul), yön otomatik, aksan/œ/elision toleranslı arama, seslendirme, kelime bankasına ekleme, CSV/TSV içe/dışa aktarma
- **AI destekli sözlük**: sözlükte bulunmayan kelimeler LM Studio'ya ya da alternatif bir OpenAI uyumlu uç noktaya (NVIDIA NIM veya herhangi bir URL + API anahtarı) yapılandırılmış JSON olarak sorulur; sonuçlar (cinsiyet/çoğul, çeviri, örnek cümle, not) yerel sözlüğe önbelleklenir ve sonraki aramalar çevrimdışı çalışır
- Kart, çoktan seçmeli, yazma, dinleme ve eşleştirme çalışma seçenekleri
- CEFR A1-C1 profili ve puanlanan sınav motoru
- `é è ê ë à â î ï ô ù û ü ç`, apostrof, élision, liaison, sessiz son harf, burun ünlüsü, `r`, `u/ou`, ritim ve dikte laboratuvarı
- Artikel, cinsiyet, çoğul, sıfat uyumu/konumu, zamirler, `y/en`, fiil grupları, olumsuzluk, sorular, temel zamanlar, emir, dönüşlü fiiller, edatlar ve partitif konuları
- Telaffuz, konuşma, serbest yazma ve el yazısı alanı
- Yerel PDF metin okuma ve sayfa notları
- Lisans ve atıf bilgili açık Kaynak Merkezi
- LM Studio ile yerel AI öğretmen; açıklama, çeviri, düzeltme, konuşma ve görsel/OCR görevleri
- Göreve göre model profilleri ve metin içermeyen token defteri
- Haftalık ilerleme raporu, açık/koyu tema ve öğrenci profilleri
- Unicode CSV ve `.fcapack` paket içe/dışa aktarımı

## Kurulum ve kaynaktan çalıştırma

Gereksinim: Python 3.11 veya üzeri.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python .\French_Course_AI.pyw
```

Öğrenci verileri `%APPDATA%\FrenchCourseAI` altında tutulur. Test veya taşınabilir deneme için `FCA_HOME` ortam değişkeniyle ayrı bir klasör seçilebilir.

## Windows EXE üretimi

```powershell
python -m pip install -r requirements-dev.txt
.\build.bat
```

Çıktı: `dist\FrenchCourseAI.exe`. `build`, `dist` ve kullanıcı verileri Git deposuna alınmaz.

## Yerel AI kurulumu

1. LM Studio'yu kurun ve bir sohbet modeli indirin.
2. OpenAI uyumlu Local Server'ı başlatın.
3. Varsayılan adres `http://127.0.0.1:1234` değeridir.
4. Uygulama içindeki Ayarlar sayfasından görev modelini veya adresi değiştirin.

LM Studio kapalıysa uygulama çalışmaya devam eder; yalnız AI özellikleri devre dışı kalır. Prompt ve AI yanıt metinleri veritabanına yazılmaz. Token defteri yalnız model, görev, token sayıları, süre ve başarı durumunu saklar.

### Sözlük için AI sağlayıcısı

Sözlük sekmesi iki sağlayıcı kullanabilir:

- **LM Studio** (yerel, anahtar gerekmez) — `app.ai`, yukarıdaki adres.
- **Alternatif uç nokta** — herhangi bir OpenAI uyumlu API: varsayılan `https://integrate.api.nvidia.com/v1` (NVIDIA NIM, model `meta/llama-3.1-8b-instruct`); OpenRouter, Groq veya Ollama gibi başka bir temel URL, model adı ve API anahtarı da girilebilir. Anahtar istemeyen bir sunucu için (ör. ağdaki başka bir bilgisayarda çalışan Ollama/LM Studio) anahtar alanı boş bırakılır; anahtarın gerekip gerekmediğine adres değil sunucu karar verir. Model adı yazıldığı gibi gönderilir. Ayarlar sayfasında etkinleştirilir, "Bağlantıyı test et" ile denenir; sözlük de aynı `GET /v1/models` sınamasını kullanır.

Ayarlardaki (ve sözlük araç çubuğundaki) **Sözlük AI kaynağı** politikası: `Otomatik` (LM Studio erişilebilirse o, değilse etkin ve erişilebilirse alternatif), `LM Studio`, `Alternatif` veya `Kapalı`. Sözlükte sonuç çıkmazsa AI arka planda sorulur; bulunan maddeler `AI` kaynağıyla listelenir ve (varsayılan olarak) `dict_entries` tablosuna kaydedilir. "AI'a sor" düğmesi yerel sonuç olsa bile AI maddelerini listenin üstüne ekler.

API anahtarı Windows Kimlik Bilgisi Yöneticisi'nde (`FrenchCourseAI/alt_api_key`) saklanır; Windows dışında veya API başarısız olursa `settings/secrets.json` dosyasına düşer. Anahtar hiçbir zaman `settings.json` içine yazılmaz. `FRENCHCOURSEAI_API_KEY` ortam değişkeni kayıtlı anahtarı geçersiz kılar.

## Gizlilik ve internet

- Profil, ilerleme, sınav, PDF notları ve sayaçlar ayrı SQLite veritabanında yerel saklanır.
- SRS, sınav, sözlük, dilbilgisi ve paket özellikleri internet olmadan çalışır.
- Kaynak Merkezi bağlantıları yalnız kullanıcı eylemiyle açılır ve internet kullanır.
- Uzak AI servisleri isteğe bağlıdır ve varsayılan olarak kapalıdır; API anahtarı Kimlik Bilgisi Yöneticisi'nde tutulur, ayar dosyasına yazılmaz.

## Testler

```powershell
python -m pytest -q
```

Testler pencere/18 sayfa kurulumu, anlık ve kalıcı dil değişimi, i18n bütünlüğü, SQLite geçişi, 150+ kelime, 1.210+ maddelik sözlük motoru (iki yönlü arama, içe/dışa aktarma, SQLite kullanıcı maddeleri), yerel sahte OpenAI sunucusuyla AI sözlük araması (JSON ayrıştırma, Bearer başlığı, sağlayıcı seçimi, sözlük sekmesi akışı), gizli anahtar deposu (dosya arka ucu), `dict_entries` şema geçişi, SRS, kart/sınav akışı, aksansız ve apostrofsuz arama, aksan-duyarlı doğru yazım, Unicode CSV, AI çevrimdışı davranışı, token gizliliği ve paket turunu kapsar. Testler gerçek ağa ya da Kimlik Bilgisi Yöneticisi'ne asla dokunmaz.

## Proje yapısı

```text
French_Course_AI.pyw    Uygulama girişi
fca/                    Bağımsız Python paketi
  app.py                Tkinter kabuğu ve dil seçici
  tabs/                 Modüler öğrenme, laboratuvar, okuma ve sistem sayfaları
  db.py                 SQLite şema, geçiş ve depolar
  srs.py                SM-2 / Leitner hesapları
  content.py            Fransızcaya özgü laboratuvar içeriği
  seed_words.py         Özgün A1 başlangıç sözlüğü
  dictionary.py         Sözlük motoru ve yapılandırılmış AI araması
  dict_data.py          Gömülü FR-EN sözlük verisi
  ai_client.py          OpenAI uyumlu istemci (LM Studio, NIM, ...) ve sağlayıcı seçimi
  secrets.py            API anahtarı deposu (Kimlik Bilgisi Yöneticisi / dosya)
tests/                  Otomatik testler
grammar/                Çevrimdışı dilbilgisi notları
Resources/              Kullanıcının ders dosyaları
docs/presentation/      Düzenlenebilir PPTX, PDF ve ekran görüntüleri
```

## Açık kaynak kataloğu

Katalog bağlantı sunar; içeriği izinsiz paketlemez. Wikibooks (CC BY-SA), Tatoeba (CC BY 2.0 FR / seçili CC0), LibriVox ve Project Gutenberg kamu malı koleksiyonları lisans ve atıf bilgisiyle gösterilir. Kamu malı durumu ülkeye göre değişebileceğinden uyarılar korunur.
