# 🤖 Titanyum Koordinat Botu

Bu bot, **SonOyuncu Titanyum** sunucusunda çoklu hesapları yönetmek, koordinatlara göre en yakın hesabı bulmak ve Minecraft tarzı koordinat sisteminde hesapların durumunu görmek için tasarlanmıştır. Bot, **Slash komutları** ile çalışır, **MongoDB** ile verileri saklar ve kullanımı kolay, kullanıcı dostu bir arayüz sunar.

---

## 🌟 Özellikler

- **Hesap Ekleme**: Farklı dünyalara ait koordinat bilgilerini girebilir, yeni hesaplar ekleyebilirsiniz.
- **Hesap Silme**: İstediğiniz bir hesabı veritabanından silebilirsiniz.
- **Koordinat Sorgulama**: Girilen dünyanın ve koordinatın (X Z) verilerine göre, en yakın hesabı bulabilirsiniz.
- **Slash Komutlar**: Tüm komutlar Discord’un slash komut sistemi ile çalışır.
- **MongoDB Desteği**: Hesap verileri MongoDB üzerinde saklanır.

---

## 🛠️ Gereksinimler

### Yazılım Gereksinimleri

- **Python 3.10+**  
  [Python İndirme](https://www.python.org/downloads/)

- **MongoDB Atlas Hesabı veya Local MongoDB**  
  MongoDB Atlas ücretsiz planı ile [kaydolabilir ve veritabanı oluşturabilirsiniz](https://www.mongodb.com/cloud/atlas/register).

- **Discord Botu**  
  [Discord Geliştirici Portalı](https://discord.com/developers/applications) üzerinden bot oluşturup token alın.

### Kütüphaneler

Aşağıdaki kütüphaneler gereklidir. Terminal veya komut satırından yükleyebilirsiniz:

```bash
pip install -U discord.py pymongo
