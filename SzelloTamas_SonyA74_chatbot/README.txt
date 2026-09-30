Sony A7 IV RAG Fotós Asszisztens – Felhasználói Útmutató

Helyi, böngészőalapú csevegőalkalmazás, amely beágyazott Python HTTP proxyn keresztül kommunikál a távoli Flowise RAG rendszerrel, és a Sony Alpha 7 IV kezelési útmutatójára támaszkodva ad strukturált beállítási javaslatokat.

Mappaszerkezet:
-SZT_SonyA7IV_Chatbot_Html.py   -Beágyazott HTTP webszerver és Flowise API proxy
-SZT_SonyA7IV_Chatbot.bat       -Automatikus indítószkript (környezet- és függőségkezeléssel)
-README.txt                     -Rendszerleírás és futtatási útmutató

Rendszerkövetelmények és előfeltételek:
-Operációs rendszer: Windows 10 / 11
-Python verzió: Python 3.9 vagy újabb

Külső csomag: requests könyvtár

Hálózat: Aktív internetkapcsolat a Flowise API végpont eléréséhez

A chatbot futtatása:
1. Indítás Batch fájllal (SZT_SonyA7IV_Chatbot.bat)
Ajánlott gyorsindítási mód mindennapi használatra.
-Győződjön meg arról, hogy az SZT_SonyA7IV_Chatbot.bat és a 	SZT_SonyA7IV_Chatbot_Html.py   ugyanabban a mappában található.
-Kattintson duplán az SZT_SonyA7IV_Chatbot.bat fájlra.

A parancsfájl automatikusan elvégzi a következőket:
-Megkeresi az elérhető Python futtatót (a PyCharm .venv / venv mappájában vagy a rendszer PATH-jában).
-Ellenőrzi és szükség esetén telepíti a hiányzó requests csomagot.
-Elindítja a helyi HTTP szervert.
-Automatikusan megnyitja az alapértelmezett webböngészőben a felületet ([http://127.0.0.1:8080](http://127.0.0.1:8080)).