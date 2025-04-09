# 🤖 Titanyum Koordinat Botu

Minecraft Titanyum sunucusunda, oyuncuların hesaplarını ve koordinatlarını yönetmek için geliştirilmiş Discord Slash komut botu.

---

## ✨ Özellikler

- Slash komut sistemiyle etkileşimli kullanım
- MongoDB veritabanı entegrasyonu
- Hesap ekleme, silme ve koordinata göre en yakın hesabı bulma
- -30.000 ile +30.000 arası koordinat doğrulama
- Embed mesajlarla şık görünüm
- Sadece yetkili rolü olanlar hesap ekleyip silebilir
- Koordinat sorgulama komutunu herkes kullanabilir

---

## 🚀 Kurulum

### 1. Python Yükle
Python 3.10+ versiyonunu indir ve kur:
👉 https://www.python.org/downloads/

### 2. MongoDB Hesabı Oluştur
1. https://www.mongodb.com/ adresine git
2. Ücretsiz bir hesap oluştur
3. Yeni bir "Cluster" oluştur
4. Veritabanı kullanıcı adı/şifresi belirle
5. "Database Deploy" edildikten sonra → **Connect** > **MongoDB for VS Code** > **Connect to your MongoDB deployment.** kısmından bağlantı URI'ını kopyala.
<username>:<password>' Kısmını Şu Şekilde Düzenle: adore:adore123

Örnek URI:
```
mongodb+srv://kullanici:parola@cluster0.mongodb.net/?retryWrites=true&w=majority
```

Bu URI'yi `main.py` içinde `MONGO_URI` yerine yapıştır.

### 3. Bot Tokeni Al
1. https://discord.com/developers/applications adresine git
2. Yeni bir uygulama oluştur
3. "Bot" sekmesinden botu oluştur ve tokeni al
4. Gerekli izinleri ver (MESSAGE, EMBED, APPLICATION_COMMANDS vs.)
5. Tokeni `main.py` içindeki `TOKEN` kısmına yapıştır

---

## 🖥️ Botun Çalışması

### 4. Kurulum
`kurulum.bat` dosyasına çift tıklayarak gerekli kütüphaneleri yükleyin:
```
🔧 kurulum.bat
```

> Bu dosya `discord.py` ve `pymongo` gibi paketleri yükler.

### 5. Botu Başlatma
```
🚀 baslat.bat
```
Bot başarıyla başlatılır.

---

## ⚙️ Komutlar

### `/hesapekle`
Yeni hesap ekler.
```bash
/hesapekle isim: deneme sancak: "30 -20" yakamoz: "50 100" ...
```

### `/hesapsil`
Belirtilen isme sahip hesabı siler.
```bash
/hesapsil isim: deneme
```

### `/kordinat`
Girilen dünya ve koordinata göre en yakın hesabı gösterir.
```bash
/kordinat dunya: sancak kordinat: 30 -50
```

---

## 📄 Lisans

MIT License kullanılmıştır. Dilediğiniz gibi kullanabilir ve geliştirebilirsiniz.

---

🎉 İyi oyunlar ve kolaylıklar! Herhangi bir sorun yaşarsanız discord: Adorexrd Arkadaşlık İsteği Atarak Bildirebilirsiniz.

