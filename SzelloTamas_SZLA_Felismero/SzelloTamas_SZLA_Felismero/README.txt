AI Számlafeldolgozó és Strukturált Adatkinyerő Rendszer
Helyi környezetben (localhost) futó, Streamlit-alapú webalkalmazás, amely a Google Gemini API (GenAI SDK) segítségével automatizálja a PDF és kép formátumú számlák feldolgozását. A rendszer 13 specifikus adatmezőt nyer ki JSON formátumban, majd az eredményeket egy előre strukturált Excel sablonba exportálja.

Rendszer és Funkciók
Kliensoldali UI: Reszponzív, böngészőből elérhető felület Drag & Drop fájlfeltöltéssel, lokális adatkezeléssel (a fájlok kizárólag a memóriában és az API hívás erejéig léteznek).

AI Adatkinyerés: A gemini-3.8-flash és gemini-flash-latest modellek dinamikus használata a számlák strukturált feldolgozására.

Hibakezelés és Kvótavédelem: Beépített védelem a Google Free Tier kvótakorlátai (HTTP 429) és a szervertúlterhelések (HTTP 503) ellen, automatikus késleltetéssel és újrapróbálkozási logikával.

Adattisztítás: Hiányzó vonalkódok intelligens pótlása a forrásfájl nevéből.

Excel Export: A kinyert adatok iteratív transzferálása a számla.xlsx sablonba, futási időbélyeggel ellátott letölthető fájlok generálása.

Projekt Felépítése és Követelmények
A futtatáshoz Python 3.9+ környezet és egy aktív Google Gemini API kulcs (Google AI Studio) szükséges. A kiadott csomag az alábbi elemekből áll:

	-Szamla_Web.py: A fő futtatókód és a Streamlit felület backend logikája.
	-szamla_sablon.xlsx: Az elvárt Excel sablon, amely tartalmazza a Szamlak munkalapot a 	 megfelelő formázással és oszlopfejlécekkel.
	-SzamlaFeldolgozo.bat: Windows shell parancsfájl a virtuális környezet aktiválásához 	 és a webes felület elindításához.
	-requirements.txt: A projekt futtatásához elengedhetetlen Python könyvtárak (pl. 	 streamlit, google-genai, openpyxl, pydantic, pandas) egzakt verziólistája.

Telepítési Útmutató:
1. Csomagold ki a projektfájlokat egy dedikált lokális mappába.
2. Nyiss egy parancssort (CMD vagy PowerShell) a mappa gyökerében.
3. Hozz létre egy virtuális környezetet, majd aktiváld azt:

python -m venv .venv
.venv\Scripts\activate

4. Telepítsd a szükséges függőségeket a mellékelt specifikációs fájlból:

pip install -r requirements.txt

Futtatás és Használat:
Kényelmi indítás Windows környezetben:
Futtasd a könyvtárban található SzamlaFeldolgozo.bat fájlt. Ez automatikusan aktiválja a Python környezetet, elindítja a lokális Streamlit szervert, és alapértelmezett böngészőben megnyitja az alkalmazást. (Alternatív, manuális indítás aktív virtuális környezetből: streamlit run Szamla_Web.py)

A program működése (számla feldolgozás):
1. A böngészőben megnyíló felületen add meg az érvényes Gemini API kulcsodat (a beviteli mező     maszkolt).
2. Húzd be a feldolgozandó fájlokat (.pdf, .jpg, .jpeg, .png) a kijelölt feltöltő zónába.
3. Kattints a "Feldolgozás indítása" gombra. A rendszer az ingyenes kvóták túllépésének elkerülése érdekében fájlonként 15 másodperces aszinkron várakozási időt alkalmaz.
4. A folyamatjelző (progress bar) lefutása után a kész, időbélyeggel ellátott Excel fájl közvetlenül letölthető a webes felületről. A letöltött file a windows "letöltések" mappájába kerül elmentésre.