# PISIBP-Projekat

Projekat iz predmeta Projektovanje Informacionih Sistema i Baza Podataka.

Danilo Radosavljević 647-2020 Backend Engineer  
Veljko Vesić 655-2020 Frontend Engineer  
Aleksa Atanasković 658-2020 Quality Assurance Engineer  
Lazar Marković 637-2020 DevOps/system/infra engineer  

Projektni zadatak iz predmeta "Projektovanje Informacionih Sistema i Baza Podataka" - portal elektronskih novina. Tehnologije koje su korišćene pri izradi aplikacije jesu Python microframework Flask, i MySQL baza podataka. 

Uputstvo za pokretanje aplikacije:
- Instalirajte Python 3.8.10
- Instalirajte requirements.txt u terminalu korišćenjem: pip install -r requirements. txt 
- Instalirajte WampServer 3.3.2 -64bitnu verziju
- Pokrenite WampServer
-Ulogujte se u PhpMyAdmin
- Importujte bazu podataka, tako što ćete kreirati bazu sa nazivom "baze" i prekopirati tekst iz bazapodataka.txt u SQL tab
- Kreirajte 9125 članaka u terminalu sa - python skripta.py
- Pokrenite aplikaciju u terminalu korišćenjem: python app.py
  
NAPOMENA: Što se tiče Devops-a, napravljeni su odvojeni kontejneri za Flask Aplikaciju i MySQL bazu podataka, ali nije uspešno rešen problem pri povezivanju ove dve komponente (Funkcioniše sa određenim stranicama, ali ne sa onim koje koriste bazu podataka). Verovatano je zbog verzija Pythona i MySQL-a. 
