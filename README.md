
# 👁️ Göz Takibi ile Bilgisayar Kontrolü

Bu proje, **göz hareketleri** ve **göz kırpma** gibi yüz ifadelerini kullanarak bilgisayar kontrolünü mümkün hale getiren bir sistem sunar. Özellikle hareket kısıtlılığı olan bireyler için büyük kolaylık sağlayabilecek bu sistem, yüz tanıma ve izleme teknolojilerinden faydalanır. 

## 🎯 Özellikler

- Göz konumuna göre fare hareketi
- Sol göz kırpması ile **sol tıklama** (ve çift tıklama algılama)
- Sağ göz kırpması ile **sağ tıklama**
- Her iki göz kapalıyken **takip durumu değiştirilebilir**
- Gülümseme tespit edilince tıklamalar geçici olarak engellenir
- Ayarlanabilir:
  - Hassasiyet
  - Yumuşaklık
  - Göz kapanma eşiği
  - Tıklama süresi, çift tıklama süresi
  - Gülümseme algılama eşikleri
- Görsel Arayüz (Tkinter) ile kolay kontrol

## 🖥️ Arayüz Ekranı

Tkinter ile oluşturulan arayüz üzerinden:

- Kamera görüntüsü izlenebilir
- Takip başlat/durdur butonu yer alır
- Eşik değerleri ve sistem ayarları slider’lar ile değiştirilebilir

## ⚙️ Kullanılan Teknolojiler

- Python
- OpenCV
- MediaPipe (Face Mesh)
- PyAutoGUI
- Tkinter
- PIL (Python Imaging Library)

## 🚀 Kurulum

```bash
pip install opencv-python mediapipe pyautogui keyboard pillow
```

Ardından Python dosyasını çalıştırın:

```bash
python goz_takip.py
```

> Kamera açıldıktan sonra gözünüzü ortalayarak takibi başlatabilirsiniz. Takip durumunu açmak/kapatmak için iki gözünüzü belirlenen süre boyunca kapatmanız yeterlidir.

## ⌨️ Kısayollar

- `Ctrl + Shift + L` : Takip başlat / durdur

## 📸 Ekran Görüntüsü

> *(Buraya arayüzden alınan bir ekran görüntüsünü ekleyebilirsin.)*

## 📩 İletişim

Proje hakkında görüşlerinizi, önerilerinizi ya da sorularınızı benimle paylaşabilirsiniz:

- 📧 E-posta: mahiryapar2453@gmail.com  
- 🐦 Twitter: [@mahirjs](https://twitter.com/mahirjs)  
- 📸 Instagram: [@mahir.js](https://instagram.com/mahir.js)

---

> Bu proje, teknolojiyle insan etkileşimini bir adım öteye taşımayı amaçlamaktadır.  
Görüşmek üzere! 👋
