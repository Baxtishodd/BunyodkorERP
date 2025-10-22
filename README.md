# 🧵 Bunyodkor PLM — Product Lifecycle Management System

Bunyodkor PLM — bu **to‘liq ishlab chiqarish jarayonini boshqarish tizimi** bo‘lib, buyurtmadan tortib tayyor mahsulot jo‘natilishigacha bo‘lgan barcha bosqichlarni raqamlashtirish uchun yaratilgan.

![Django Version](https://img.shields.io/badge/Django-4.2-green)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![License](https://img.shields.io/badge/license-MIT-lightgrey)
![Status](https://img.shields.io/badge/status-Active-success)

---

## 🚀 Asosiy maqsad

Tizim **tikuvchilik, ishlab chiqarish va rejalashtirish bo‘limlari** uchun yagona platforma yaratadi. Har bir buyurtma bo‘yicha **kesim, pechat, tikuv, dazmol, sifat nazorati, qadoqlash va jo‘natish** jarayonlari to‘liq avtomatlashtiriladi.

---

## ⚙️ Asosiy imkoniyatlar

| Modul | Tavsif |
|-------|---------|
| 🧩 **Product Model** | Model kartalari, artikul, mijoz, ishlab chiqarish rejalari |
| 📦 **Order Management** | Buyurtma yaratish, o‘lchamlar, umumiy son va muddatlarni boshqarish |
| 🧵 **Cutting / Stitching / Ironing** | Ishlab chiqarish bosqichlarini kunlik kuzatish |
| 🪡 **Hourly Work** | Har bir ishchi va patok bo‘yicha soatlik ish natijalari |
| 🧰 **Fabric & Accessories** | Mato va aksessuar kirimi, tasdiqlash va nazorat |
| 🔍 **Inspection (Quality Control)** | Sifat nazorati hisobotlari va nuqson tahlili |
| 📦 **Packing & Shipment** | Tayyor mahsulotni qadoqlash va yuk xatlarini yaratish |
| 👷 **Employee & Production Lines** | Ishchilar va patoklar bo‘yicha normativ, model biriktirish |
| 📊 **Dashboard & Analytics** | Har bir buyurtmaning jarayon bo‘yicha progressi va statistikasi |

---

## 🏗️ Texnologiyalar

- **Backend:** Django 4.2 (Python 3.10+)
- **Frontend:** Bootstrap 5 + Django templating
- **Database:** MySQL
- **Authentication:** Custom User model
- **Media Management:** Django File/ImageField
- **Admin panel:** Django Admin (customized)


---

## 🧩 O‘rnatish

```bash
# 1️⃣ Loyihani klonlash
git clone https://github.com/<yourusername>/BunyodkorERP.git
cd BunyodkorERP/plm

# 2️⃣ Virtual muhitni yaratish
python -m venv venv
source venv/bin/activate   # (Windows: venv\Scripts\activate)

# 3️⃣ Kutubxonalarni o‘rnatish
pip install -r requirements.txt

# 4️⃣ Ma’lumotlar bazasini migratsiya qilish
python manage.py migrate

# 5️⃣ Superuser yaratish
python manage.py createsuperuser

# 6️⃣ Serverni ishga tushirish
python manage.py runserver

👤 Kirish

Admin panel:

http://127.0.0.1:8000/admin/


PLM moduli:

http://127.0.0.1:8000/plm/

📸 Ekran ko‘rinishlari (UI Previews)
Model ro‘yxati	Buyurtma tafsiloti	Ishlab chiqarish jarayoni

	
	
🧠 Kelajakdagi reja

 Realtime progress dashboard

 AI asosidagi norma tahlili

 API (mobile ilovalar uchun)

 Telegram integratsiyasi (hisobotlar uchun)

💼 Muallif

Bunyodkor Textile
📍 Qashqadaryo, Koson tumani
🌐 bunyodkortex.com

📧 sales@bunyodkortex.com

📞 +998 90 997 8888

🪪 Litsenziya

MIT License — erkin foydalanish va o‘zgartirish mumkin.



## 📁 Loyihaning tuzilmasi

