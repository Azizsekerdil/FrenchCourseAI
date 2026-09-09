# French Course AI — Kullanım Kılavuzu

Sürüm 1.3.0 · Windows ve macOS masaüstü uygulaması · Arayüz dilleri: Türkçe, English, Français

## İçindekiler

- [1. Bu kılavuz hakkında](#1-bu-kılavuz-hakkında)
- [2. Kurulum](#2-kurulum)
- [3. Uygulamayı ilk kez açmak](#3-uygulamayı-ilk-kez-açmak)
- [4. Ekranlar](#4-ekranlar)
- [5. Sözlük (ayrıntılı)](#5-sözlük-ayrıntılı)
- [6. Yapay zeka](#6-yapay-zeka)
- [7. Veri yönetimi](#7-veri-yönetimi)
- [8. Kısayollar ve ipuçları](#8-kısayollar-ve-ipuçları)
- [9. Sorun giderme](#9-sorun-giderme)
- [10. Sürüm notları özeti](#10-sürüm-notları-özeti)
- [11. Sık sorulan sorular](#11-sık-sorulan-sorular)
- [12. Lisans](#12-lisans)

---

## 1. Bu kılavuz hakkında

French Course AI, Fransızca öğrenenler için bağımsız bir masaüstü uygulamasıdır. Bu kılavuz **sürüm 1.3.0**'ı anlatır ve tek başına okunabilir: hiçbir adım için başka bir belgeye ihtiyacınız yoktur.

Kılavuz, ana dili Türkçe olan ve Fransızcada A1-B1 aralığında ilerleyen bir öğrenci için yazıldı. Yeni kurduysanız baştan sona okuyun; günlük kullanımda ilgili bölüme atlayın. [4. Ekranlar](#4-ekranlar) 18 sayfayı kenar çubuğundaki sırayla anlatır; [5. Sözlük](#5-sözlük-ayrıntılı) ve [6. Yapay zeka](#6-yapay-zeka) sürüm 1.2.1'in en çok değişen parçalarıdır.

Düğme ve alan adları Türkçe arayüzde göründüğü gibi yazılmıştır; yararlı olduğu yerde İngilizcesi parantez içindedir. Temel işlevler internetsiz çalışır; yalnızca Kaynak Merkezi bağlantıları ve isteğe bağlı alternatif yapay zeka uç noktası internet kullanır.

## 2. Kurulum

Kurulum sihirbazı, Python ya da yönetici hakkı gerekmez; paketler taşınabilirdir.

### 2.1 Windows (zip)

1. `FrenchCourseAI-Windows.zip` dosyasını indirin.
2. Zip'i sağ tıklayıp **Tümünü ayıkla** ile bir klasöre açın.
3. `FrenchCourseAI.exe` dosyasına çift tıklayın; kurulum yapılmaz, uygulama doğrudan açılır.
4. SmartScreen uyarısı çıkarsa **Ek bilgi → Yine de çalıştır** deyin.

Zip üç dosya içerir: `FrenchCourseAI.exe`, `LICENSE` ve `THIRD_PARTY_NOTICES.md`. `assets`, `Resources` ve `grammar` klasörleri .exe'nin içine paketlenmiştir; iki lisans dosyası hem .exe'nin yanında hem de içinde bulunur. Zip'i önce bir klasöre ayıklayın ve .exe'yi oradan çalıştırın.

### 2.2 macOS (zip, Apple Silicon)

`FrenchCourseAI-macOS.zip` paketi Apple Silicon (arm64) içindir ve **notarize edilmemiştir**:

1. Zip'e çift tıklayıp `FrenchCourseAI.app` paketini **Uygulamalar** klasörüne taşıyın. (Zip'te uygulamanın yanında `LICENSE` ve `THIRD_PARTY_NOTICES.md` dosyaları da vardır; aynı metinler `.app` paketinin içine de kopyalanır.)
2. Uygulamaya **sağ tıklayın** (ya da Control ile tıklayın) ve **Aç** seçin.
3. Uyarı penceresinde yine **Aç** düğmesine basın.

Bu adım yalnızca ilk açılışta gereklidir; çift tıklarsanız macOS "açılamıyor" uyarısı verir (bkz. [9. Sorun giderme](#9-sorun-giderme)).

### 2.3 Kaynaktan çalıştırma

Python 3.11 veya üzeri gerekir; tek çalışma bağımlılığı PDF okuma için `pypdf`'tir.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python .\French_Course_AI.pyw
```

Kendi `.exe` dosyanız için `python -m pip install -r requirements-dev.txt` ardından `.\build.bat` (çıktı `dist\FrenchCourseAI.exe`); macOS paketi bir Mac üzerinde `./build_macos.sh` ile üretilir (çıktı `dist/FrenchCourseAI-macOS.zip`).

### 2.4 Verileriniz nerede tutulur

| Platform | Veri klasörü |
| --- | --- |
| Windows | `%APPDATA%\FrenchCourseAI` |
| macOS | `~/Library/Application Support/FrenchCourseAI` |
| Linux | `~/.frenchcourseai` |

İçinde dört alt klasör oluşur: `data` (SQLite veritabanı `FrenchCourseAI.db`), `settings` (`settings.json`, gerekirse `secrets.json`), `exports` ve `downloads`.

Taşınabilir kullanım için **`FCA_HOME`** ortam değişkeniyle başka bir klasör seçin; uygulama bütün verisini orada oluşturur ve varsayılan klasöre dokunmaz:

```powershell
$env:FCA_HOME = "D:\FransizcaVerim"
.\FrenchCourseAI.exe
```

## 3. Uygulamayı ilk kez açmak

Pencere 1360 × 860 boyutunda gelir (en küçük 1080 × 700): solda 18 sayfalık gruplu kenar çubuğu, üstte sayfa başlığı ile profil, dil ve AI göstergesi, altta durum çubuğu. Uygulama **Aralıklı Tekrar** sayfasında açılır. İlk açılışta arka planda şunlar hazırlanır:

- **Profil.** `Alex` adında varsayılan bir profil oluşur. Üstteki **+** düğmesi yeni profil ekler, yanındaki liste profiller arasında geçirir. İlerleme, sınav ve notlar profil bazlıdır; kelimeler ve sözlük ortaktır.
- **Arayüz dili.** 🌐 simgesinin yanındaki listede **Türkçe · English · Français** vardır (varsayılan Türkçe); seçim anında uygulanır ve kaydedilir.
- **Tema.** Varsayılan koyudur; **Ayarlar → Tema** satırından `dark` / `light` seçip **Kaydet** dediğinizde pencere yeniden çizilir.
- **Günlük hedef.** Varsayılan 20; Ayarlar'dan 5-200 arasına alınır ve İlerleme sayfasında gösterilir.
- **Veriler.** 162 A1 kelimesi veritabanına yazılır, 1.219 maddelik gömülü sözlük belleğe yüklenir. İkisi de uygulamanın içindedir, indirme gerektirmez.

Sağ üstteki **AI:** rozeti kısa süre sonra LM Studio adresini yoklar ve **Kullanılabilir** ya da **Kullanılamıyor** yazar; LM Studio yoksa yalnızca yapay zeka özellikleri beklemeye alınır.

## 4. Ekranlar

Kenar çubuğu beş gruba ayrılır; 18 sayfa aşağıda kenar çubuğundaki sırayla anlatılır.

| Grup | Sayfalar |
| --- | --- |
| **ÖĞREN** | Aralıklı Tekrar · Kelime Bankası · Sözlük FR-EN-TR · Sınav |
| **LABORATUVARLAR** | Yazım ve Ses · Telaffuz · Dilbilgisi |
| **OKU & KEŞFET** | Kaynak Merkezi · PDF Okuyucu · Ders Kitaplığı |
| **PRATİK** | AI Öğretmen · Konuşma · Yazma & El Yazısı |
| **İLERLEME & SİSTEM** | İlerleme · Paketler · Token Defteri · Çevrimdışı Kılavuz · Ayarlar |

### 4.1 ÖĞREN grubu

**Aralıklı Tekrar (Spaced Review)** — kelimeleri unutma eğrisine göre tekrar ettirir; dört kutu **Bugün**, **Yeni**, **Yanlışlar** ve **Favoriler** sayılarını gösterir.
*Nasıl:* kuyruktan `new`, `due`, `wrong` ya da `favorites` (bu kodlar her arayüz dilinde İngilizcedir), moddan **Kart**, **Çoktan seçmeli**, **Yazma**, **Dinleme** veya **Eşleştirme**'yi ve 5-50 arası kart sayısını (varsayılan 10) seçip **Başlat**'a basın; **Cevabı göster** karşılıkları açar, sonra **Tekrar**, **Zor**, **İyi** ya da **Kolay** ile puan verirsiniz.
*İpucu:* Bu sürümde mod seçimi yalnızca **Dinleme**'yi etkiler — kart açılırken kelime seslendirilir; **Çoktan seçmeli**, **Yazma** ve **Eşleştirme** aynı kart akışını çalıştırır. "Kolay" dedikleriniz uzayan aralıklara atılır.

**Kelime Bankası (Word Bank)** — tekrar ve sınavın beslendiği kişisel listeniz; sütunlar **Fransızca**, **Türkçe**, **İngilizce**, **Artikel**, **Çoğul**, **Deste**.
*Nasıl:* kutuya yazıp **Ara**'ya (veya Enter'a) basın; arama üç dilde çalışır ve satır seçince örnek cümleler görünür. **★ Favori** favorilere alır/çıkarır, **↑ Dışa aktar** UTF-8 CSV yazar, **↓ İçe aktar** okur.
*İpucu:* Sözlükten eklediğiniz kelimeler `Sözlük FR-EN-TR` destesine düşer.

**Sözlük FR-EN-TR (Dictionary FR-EN-TR)** — bu sayfanın tamamı [5. bölümde](#5-sözlük-ayrıntılı) anlatılır.

**Sınav (Exam)** — kelime bankasından rastgele kelimelerle çoktan seçmeli sınav üretir ve yüzde olarak puanlar.
*Nasıl:* **Soru sayısı**'nı 5-50 arasında ayarlayıp (varsayılan 10) **Başlat**'a basın; her soruda dört Türkçe seçenekten birini işaretleyip **Kontrol et**'e basarsınız, sonda **Sınav bitti** ve **Puan: …%** görünür (puan bir ondalıkla yazılır, örneğin `Puan: 80.0%`).
*İpucu:* Sonuç haftalık rapora işlenir ve İlerleme grafiğinde görünür.

### 4.2 LABORATUVARLAR grubu

**Yazım ve Ses (Spelling & Sound)** — yazım işaretlerini tanıtır ve dikte yaptırır; tabloda `A–Z`, `é`, `è / ê / ë`, `à / â`, `î / ï`, `ô`, `ù / û / ü`, `ç`, `'`, `liaison`, `finale`, `nasales`, `r`, `u / ou`, `rythme` satırları vardır.
*Nasıl:* soldan satırı seçin, sağda kuralı belirir. **Dikte alıştırması**'nda **▶ Seslendir** kutudaki kelimeyi okur; duyduğunuzu yazıp **Kontrol et** deyin — doğruysa ✓, yanlışsa `→` ile doğru yazım çıkar.
*İpucu:* Hazır kelimeyi silip kendi kelimenizi yazın. Karşılaştırma **aksana duyarlıdır**: `eleve` ile `élève` farklı sayılır.

**Telaffuz (Pronunciation)** — yazdığınız kelimeyi seslendirir ve dokuz ses grubunu (`r`, `u / ou`, `on`, `an / en`, `in / ain`, `eu / œu`, `é / è`, `oi`, `ch / j`) IPA ve örneklerle listeler.
*Nasıl:* kutuya kelimeyi yazın ve **▶ Seslendir**'e basın.
*İpucu:* **◉ Mikrofonla karşılaştır** bu sürümde etkin değildir; bastığınızda **Kullanılamıyor** yazar.

**Dilbilgisi (Grammar)** — 29 konuluk laboratuvar: `Belirli artikeller`, `İsim cinsiyetleri`, `Sıfat uyumu`, `y ve en`, `Passé composé`, `Elision ve liaison` ve benzerleri.
*Nasıl:* soldan konuyu seçin, sağda kural ve örnek belirir; **Alıştırma** altındaki şıkkı işaretleyip **Kontrol et**'e basın, **Sonraki** yeni alıştırma getirir.
*İpucu:* 18 soruluk havuz konudan bağımsız gelir; doğru/yanlış sayınız, seçtiğiniz konuya değil, gelen alıştırmanın kendi konusuna yazılır. Havuz 29 konunun 18'ini kapsadığı için kalan konular hiç sayaç almaz.

### 4.3 OKU & KEŞFET grubu

**Kaynak Merkezi (Resource Center)** — dört açık lisanslı dış kaynağı (Wikibooks, Tatoeba, LibriVox, Project Gutenberg) düzey, **Lisans:** ve **Atıf:** bilgisiyle listeler.
*Nasıl:* karttaki **Aç ↗** düğmesi bağlantıyı varsayılan tarayıcınızda açar.
*İpucu:* En üstte **ⓘ Bağlantıları açmak internet kullanır.** uyarısı durur; uygulama içerikleri paketlemez.

**PDF Okuyucu (PDF Reader)** — yerel bir PDF'in metnini sayfa sayfa gösterir ve her sayfa için ayrı not tutar.
*Nasıl:* **PDF seç** ile dosyayı açın, **Sayfa** sayacıyla gezinin, sağdaki **Sayfa notu** alanına yazıp **Kaydet**'e basın; not profil + dosya + sayfaya bağlanır ve geri döndüğünüzde yüklenir.
*İpucu:* Son açtığınız PDF kaydedilir. Taranmış PDF'lerde metin boş kalır; böyle bir belge için **Görsel / OCR** görevini kullanın.

**Ders Kitaplığı (Course Library)** — uygulamanın yanındaki `Resources` klasörünü **Ad**, **Tür** ve **MB** sütunlarıyla listeler.
*Nasıl:* **Ders klasörünü aç** klasörü Gezgin'de açar, **Yenile** listeyi günceller, satıra çift tıklamak dosyayı varsayılan uygulamada açar.
*İpucu:* Alt klasörler de taranır; derslerinizi konuya göre klasörleyebilirsiniz. Kaynaktan çalıştırırken uygulamanın yanındaki `Resources` klasörü listelenir; paketlenmiş .exe'de bu klasör her açılışta geçici bir klasöre çıkarılır ve uygulama kapanınca silinir, bu yüzden kalıcı ders dosyalarınızı orada tutmayın.

### 4.4 PRATİK grubu

**AI Öğretmen (AI Tutor)** — yerel modelle dört görev: **Açıkla**, **Çevir**, **Düzelt**, **Görsel / OCR**.
*Nasıl:* **Görev**'i seçin, metninizi yazıp **Gönder**'e basın. Görsel görevinde önce **Görsel / OCR** düğmesiyle bir `.png`, `.jpg`, `.jpeg` ya da `.webp` seçin; metin kutusu boşsa hazır bir istem kullanılır.
*İpucu:* Altta **🔒 Prompt ve yanıt metni kaydedilmez; yalnızca token sayıları tutulur.** yazar; AI erişilemiyorsa **AI kapalı veya LM Studio erişilemiyor.** görünür.

**Konuşma (Speaking)** — beş senaryoda yazışmalı rol yapma: `Au café`, `À la gare`, `À l'hôtel`, `Dans un magasin`, `Chez le médecin`.
*Nasıl:* **Senaryo** seçip **Konuşmayı başlat**'a basın; model kısa bir soru sorar, siz alttaki kutuya Fransızca yanıtınızı yazıp **Gönder** dersiniz.
*İpucu:* Bu sayfa yalnızca yerel LM Studio'yu kullanır; alternatif uç nokta sadece sözlük içindir.

**Yazma & El Yazısı (Writing & Handwriting)** — solda serbest yazma ve AI düzeltmesi, sağda fareyle yazı çalışma alanı.
*Nasıl:* yönerge **Bugün ne yaptığınızı Fransızca yazın.** der; metni yazıp **AI ile düzelt**'e basın, düzeltilmiş metin ve kural açıklaması alt kutuya gelir. **El yazısı alanı**'nda fareyle yazar, **Temizle** ile boşaltırsınız.
*İpucu:* Çizim alanı kaydedilmez; sayfayı kapatınca kaybolur.

### 4.5 İLERLEME & SİSTEM grubu

**İlerleme (Progress)** — **Günlük hedef**, **Günlük seri**, **Çalışılan** ve **Öğrenilen** kutuları, son yedi günün çubuk grafiği ve **Haftalık rapor** satırı (Doğru · Yanlış · Puan).
*Nasıl:* sayfaya girmeniz yeter; "Çalışılan" en az bir kez yanıtladığınız kelimeler, "Öğrenilen" Leitner kutusu 4 ve üzerindekiler, her çubuk o günkü doğru + yanlış toplamıdır.
*İpucu:* "Günlük seri" kesintisiz çalıştığınız gün sayısıdır ve bir gün atlayınca sıfırlanır.

**Paketler (Packs)** — kelime bankanızı (isteğe bağlı ilerlemeyle) tek bir `.fcapack` dosyasına yazar ve geri okur.
*Nasıl:* **İlerlemeyi ekle** işaretliyse profilin tekrar verisi de pakete girer; **↑ Dışa aktar** kaydeder, **↓ İçe aktar** açar ve **Paket oluşturuldu** ya da **Paket içe aktarıldı** görünür.
*İpucu:* Paketler hedef dile göre etiketlenir; başka bir dilin paketi reddedilir.

**Token Defteri (Token Ledger)** — **Çağrı** ve **Toplam token** kutuları ile son 500 çağrının tablosu: `Ts`, `Model`, `Task`, `Prompt Tokens`, `Completion Tokens`, `Total Tokens`, `Ms`, `Ok`.
*Nasıl:* sayfayı açıp listeyi okuyun; hangi modelin hangi görevde ne kadar token harcadığını görürsünüz.
*İpucu:* Tabloda hiçbir istem ya da yanıt metni yoktur; maliyet takibinin kaynağıdır.

**Çevrimdışı Kılavuz (Offline Guide)** — hangi özelliğin yerel, hangisinin internete bağlı olduğunu özetler ve en altta veri klasörünüzün tam yolunu yazar.
*Nasıl:* sayfayı açıp metni okuyun; sözlük yönleri, AI politikası, anahtarın yeri ve CSV düzeni burada da özetlenir.
*İpucu:* Yedek alırken veri klasörü yolunu buradan okuyun.

**Ayarlar (Settings)** — uygulamanın bütün kalıcı tercihleri.

| Ayar | Değer | Varsayılan |
| --- | --- | --- |
| **Tema** | `dark` / `light` | `dark` |
| **Günlük hedef** | 5-200 | 20 |
| **Seslendirme** | açık / kapalı | açık |
| **Yerel AI** | açık / kapalı | açık |
| **LM Studio adresi** | URL | `http://127.0.0.1:1234` |
| **Varsayılan model** | model adı | `qwen2.5-7b-instruct` |
| **Sözlük AI kaynağı** | Otomatik / LM Studio / Alternatif / Kapalı | Otomatik |
| **AI sözlük sonuçlarını sözlüğe kaydet** | açık / kapalı | açık |
| **Alternatif uç noktayı kullan** | açık / kapalı | kapalı |
| **Temel URL** | URL | `https://integrate.api.nvidia.com/v1` |
| **Model** | model adı | `meta/llama-3.1-8b-instruct` |
| **API anahtarı** | gizli metin | boş |

*Nasıl:* değerleri değiştirip **Kaydet**'e basın; **Ayarlar kaydedildi** görünür, tema değiştiyse pencere yeniden çizilir. **Bağlantıyı test et** alternatif uç noktayı yoklayıp **Bağlantı başarılı · N model** ya da **Bağlantı başarısız** yazar, **Anahtarı sil** anahtarı kaldırır.
*İpucu:* Anahtar alanının yanındaki etiket **••••• kayıtlı** ya da **anahtar yok** der; anahtar ekrana geri yazılmaz.

## 5. Sözlük (ayrıntılı)

Sözlük üç dilli bir arama motorudur: **Fransızca ↔ İngilizce ↔ Türkçe**. Gömülü 1.219 madde uygulamanın içindedir ve internetsiz çalışır; üzerine kendi maddeleriniz ve önbelleklenen AI maddeleri eklenir. En alttaki sayaç dağılımı gösterir: `… madde · gömülü … · kullanıcı … · AI …`.

### 5.1 Yön seçici

Araç çubuğunun ikinci satırındaki **Yön:** listesi beş seçenek sunar:

| Seçenek | Kod | Ne yapar | Ne zaman seçmeli |
| --- | --- | --- | --- |
| **Otomatik** | `auto` | Üç tarafta birden arar; en iyi eşleşen taraf yönü belirler | Günlük kullanım |
| **FR → EN** | `fr2en` | Yalnızca Fransızca madde başlarında arar | Fransızca kelimenin İngilizcesi |
| **EN → FR** | `en2fr` | Yalnızca İngilizce karşılıklarda arar | İngilizceden Fransızcaya üretim |
| **FR → TR** | `fr2tr` | Fransızca madde başlarında arar, Türkçe sütununu öne alır | Fransızca kelimenin Türkçesi; **eksik Türkçe karşılığı AI ile tamamlatan yön budur** |
| **TR → FR** | `tr2fr` | Yalnızca Türkçe karşılıklarda arar | Türkçe kelimenin Fransızcası |

Seçim anında kaydedilir ve yeniden açılışta korunur. Arama kutusunun sağındaki etiket geçerli yönü (`FR → EN` gibi) yazar; **Otomatik** modda motorun kararını gösterir. Sabit yönde yalnızca kaynak taraf taranır, böylece diğer dillerdeki benzer diziler karışmaz.

### 5.2 Türkçe sütunu ve detay paneli

Tablo sütunları: **Fransızca**, **İngilizce**, **Türkçe**, **Tür**, **Cinsiyet / Çoğul**, **Kaynak**. `FR → TR` yönünde **Türkçe** sütunu madde başının hemen sağına taşınır; Türkçesi bilinmeyen maddeler `—` ile işaretlenir.

Detay panelinde büyük punto madde başı; altında tür, cinsiyet (`m`, `f`, `mf`, `pl`), varsa artikel (`le`, `la`, `les`, ortak cinsiyetli isimlerde `le/la`) ve düzensiz çoğul; **İngilizce:** ile **Türkçe:** satırları (`FR → TR` yönünde Türkçe üste çıkar); varsa « örnek cümle »; not; kelime bankanızdaysa **★ Kelime Bankası: …** satırı bulunur. Düğmeler: **🔊 Seslendir**, **✦ AI'a sor**, **Kopyala**, **★ Kelime bankasına ekle** ve yalnızca kaydedilmemiş AI maddelerinde beliren **💾 Sözlüğe kaydet**. Altta 12 sorgu tutan **Son aramalar** listesi ve **AI yanıtı** kutusu vardır.

### 5.3 Arama kuralları

İki harf yazdığınız anda liste sessizce güncellenir; Enter ya da **Ara** "tam arama" yapar (geçmişe ekler, gerekirse AI'a sorar). Sıralama en iyiden en zayıfa:

1. **Tam eşleşme** — madde başı ya da anlamlardan biri sorgunun aynısı.
2. Baştaki `to` / `the` / `a` / `an` / `sich` / `se` / `s'` atılmış tam eşleşme (`to speak` de `speak` de `parler` bulur).
3. **Önek** — `mai` sorgusu `maison` getirir.
4. **Kelime başı** — sorgu, çok kelimeli bir karşılığın bir kelimesinin başındaysa.
5. **İçerme** — en az üç harflik sorgular için.
6. **Not alanı** — başka hiçbir şey tutmadığında son çare.

Arama, yazımı bozmadan şu esneklikleri tanır:

- **Aksanlar önemsizdir:** `eleve` → `élève`, `ecole` → `école`.
- **Bağlı harfler açılır:** `œ` → `oe`, `æ` → `ae`; `oeil` ile `œil` aynıdır.
- **Élision atılır:** `l'`, `d'`, `j'`, `s'`, `qu'`, `n'`, `m'`, `t'`, `c'` önekleri yok sayılır (`l'école` → `école`).
- **Türkçe harfler katlanır:** `ç/c`, `ğ/g`, `ş/s`, `ö/o`, `ü/u`, `İ/I/ı → i`; `ışık` ve `isik` aynı sonucu verir.

Bu esneklik **yalnızca aramaya** özgüdür; dikte ve sınav yanıtları aksana duyarlı karşılaştırılır.

### 5.4 Kaynak etiketleri

| Etiket | Anlamı |
| --- | --- |
| **gömülü** | Uygulamayla gelen çekirdek sözlük (1.219 madde) |
| **kullanıcı** | Elle eklediğiniz ya da CSV/TSV ile içe aktardığınız maddeler |
| **AI** | Yapay zekadan gelip yerel sözlüğe önbelleklenen maddeler |

AI maddesi kaydedildikten sonra çevrimdışı da bulunur; ikinci aramada ağa çıkılmaz.

### 5.5 Eksik Türkçe karşılığı AI ile doldurmak

Sürüm 1.2.0'in en belirgin yeniliği budur. **FR → TR** yönünde bulunan maddenin Türkçe sütunu `—` ise ve AI politikası **Kapalı** değilse uygulama arka planda yapay zekaya sorar: durum çubuğunda önce **Türkçe karşılık eksik, AI'a soruluyor…**, yanıt gelince **Türkçe karşılık AI ile eklendi** yazar.

Gelen karşılık **var olan maddenin içine yazılır**, yanına kopya madde açılmaz. Eşleştirme madde başı ve ortak bir İngilizce anlam üzerinden yapılır; yapay zeka İngilizceyi farklı yazsa da (`attic` / `attic; loft`), kelimenin birden çok anlamı olsa da (her anlam kendi karşılığını alır) ya da maddeyi tür alanı boş bırakarak elle eklemiş olsanız da karşılık doğru maddeye gider.

**✦ AI'a sor** bundan bağımsızdır: yerel sonuç bulunsa bile sorar ve maddeleri listenin üstüne ekler. Hiç sonuç çıkmazsa AI kendiliğinden sorulur ve **Sözlükte bulunamadı. AI'a sorabilir veya kendiniz ekleyebilirsiniz.** mesajı çıkar. Yanıtın sonunda **Yanıtlayan: LM Studio · model-adı** ya da **Yanıtlayan: Alternatif · model-adı** satırı bulunur. **AI sözlük sonuçlarını sözlüğe kaydet** kapalıysa maddeler yalnızca gösterilir; beğendiğinizi seçip **💾 Sözlüğe kaydet** ile kalıcılaştırırsınız.

### 5.6 Kelime bankasına ekleme

**★ Kelime bankasına ekle** seçili maddeyi çalışma destenize aktarır: Türkçe karşılık varsa `tr` alanına ilk Türkçe anlam, `en` alanına İngilizce karşılık yazılır; Türkçe yoksa ilk İngilizce anlam Türkçe alanına düşer. İsimlerde cinsiyet (`masculin`, `féminin`, `masculin/féminin`, `pluriel`), artikel ve düzensiz çoğul da taşınır. Kelime `Sözlük FR-EN-TR` destesine girer ve Aralıklı Tekrar'ın **Yeni** kuyruğunda görünür.

### 5.7 CSV içe / dışa aktarma

**↑ CSV dışa aktar** listede duran sonuçları (liste boşsa sözlüğün tamamını) yazar; dosya adı varsayılan `dictionary_fr.csv`, başlangıç klasörü `exports`.

| # | Sütun | İçerik |
| --- | --- | --- |
| 1 | `headword` | Fransızca madde başı (artikelsiz, doğru aksanlarla) |
| 2 | `translation` | İngilizce karşılık; anlamlar `; ` ile ayrılır |
| 3 | `pos` | Tür kodu: `n`, `v`, `adj`, `adv`, `pron`, `prep`, `conj`, `num`, `art`, `int`, `part`, `phr` |
| 4 | `extra` | İsimlerde cinsiyet (`m`, `f`, `mf`, `pl`) ve düzensizse çoğul; diğer türlerde boş |
| 5 | `note` | Kısa not; fiillerde çoğunlukla participe passé |
| 6 | `source` | `builtin`, `user` veya `ai` |
| 7 | `example` | Kısa Fransızca örnek cümle (boş olabilir) |
| 8 | `tr` | Türkçe karşılık; anlamlar `; ` ile ayrılır |

```csv
headword,translation,pos,extra,note,source,example,tr
maison,house,n,f,,builtin,,ev
œil,eye,n,m yeux,,builtin,,göz
aller,to go,v,,allé (être),builtin,,gitmek
journal,newspaper; diary,n,m journaux,,builtin,,gazete; günlük
```

**↓ CSV/TSV içe aktar** `.csv`, `.tsv` ve `.txt` dosyalarını okur; ayırıcı kendiliğinden anlaşılır. Başlık satırı varsa sütunlar **herhangi bir sırada** olabilir ve `word`, `target`, `français`, `meaning`, `english`, `türkçe`, `turkish`, `definition` adları da tanınır. Başlık yoksa yukarıdaki sıra beklenir; `tr` sütunu olmayan eski düzen de kabul edilir. Boş satırlar atlanır, aynı madde iki kez eklenmez.

### 5.8 Elle madde eklemek

**+ Madde ekle** bir pencere açar: **Fransızca**, **İngilizce**, **Türkçe**, **Tür (n/v/adj/…)**, **Cinsiyet / Çoğul**, **Not / tanım**, **Örnek cümle**. Arama kutusunda metin varsa uygun alan hazır doldurulur. Fransızca ya da İngilizce alanını boş bırakırsanız **Fransızca ve İngilizce alanları zorunlu.** uyarısı çıkar. **Kaydet** (ya da Enter) maddeyi `kullanıcı` kaynağıyla ekler, **Esc** pencereyi kapatır.

## 6. Yapay zeka

Yapay zeka **isteğe bağlıdır**: kapalıyken kelime, tekrar, sınav, dilbilgisi, sözlük, PDF ve ilerleme çalışmaya devam eder.

### 6.1 LM Studio kurulumu ve yerel sunucu

1. LM Studio'yu kurun ve bir sohbet modeli indirin.
2. **Local Server** (OpenAI uyumlu sunucu) bölümünü açın, modeli yükleyip sunucuyu başlatın.
3. Varsayılan adres `http://127.0.0.1:1234`'tür; farklı port kullanıyorsanız **Ayarlar → LM Studio adresi** satırına yazın.
4. Sağ üstteki rozetin **AI: Kullanılabilir** demesini bekleyin.

Yerel sunucu anahtar istemez ve istekleriniz bilgisayarınızdan çıkmaz.

### 6.2 Model seçimi

| Görev | Tercih edilen modeller |
| --- | --- |
| `chat` | `qwen2.5-7b-instruct`, `llama-3.1-8b-instruct` |
| `grammar` (Açıkla) | `qwen2.5-7b-instruct`, `qwen2.5-14b-instruct` |
| `translate` (Çevir) | `qwen2.5-7b-instruct`, `gemma-2-9b-it` |
| `correct` (Düzelt / Yazma) | `qwen2.5-7b-instruct`, `qwen2.5-14b-instruct` |
| `dialogue` (Konuşma) | `qwen2.5-7b-instruct`, `llama-3.1-8b-instruct` |
| `dictionary` (Sözlük) | `qwen2.5-7b-instruct`, `llama-3.1-8b-instruct` |
| `vision` (Görsel / OCR) | `qwen2-vl-7b-instruct`, `llava-v1.6-mistral-7b` |

Ayarlar'daki **Varsayılan model** LM Studio'da yüklüyse doğrudan kullanılır; değilse görev profilinden yüklü olan ilk model, o da yoksa sıralamanın ilki seçilir. Sıralamada **uzman modeller atlanır**: adında `embed`, `rerank`, `math`, `coder`, `code-`, `vision`, `-vl`, `llava`, `moondream`, `bio`, `medic`, `whisper`, `tts`, `audio`, `clip`, `sd-`, `stable-diffusion` geçenler ancak başka model yoksa kullanılır. Eşitlikte 4-16 milyar parametreli, adında `instruct` / `-it` / `chat` / `assistant` geçen modeller öne alınır.

### 6.3 Alternatif uç nokta

Ayarlar'daki grup başlığı: **Alternatif uç nokta (OpenAI uyumlu: NVIDIA NIM, OpenRouter, Groq, Ollama…)**.

1. **Alternatif uç noktayı kullan** kutusunu işaretleyin.
2. **Temel URL**'yi yazın (varsayılan `https://integrate.api.nvidia.com/v1`, NVIDIA NIM).
3. **Model** adını yazın (varsayılan `meta/llama-3.1-8b-instruct`); bu ad sunucuya **yazdığınız gibi** gönderilir.
4. **API anahtarı** alanına anahtarınızı yapıştırın; anahtar istemeyen bir sunucu için (ağdaki bir Ollama ya da LM Studio gibi) boş bırakın — anahtarın gerekip gerekmediğine adres değil sunucu karar verir.
5. **Kaydet**'e, sonra **Bağlantıyı test et**'e basın: **Bağlantı başarılı · N model**; model listede yoksa ayrıca **seçili model listede yok** uyarısı çıkar.

Alternatif uç nokta **yalnızca sözlük** için kullanılır; AI Öğretmen, Konuşma ve Yazma her zaman yerel LM Studio'ya bağlanır.

### 6.4 API anahtarının saklanması

Anahtar **hiçbir zaman `settings.json` dosyasına yazılmaz**. Windows'ta Kimlik Bilgisi Yöneticisi'nde `FrenchCourseAI/alt_api_key` adıyla saklanır; Windows dışında ya da bu API kullanılamazsa `settings/secrets.json` dosyası devreye girer. **Anahtarı sil** anahtarı her iki yerden kaldırır; `FRENCHCOURSEAI_API_KEY` ortam değişkeni tanımlıysa kayıtlı anahtarın yerine o kullanılır.

### 6.5 Sözlük AI politikası

Politikayı hem **Ayarlar → Sözlük AI kaynağı** satırından hem de sözlük araç çubuğundaki **AI:** listesinden değiştirebilirsiniz; ikisi aynı ayarı yazar.

| Politika | Davranış |
| --- | --- |
| **Otomatik** | LM Studio erişilebilirse onu; değilse etkin ve erişilebilirse alternatifi kullanır; ikisi de yoksa AI'sız çalışır |
| **LM Studio** | Yalnızca yerel sunucu; erişilemezse AI kullanılmaz |
| **Alternatif** | Yalnızca alternatif uç nokta; kapalı ya da erişilemezse AI kullanılmaz |
| **Kapalı** | Hiç AI çağrısı yapılmaz |

Araç çubuğundaki durum etiketi o anki gerçeği söyler: **LM Studio: bağlı**, **Alternatif: hazır**, **AI erişilemiyor** ya da **AI kapalı**. Erişilebilirlik sınaması `GET /v1/models` isteğidir ve sonuç 30 saniye önbelleklenir. Ayarlar'daki **Bağlantıyı test et** de aynı isteği kullanır, ama formda o an duran (henüz kaydedilmemiş) değerleri dener; sözlük ise kaydedilmiş ayarları kullanır. Bu yüzden anahtarı kaydetmeden test ederseniz ikisi farklı sonuç verebilir.

### 6.6 Token defteri ve gizlilik

Her AI çağrısından sonra Token Defteri'ne bir satır düşer: zaman damgası, model, görev, istem tokenı, yanıt tokenı, toplam, süre (ms) ve başarı durumu. **İstem ve yanıt metni hiçbir yere kaydedilmez**; gönderdiğiniz görsel de saklanmaz.

Sözlük çağrıları yapılandırılmış JSON ister: en fazla 5 madde, 1.200 token bütçe, 90 saniye zaman aşımı. "Düşünen" modeller bütçelerini akıl yürütmeye harcayıp boş yanıt döndürebildiği için yerel sunuculara `reasoning_effort` alanı gönderilir (tanımayan sunucularda istek bu alan olmadan yinelenir); yanıt uzunluk sınırından kesildiyse çağrı bir kez üç kat bütçeyle tekrarlanır.

## 7. Veri yönetimi

**Profiller.** Üst çubuktaki liste profilleri gösterir, **+** yeni profil ekler. Her profil kendi tekrar takvimini, sınav geçmişini, favorilerini, PDF notlarını ve dilbilgisi istatistiğini tutar; kelime bankası, sözlük ve ayarlar ortaktır. Bu sürümde arayüzde profil silme düğmesi yoktur.

**Yedekleme.** Üç yol vardır: Kelime Bankası → **↑ Dışa aktar** (UTF-8 kelime CSV'si), Sözlük → **↑ CSV dışa aktar** (sütun düzeni [5.7](#57-csv-içe--dışa-aktarma)), Paketler → **↑ Dışa aktar** (`.fcapack`). En eksiksiz yedek veri klasörünün tamamını kopyalamaktır; kopyalamadan önce uygulamayı kapatın.

**Sıfırlama.** Uygulama içinde "her şeyi sil" düğmesi yoktur. Temiz başlangıç için uygulamayı kapatın, veri klasörünü (ya da `data\FrenchCourseAI.db` dosyasını) yedekleyip silin; sonraki açılışta veritabanı, varsayılan profil ve gömülü kelime destesi yeniden oluşur. Yalnızca ayarları sıfırlamak için `settings\settings.json` dosyasını silmeniz yeterlidir. Silmeden denemek isterseniz `FCA_HOME` ile geçici bir klasör kullanın.

## 8. Kısayollar ve ipuçları

| Kısayol | Nerede | Ne yapar |
| --- | --- | --- |
| **Enter** | Sözlük arama kutusu | Tam arama yapar (geçmişe ekler, gerekirse AI'a sorar) |
| **2+ harf yazmak** | Sözlük arama kutusu | Listeyi sessizce, AI'a sormadan günceller |
| **Çift tıklama** | Sözlük sonuç listesi | Seçili madde başını seslendirir |
| **Enter** | Madde ekle penceresi | Maddeyi kaydeder |
| **Esc** | Madde ekle penceresi | Pencereyi kapatır |
| **Enter** | Kelime Bankası arama kutusu | Aramayı çalıştırır |
| **Çift tıklama** | Ders Kitaplığı listesi | Dosyayı varsayılan uygulamada açar |
| **Fareyi basılı sürükleme** | El yazısı alanı | Çizgi çizer |

Diğer ipuçları:

- **🎲 Rastgele kelime** gömülü sözlükten rastgele bir madde açar; sabit `EN → FR` ya da `TR → FR` yönündeyken bile bulur, çünkü bu tek arama için yön ters çevrilir ve seçiminiz bozulmaz.
- **Kopyala** maddeyi `madde başı — İngilizce — Türkçe` biçiminde panoya alır.
- Seslendirme Windows'un ses motorunu kullanır ve sisteminizde `fr-*` bir ses yüklüyse onu seçer.

## 9. Sorun giderme

**LM Studio bağlanmıyor / rozet "Kullanılamıyor" diyor.** Yerel sunucu çalışmıyor, model yüklü değil ya da adres farklıdır. LM Studio'da bir model yükleyip **Local Server**'ı başlatın, Ayarlar'daki **LM Studio adresi** değerini sunucunun portuyla karşılaştırın (varsayılan `http://127.0.0.1:1234`) ve **Yerel AI**'nın işaretli olduğundan emin olun. Sonuç 30 saniye önbelleklendiği için sayfayı bir kez değiştirip geri dönün.

**AI boş yanıt veriyor / "AI bu sorgu için madde döndürmedi." yazıyor.** Genellikle "düşünen" bir model token bütçesini akıl yürütmeye harcamıştır ya da model JSON üretemeyecek kadar küçüktür. Ayarlar'dan `qwen2.5-7b-instruct` gibi bir instruct modeli seçin; `coder`, `math`, `embed` adlı modellerden kaçının. Uygulama kesilen yanıtı bir kez daha büyük bütçeyle dener, ama düzgün bir sohbet modeli sorunu tamamen ortadan kaldırır.

**Türkçe karşılık yok, sütunda `—` görünüyor.** Madde Türkçesiz eklenmiştir (elle ya da CSV ile) veya AI politikası **Kapalı**'dır. Yönü **FR → TR** yapıp aramayı tekrarlayın; politika Kapalı değilse eksik karşılık arka planda sorulup aynı maddeye yazılır. AI istemiyorsanız **+ Madde ekle** ile ya da `tr` sütunu dolu bir CSV ile elle tamamlayın.

**macOS "açılamıyor" uyarısı veriyor.** Paket notarize edilmemiştir. Uygulamaya çift tıklamak yerine **sağ tıklayıp Aç** deyin ve çıkan uyarıda yine **Aç**'a basın; izin bir kez verildikten sonra kalıcıdır.

**Ses çıkmıyor.** **Seslendirme** kapalı olabilir, sistemde Fransızca ses yüklü olmayabilir ya da Windows dışı bir sistemde olabilirsiniz. Ayarlar'dan **Seslendirme**'yi işaretleyin ve Windows'ta *Ayarlar → Saat ve dil → Konuşma* bölümünden Fransızca ses paketini kurun; seslendirme Windows'un `System.Speech` motoruna dayanır.

**.exe açılmıyor.** Zip ayıklanmadan çalıştırılmış, SmartScreen engellemiş ya da antivirüs karantinaya almış olabilir. Zip'i bir klasöre ayıklayın, SmartScreen uyarısında **Ek bilgi → Yine de çalıştır** deyin, gerekirse antivirüse klasör istisnası tanımlayın. Sorun sürerse `python .\French_Course_AI.pyw` ile kaynaktan çalıştırıp hata iletisini görün.

**Verilerim nerede?** Windows'ta `%APPDATA%\FrenchCourseAI`, macOS'ta `~/Library/Application Support/FrenchCourseAI`, Linux'ta `~/.frenchcourseai`; tam yol **Çevrimdışı Kılavuz** sayfasının en altında yazılıdır. `FCA_HOME` tanımlıysa veriler orada durur ve uygulamayı silmek bu klasörü silmez.

## 10. Sürüm notları özeti

| Sürüm | Öne çıkanlar |
| --- | --- |
| **v1.0.0** | 18 sayfalık kabuk: SM-2/Leitner tekrar, kelime bankası (162 A1 kelimesi), sınav, yazım/telaffuz/dilbilgisi laboratuvarları, Kaynak Merkezi, PDF okuyucu, ders kitaplığı, LM Studio ile AI Öğretmen, konuşma ve yazma, ilerleme, paketler, token defteri; tr/en/fr arayüz; Windows ve macOS paketleri |
| **v1.1.0** | **Sözlük sekmesi** (çift yönlü Fransızca-İngilizce) ve sözlük için **AI bağlantısı**: LM Studio ya da alternatif OpenAI uyumlu uç nokta, AI politikası, anahtarın Kimlik Bilgisi Yöneticisi'nde saklanması |
| **v1.1.1** | Sözlük AI düzeltmeleri: düşünen modellerde boş yanıt sorunu, model seçimi |
| **v1.1.2** | Sözlük AI cilası: isimlerde ek alanı temizliği, AI yanıtında yön etiketi, araç çubuğu düzeni, tekrar eden anlamların ayıklanması |
| **v1.2.0** | **Yön seçici** (`Otomatik`, `FR → EN`, `EN → FR`, `FR → TR`, `TR → FR`; seçim kaydedilir) ve **üçüncü dil olarak Türkçe**: tabloda ve detay panelinde Türkçe sütunu, `FR → TR` yönünde eksik Türkçe karşılığın AI ile aynı maddeye doldurulması, CSV'de `tr` sütunu, 1.219 gömülü madde |
| **v1.2.1** | **Türkçe aramada ASCII ve büyük harf desteği**: `sinav` = `SINAV` = `sınav`, `cok` = `çok`, `ogrenci` = `öğrenci`; Türkçe katlama Fransızca aksan sadeleştirmesinden önce uygulanır, katlanarak bulunan eşleşme doğrudan eşleşmenin altına sıralanır, gösterilen yazım değişmez. Ayrıca **kullanım kılavuzu** depoya eklendi (`docs/KULLANIM_KILAVUZU.md` ve `docs/USER_GUIDE.md`; PDF sürümü sürüm ek dosyası olarak yayımlanır) |
| **v1.3.0** | **MIT lisansı**: proje MIT Lisansı altında yayımlandı; `LICENSE` ve `THIRD_PARTY_NOTICES.md` depoya eklendi ve yayımlanan paketlerin hem içine hem yanına kondu. Ayrıca paketler **temiz bir sanal ortamda** derlenir: yalnızca `requirements.txt`'teki kütüphaneler pakete girer, dosya boyutu küçülür ve üçüncü taraf bildirimi paketle birlikte gelir |

## 11. Sık sorulan sorular

**Uygulama internetsiz çalışır mı?** Evet. Kelime, tekrar, sınav, dilbilgisi, gömülü 1.219 sözlük maddesi, PDF notları ve ilerleme tamamen yereldir; yalnızca Kaynak Merkezi bağlantıları ve alternatif AI uç noktası internet ister.

**Yapay zeka olmadan sözlük işe yarar mı?** Yarar. Gömülü sözlük 1.219 maddeyi cinsiyet, düzensiz çoğul, İngilizce ve Türkçe karşılıklarıyla içerir; AI yalnızca bulunmayan kelimeler ve eksik Türkçe karşılıklar için devreye girer.

**Verilerim bir sunucuya gönderiliyor mu?** Hayır. Profil, ilerleme, sınav, not ve sözlük verileriniz bilgisayarınızdaki SQLite dosyasında kalır; yalnızca alternatif uç noktayı siz etkinleştirdiğinizde sözlük sorgularınız o servise gider ve istem/yanıt metni hiçbir yerde saklanmaz.

**API anahtarım nerede duruyor?** Windows Kimlik Bilgisi Yöneticisi'nde `FrenchCourseAI/alt_api_key` adıyla, diğer sistemlerde `settings/secrets.json` dosyasında. `settings.json` içine asla yazılmaz ve ekrana geri gösterilmez.

**Otomatik yön yanlış tahmin ederse?** Sabit bir yön seçin: `chat` hem Fransızca "kedi" hem İngilizce bir kelimedir, `FR → EN` belirsizliği kaldırır.

**Aksanları yazmak zorunda mıyım?** Aramada hayır: `eleve` yazınca `élève`, `oeil` yazınca `œil` bulunur. Dikte ve sınav yanıtlarında ise karşılaştırma aksana duyarlıdır, çünkü amaç doğru yazımı öğretmektir.

**Kendi kelime listemi nasıl yüklerim?** Kelime Bankası'nda **↓ İçe aktar** (kelime CSV'si) ya da Sözlük'te **↓ CSV/TSV içe aktar** (sözlük tablosu; başlık satırını tanır, sütun sırasından bağımsızdır).

**Bir kelimeyi hem sözlüğe hem çalışma desteme nasıl alırım?** Sözlükte maddeyi seçip **★ Kelime bankasına ekle**'ye basın; kelime `Sözlük FR-EN-TR` destesine girer ve ilk oturumda **Yeni** kuyruğunda karşınıza çıkar.

**Hangi modeli kurmalıyım?** `qwen2.5-7b-instruct` iyi bir başlangıçtır; 4-16 milyar parametreli instruct modelleri hem hızlı hem yeterlidir.

**Uygulamayı kaldırırsam verilerim silinir mi?** Hayır. Program klasörünü silmek veri klasörüne dokunmaz; verileri de silmek isterseniz `%APPDATA%\FrenchCourseAI` klasörünü elle kaldırın.

## 12. Lisans

French Course AI **MIT Lisansı** ile dağıtılır. Tam metin `LICENSE` dosyasındadır; bu dosyayı hem depo
kökünde hem de indirdiğiniz paketin içinde uygulamanın yanında bulursunuz. Programı özgürce
kullanabilir, kopyalayabilir, değiştirebilir ve dağıtabilirsiniz; tek koşul telif ve lisans
bildiriminin kopyalarla birlikte kalmasıdır. Yazılım hiçbir garanti verilmeksizin "olduğu gibi"
sunulur.

Uygulamanın kullandığı ve Windows ile macOS paketlerinin içine giren üçüncü taraf bileşenler — PDF
metni için pypdf, arayüz için Tcl/Tk, Python çalışma zamanı, OpenSSL, SQLite ve diğerleri — gerçek
lisanslarıyla birlikte `THIRD_PARTY_NOTICES.md` dosyasında listelenir; o dosya da aynı iki yerde
bulunur.

Kaynak Merkezi'ndeki Wikibooks, Tatoeba, LibriVox ve Project Gutenberg bağlantıları yalnız tarayıcınızda
açılır; indirdiğiniz her materyal kendi lisansını korur ve uygulamayla birlikte dağıtılmaz. `Resources`
klasörüne koyduğunuz kendi ders dosyalarınız da bilgisayarınızda kalır.
