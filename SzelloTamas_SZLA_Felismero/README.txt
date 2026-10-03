------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

AI Számlafeldolgozó és Strukturált Adatkinyerő Rendszer

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Helyi környezetben (localhost) futó, Streamlit-alapú webalkalmazás, amely a Google Gemini API (GenAI SDK) segítségével automatizálja a PDF, és kép formátumú számlák feldolgozását. A rendszer 13 specifikus adatmezőt nyer ki JSON formátumban, majd az eredményeket közvetlenül a kódból felépített, formázott Excel fájlba exportálja (külső sablonfájl használata nélkül).

1. Rendszer, és funkciók
   -Kliensoldali UI: Reszponzív, böngészőből elérhető felület Drag & Drop fájlfeltöltéssel, lokális adatkezeléssel (a fájlok kizárólag a memóriában, és az API hívás erejéig  léteznek).
   -AI Adatkinyerés: A gemini-3.8-flash, és gemini-flash-latest modellek dinamikus használata, a számlák strukturált feldolgozására.

2. Hibakezelés, Kvótavédelem, és Vizuális Visszajelzés
  -Beépített védelem: A Google Free Tier kvótakorlátai (HTTP 429), és a szervertúlterhelések (HTTP 503) ellen, automatikus késleltetéssel, és újrapróbálkozási logikával. 
  -Mezőszintű hibajelzés: Amennyiben a modell nem talál meg egy adatot a számlán, vagy az érték hiányzik, a generált táblázat a „Megjegyzés” oszlopában megjelenik a „Hiba!” felirat, és a cella piros háttérszínt kap, a gyors auditálhatóság érdekében.
  -Adattisztítás: A hiányzó vonalkódok intelligens pótlása, a forrásfájl nevéből.
  -Excel Export: A strukturált adatok exportálása közvetlenül, a Python kód által létrehozott, és formázott Excel táblázatba (nincs szükség előre mentett sablonfájlra). A munkafüzet egyedi oszlopszélességeket, rácsvonalakat és futási időbélyeggel ellátott fájlnevet kap.

3. Projekt Felépítése, és Követelmények
   A futtatáshoz Python 3.9+ környezet, és egy aktív Google Gemini API kulcs (Google AI Studio) szükséges. 
   A kiadott csomag az alábbi elemekből áll:
    -Szamla_Web.py: A fő futtatókód, az adatkinyerési logika, az önálló Excel-generálás, és a Streamlit felület.
    -SzamlaFeldolgozo.bat: Windows shell parancsfájl, a virtuális környezet aktiválásához, és a webes felület elindításához.
    -requirements.txt: A program futtatásához elengedhetetlen Python könyvtárak (streamlit, google-genai, openpyxl, pydantic, pandas stb.) egzakt verziólistája.
    -README.txt: A program rövid ismertetője, telepítése, működése, technikai specifikációja.

3. Telepítési Útmutató:
   a) Csomagold ki a projektfájlokat, egy dedikált lokális mappába.
   b) Nyiss egy parancssort (CMD, vagy PowerShell) a mappa gyökerében.
   c) Hozz létre egy virtuális környezetet, majd aktiváld ezt:
	python -m venv .venv
	.venv\Scripts\activate

   d) Telepítsd a szükséges függőségeket, a mellékelt specifikációs fájlból:
        pip install -r requirements.txt

5. Futtatás és Használat:
   -Kényelmi indítás Windows környezetben: Futtasd a könyvtárban található SzamlaFeldolgozo.bat fájlt. Ez automatikusan aktiválja a Python környezetet, majd 
    elindítja a lokális Streamlit szervert, és az alapértelmezett böngészőben megnyitja az alkalmazást. 
    Alternatív, manuális indítás aktív virtuális környezetből: streamlit run Szamla_Web.py .

6. A program működése (számla feldolgozása):
   a) A böngészőben megnyíló felületen add meg az érvényes Gemini API kulcsodat (a beviteli mező maszkolt).
   b) Húzd be a feldolgozandó fájlokat (.pdf, .jpg, .jpeg, .png), a kijelölt feltöltő zónába.
   c) Kattints a "Feldolgozás indítása" gombra. A rendszer, az ingyenes kvóták túllépésének elkerülése érdekében, fájlonként 15 másodperces várakozási időt alkalmaz.
   d) A folyamatjelző (progress bar) lefutása után a kész, időbélyeggel ellátott Excel fájl közvetlenül letölthető a webes felületről. A letöltött fájl, 
      az operációs rendszer alapértelmezett letöltési mappájába kerül mentésre.
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
