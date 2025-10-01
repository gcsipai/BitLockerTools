==================================================
🔐 BitLockerTools (Citk 2025)
==================================================

BitLockerTools egy grafikus segédprogram (GUI), amely a Windows natív manage-bde.exe eszközét használja a BitLocker titkosítási műveletek (állapotlekérdezés, kulcsexportálás, felfüggesztés, kikapcsolás) egyszerűsítésére. A program CustomTkinter segítségével modern megjelenésű és felhasználóbarát felületet biztosít.

**************************************************
✨ FŐ FUNKCIÓK
**************************************************

- Állapot Lekérdezése: Gyorsan ellenőrzi a megadott meghajtó BitLocker állapotát (titkosítási státusz, verzió, védelem állapota).
- Helyreállítási Kulcs Exportálása: Kimentheti a BitLocker helyreállítási jelszavakat egy megadott TXT fájlba (normál felhasználói joggal).
- Felfüggesztés/Folytatás: Lehetővé teszi a BitLocker ideiglenes felfüggesztését a rendszergazdai műveletekhez (pl. BIOS frissítés). (Rendszergazdai jog szükséges!)
- Kikapcsolás (Dekódolás): Véglegesen kikapcsolja a BitLocker titkosítást. (Rendszergazdai jog szükséges!)
- Aszinkron Futtatás: A parancsokat külön szálon futtatja, elkerülve a grafikus felület lefagyását.

**************************************************
💻 RENDSZERKÖVETELMÉNYEK
**************************************************

- Operációs rendszer: Windows 10/11
- Windows kiadás: Csak a BitLockert támogató kiadásokon működik (általában Pro, Enterprise, Education). A Home kiadás nem támogatott, mivel nem tartalmazza a manage-bde.exe eszközt.
- Python: Python 3.x

**************************************************
🚀 TELEPÍTÉS ÉS FUTTATÁS
**************************************************

1. Függőségek (Requirements)
A programhoz a CustomTkinter nevű Python könyvtár szükséges.

    pip install customtkinter

2. A Program Indítása
A program futtatása a szükséges műveletektől függően eltérő jogosultságot igényel.

A) Normál Futtatás (Csak Állapot/Kulcs Export)
Az egyszerű állapotlekérdezéshez és a kulcsexportáláshoz általában elegendő a normál futtatás:

    python BitLockerTools-9.0.py

B) Rendszergazdai Futtatás (Felfüggesztés/Kikapcsolás)
A Felfüggesztés, Folytatás és Kikapcsolás műveletekhez RENDSZERGAZDAI JOGOSULTSÁG (Admin Jog) szükséges.

   - Keresse meg a Parancssort (CMD) vagy a PowerShellt a Windows keresőjében.
   - Kattintson jobb egérgombbal, és válassza a "Futtatás rendszergazdaként" opciót.
   - Navigáljon a szkript helyére, majd futtassa a parancsot:

    # Példa
    cd C:\Path\To\Script
    python BitLockerTools-9.0.py

**************************************************
⚠️ FONTOS MEGJEGYZÉS A JOGOSULTSÁGOKRÓL
**************************************************

- Ha a programot normál joggal indítja, a rendszergazdai funkciók gombjai inaktívak maradnak, és a program figyelmeztet.
- A legtöbb manage-bde parancsnál a Windows rendszergazdai jogot vár el. Ha normál joggal indítva próbál meg lekérni egy állapotot, valószínűleg "access denied" hibát kap.
- Mindig indítsa a programot RENDSZERGAZDAKÉNT, ha a Titkosítási műveletekkel (Pause/Resume/Disable) dolgozik!

**************************************************
🖼️ GRAFIKUS FELÜLET (GUI)
**************************************************

A program CustomTkinter segítségével készült, ami modern, témafüggő megjelenést biztosít a Tkinter felületeknek. A kimeneti naplóban az eredmények és a hibák színekkel vannak megkülönböztetve.

- Zöld: Sikeres művelet
- Piros: Hiba/Veszélyes művelet
- Sárga: Figyelmeztetés (pl. Admin jog hiánya)
- Kék: Információ

**************************************************
ELÉRHETŐSÉG ÉS KÉSZÍTŐ
**************************************************

Elérhetőség: https://github.com/gcsipai/BitLockerTools/
Készítette: Citk (2025)
