import pygame
import time
import random
import os
import sys
# Pygame Başlatma
pygame.init()

# Renkler
BEYAZ = (255, 255, 255)
SIYAH = (30, 30, 30) 
KIRMIZI = (255, 82, 82)
YESIL = (76, 175, 80)
MAVI = (33, 150, 243)
GRI = (150, 150, 150)
SARI = (255, 235, 59)

# Ekran Ayarları
ekran = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
GENISLIK = ekran.get_width()
YUKSEKLIK = ekran.get_height()
ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption('Pro Piksel Yılan')

saat = pygame.time.Clock()
yilan_blok = 20
yilan_hizi = 15

# Fontlar
font_stili = pygame.font.SysFont("comicsansms", 25)
skor_fontu = pygame.font.SysFont("comicsansms", 20)

# ---------------- REKOR SİSTEMİ ----------------
def rekoru_oku():
    if not os.path.exists("rekor.txt"):
        return 0
    with open("rekor.txt", "r") as f:
        try:
            return int(f.read())
        except:
            return 0

def rekoru_yaz(rekor):
    with open("rekor.txt", "w") as f:
        f.write(str(rekor))

# ---------------- ARAYÜZ ARAÇLARI ----------------
def mesaj_yaz(mesaj, renk, y_kaydirma=0):
    metin = font_stili.render(mesaj, True, renk)
    metin_rect = metin.get_rect(center=(GENISLIK/2, YUKSEKLIK/2 + y_kaydirma))
    ekran.blit(metin, metin_rect)

def buton_olustur(mesaj, x, y, w, h, pasif_renk, aktif_renk, aksiyon=None):
    fare = pygame.mouse.get_pos()
    tiklama = pygame.mouse.get_pressed()

    # Fare butonun üzerindeyse
    if x + w > fare[0] > x and y + h > fare[1] > y:
        pygame.draw.rect(ekran, aktif_renk, (x, y, w, h))
        if tiklama[0] == 1 and aksiyon is not None:
            time.sleep(0.15) # Çift tıklamayı önlemek için kısa bir bekleme
            aksiyon()
    else:
        pygame.draw.rect(ekran, pasif_renk, (x, y, w, h))

    buton_metni = font_stili.render(mesaj, True, BEYAZ)
    ekran.blit(buton_metni, (x + (w/2 - buton_metni.get_width()/2), y + (h/2 - buton_metni.get_height()/2)))

# ---------------- OYUN DURUMLARI ----------------
def oyunu_baslat():
    oyun_dongusu()

def oyundan_cik():
    pygame.quit()
    sys.exit()

def ana_menu():
    while True:
        ekran.fill(SIYAH)
        mesaj_yaz("YILAN OYUNU", YESIL, -150)
        
        rekor = rekoru_oku()
        mesaj_yaz(f"En İyi Süre: {rekor} saniye", SARI, -80)

        buton_olustur("BAŞLAT", 300, 300, 200, 50, YESIL, GRI, oyunu_baslat)
        buton_olustur("ÇIKIŞ", 300, 380, 200, 50, KIRMIZI, GRI, oyundan_cik)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                oyundan_cik()

        pygame.display.update()
        saat.tick(15)

def oyun_dongusu():
    oyun_bitti = False
    oyun_durdu = False
    zaman_kaydedildi = False
    final_sure = 0

    x1, y1 = GENISLIK / 2, YUKSEKLIK / 2
    x1_degisim, y1_degisim = 0, 0
    yilan_listesi = []
    yilan_uzunlugu = 1

    yiyecekx = round(random.randrange(0, GENISLIK - yilan_blok) / 20.0) * 20.0
    yiyeceky = round(random.randrange(0, YUKSEKLIK - yilan_blok) / 20.0) * 20.0

    baslangic_zamani = time.time()
    rekor = rekoru_oku()
    yeni_rekor_kirildi = False

    while not oyun_bitti:

        # --- OYUN BİTİŞ EKRANI (ÖLÜNCE) ---
        while oyun_durdu:
            ekran.fill(SIYAH)
            
            # Süreyi ve rekoru sadece bir kez hesaplayıp sabitliyoruz
            if not zaman_kaydedildi:
                final_sure = int(time.time() - baslangic_zamani)
                if final_sure > rekor:
                    rekoru_yaz(final_sure)
                    yeni_rekor_kirildi = True
                zaman_kaydedildi = True

            mesaj_yaz("OYUN BİTTİ!", KIRMIZI, -120)
            mesaj_yaz(f"Hayatta Kalma Süreniz: {final_sure} saniye", BEYAZ, -70)
            
            if yeni_rekor_kirildi:
                mesaj_yaz("YENİ REKOR!", SARI, -20)

            buton_olustur("TEKRAR OYNA", 150, 350, 200, 50, YESIL, GRI, oyunu_baslat)
            buton_olustur("ANA MENÜ", 450, 350, 200, 50, MAVI, GRI, ana_menu)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    oyundan_cik()
            
            pygame.display.update()
            saat.tick(15)

        # --- OYUN İÇİ KONTROLLER ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                oyundan_cik()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_degisim == 0:
                    x1_degisim = -yilan_blok
                    y1_degisim = 0
                elif event.key == pygame.K_RIGHT and x1_degisim == 0:
                    x1_degisim = yilan_blok
                    y1_degisim = 0
                elif event.key == pygame.K_UP and y1_degisim == 0:
                    y1_degisim = -yilan_blok
                    x1_degisim = 0
                elif event.key == pygame.K_DOWN and y1_degisim == 0:
                    y1_degisim = yilan_blok
                    x1_degisim = 0

        # Kenarlara Çarpma Kontrolü
        if x1 >= GENISLIK or x1 < 0 or y1 >= YUKSEKLIK or y1 < 0:
            oyun_durdu = True

        x1 += x1_degisim
        y1 += y1_degisim
        ekran.fill(SIYAH)
        
        # Yiyeceği Çiz
        pygame.draw.rect(ekran, KIRMIZI, [yiyecekx, yiyeceky, yilan_blok, yilan_blok])
        
        yilan_basi = [x1, y1]
        yilan_listesi.append(yilan_basi)
        if len(yilan_listesi) > yilan_uzunlugu:
            del yilan_listesi[0]

        # Kendi Kendine Çarpma Kontrolü
        for x in yilan_listesi[:-1]:
            if x == yilan_basi:
                oyun_durdu = True

        # Yılanı Çiz
        for segment in yilan_listesi:
            pygame.draw.rect(ekran, YESIL, [segment[0], segment[1], yilan_blok, yilan_blok])

        # Canlı Sayaç ve Rekor Gösterimi (Oyun Oynanırken)
        su_anli_sure = int(time.time() - baslangic_zamani)
        skor_metni = skor_fontu.render(f"Süre: {su_anli_sure} sn  |  Rekor: {rekor} sn", True, BEYAZ)
        ekran.blit(skor_metni, [10, 10])

        pygame.display.update()

        # Yiyecek Yeme Kontrolü
        if x1 == yiyecekx and y1 == yiyeceky:
            yiyecekx = round(random.randrange(0, GENISLIK - yilan_blok) / 20.0) * 20.0
            yiyeceky = round(random.randrange(0, YUKSEKLIK - yilan_blok) / 20.0) * 20.0
            yilan_uzunlugu += 1

        saat.tick(yilan_hizi)

# Uygulamayı Başlat
ana_menu()