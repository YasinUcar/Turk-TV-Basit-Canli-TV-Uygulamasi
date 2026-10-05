# 📺 Türk TV

Sade, büyük yazılı ve herkesin kolayca kullanabileceği bir **Türk canlı TV uygulaması**. Windows ve Debian/Ubuntu üzerinde çalışır. Kurulumu ve kullanımı basittir: kanala tıkla, izle.

## Ne yapar?

- 100'den fazla Türk televizyon kanalını canlı olarak izletir.
- Bilinen kanallar (TRT 1, ATV, Kanal D, Star TV, Show TV, NOW, TV8, Kanal 7 …) listenin en üstündedir.
- Kanallar gruplara ayrılmıştır: Ulusal, Haber, Spor, Çocuk, Müzik, Belgesel ve Dini, Yerel ve Diğer.
- Her kanalın yanında numarası ve logosu vardır. Logo yüklenemezse kanalın baş harfleri gösterilir.
- Son izlenen kanalı hatırlar, program açılınca kaldığı yerden devam eder.
- Açılmayan bir kanalda "Bu kanal şu an açılamıyor" mesajı ve **Tekrar dene** düğmesi çıkar.
- Büyük yazı ve sade arayüzüyle yaşlılar ve bilgisayar kullanmakta zorlananlar için tasarlanmıştır.

## Kullanım

| Eylem | Nasıl |
|---|---|
| Kanal aç | Soldaki listeden kanala tıkla |
| Sonraki / önceki kanal | `↓` / `↑` tuşları |
| Tam ekran | Videoya çift tıkla veya `F` tuşu (`Esc` ile çık) |
| Ses | Videonun altındaki ses çubuğu |

## Kurulum

[Releases](../../releases) bölümünden işletim sisteminize uygun dosyayı indirin.

**Windows (64 bit):** `TurkTV-Windows.zip` dosyasını ayıklayın ve `TurkTV.exe` dosyasını çalıştırın. Kurulum gerekmez. Exe imzasız olduğu için Windows uyarı verirse **Ek bilgi → Yine de çalıştır** deyin.

**Debian / Ubuntu (64 bit):**
```bash
sudo apt install ./turk-tv_1.0.0_amd64.deb
```
Kurulumdan sonra uygulama menüsünde **Türk TV** olarak görünür, terminalden `turk-tv` ile de açılır.

## Kaynak koddan çalıştırma

Gereksinimler: [Node.js](https://nodejs.org) 18+ ve (kanal listesini yenilemek için) Python 3.

```bash
npm install
npm start
```

### Kanal listesini yenileme

Kanal adresleri ve logolar [iptv-org](https://github.com/iptv-org) projesinin açık listelerinden alınır. Listeyi güncellemek için:

```bash
rm -f tr.m3u logos.csv   # eski kopyaları sil (Windows'ta elle silin)
npm run gen              # channels.js dosyasını yeniden üretir
```

Kanalların sırası ve grupları `gen.py` içindeki listeden değiştirilebilir.

### Paket oluşturma

```bash
npm run build:win     # dist/TurkTV-win32-x64
npm run build:linux   # dist/TurkTV-linux-x64
npm run build:deb     # dist/turk-tv_1.0.0_amd64.deb  (dpkg-deb gerekir)
```

## Nasıl çalışır?

- [Electron](https://www.electronjs.org) ile masaüstü uygulaması olarak paketlenmiştir.
- Yayınlar (HLS / `.m3u8`) [hls.js](https://github.com/video-dev/hls.js) ile oynatılır.
- Bazı yayın sunucuları tarayıcı kısıtlamaları (CORS) yüzünden doğrudan oynatmaya izin vermez. `main.js` içinde bu kısıtlama yalnızca uygulamanın kendi penceresi için gevşetilir.
- Uygulama kanal içeriği barındırmaz veya kopyalamaz. Yayınlar doğrudan ilgili yayıncıların sunucularından gelir.

## Bilinen sınırlamalar

- Yayın adresleri üçüncü tarafların sunucularına aittir ve zamanla değişebilir veya kapanabilir. Açılmayan kanalları bir [issue](../../issues) olarak bildirebilirsiniz.
- Bazı yayınlar yurt dışından izlenemeyebilir.
- Yalnızca 64 bit (x64) sürümleri derlenmiştir.

## Yasal not

Bu proje bir yayın hizmeti değildir. Kanal adları, logolar ve yayınlar ilgili kuruluşlara aittir. Yalnızca herkese açık, ücretsiz yayın adresleri listelenir. Bir hak sahibi kaldırılmasını isterse ilgili kanal listeden çıkarılır.

## Lisans

[MIT](LICENSE)
