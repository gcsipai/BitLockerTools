Program neve: BitLockerTools (v7.1 - Citk 2025)

Leírás:

A BitLockerTools egy grafikus felhasználói felülettel (GUI) rendelkező segédprogram, amelyet a Microsoft BitLocker meghajtótitkosítási funkciójának egyszerűsített kezelésére terveztek Windows 10 és Windows 11 operációs rendszereken.

A program a Windows beépített manage-bde parancssori eszközét használja egy felhasználóbarát felületen keresztül, lehetővé téve a felhasználók számára a leggyakoribb BitLocker műveletek gyors elvégzését a meghajtókon.

Fő Funkciók (Képességek)
A program két fő műveletcsoportra osztja a funkciókat:

1. Általános Műveletek (Normál jogosultság is elegendő)
Állapot Lekérdezése 🔍: Megjeleníti egy kiválasztott meghajtó aktuális BitLocker állapotát (pl. titkosított, felfüggesztett, dekódolt).

Kulcs Exportálása 💾: Kinyeri és elmenti a Recovery Password (helyreállítási jelszó) típusú kulcsokat egy szöveges (.txt) fájlba. Ez kritikus fontosságú a meghajtó visszaállításához hardverhiba esetén.

2. Adminisztrációs Műveletek (Rendszergazdai jog szükséges)
Felfüggesztés ⏸️: Ideiglenesen kikapcsolja a BitLocker védelmet (pl. firmware frissítésekhez, diagnosztikához). Újraindítás után automatikusan folytatódik.

Folytatás ▶️: Visszakapcsolja a felfüggesztett BitLocker védelmet.

KIKAPCSOLÁS (Dekódolás) ⛔: Véglegesen eltávolítja a BitLocker titkosítást a meghajtóról. Ez egy hosszadalmas és visszafordíthatatlan művelet.

Fontos Kompatibilitási és Használati Feltételek
Windows Kiadás Követelménye: A program csak a BitLockert támogató Windows kiadásokkal működik:

Windows 10/11 Professional (Pro)

Windows 10/11 Enterprise

Windows 10/11 Education

Nem kompatibilis a Windows Home kiadással.

Rendszergazdai Jogosultság: A "Adminisztrációs Műveletek" csoportban lévő funkciók (Felfüggesztés, Folytatás, Kikapcsolás) használatához a programot RENDSZERGAZDAKÉNT kell indítani (Jobb gomb -> Futtatás rendszergazdaként).

Hibakezelés: A program beépített hibaellenőrzéssel rendelkezik, és hiba esetén pontos információt nyújt a felhasználónak a probléma okáról (pl. érvénytelen meghajtóbetű, manage-bde eszköz hiánya, vagy jogosultság hiánya).
