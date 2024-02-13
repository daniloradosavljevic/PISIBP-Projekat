import unittest
from unittest.mock import patch
import pdb
from app import app

class TestKreirajNovosti(unittest.TestCase):

    
        def test_korisnik_nije_prijavljen(self):
            tester = app.test_client(self)
            response = tester.get("/cms/kreiraj_novosti", content_type="html/text")
            self.assertEqual(response.status_code, 302)  

    
        def test_korisnik_prijavljen(self):
            tester = app.test_client(self)
            with tester.session_transaction() as sess:
                sess["loggedin"] = True
                sess["id"] = 3  
            response = tester.get("/cms/kreiraj_novosti", content_type="html/text")
            self.assertEqual(response.status_code, 200) 

    
        def test_dodavanje_novosti(self):
            tester = app.test_client(self)
            with tester.session_transaction() as sess:
                sess["loggedin"] = True
                sess["id"] = 3
            data = {
                "title": "Naslov novosti",
                "category": "Kategorija",
                "content": "Sadržaj novosti",
                "tags": "tag1, tag2"
            }
            response = tester.post("/cms/kreiraj_novosti", data=data, follow_redirects=True)
            self.assertIn(b"prikaz_novosti", response.data)

class TestKomentarisi(unittest.TestCase):

    
        def test_get_request(self):
            tester = app.test_client(self)
            response = tester.get("/komentarisi/1", content_type="html/text")
            self.assertEqual(response.status_code, 200) 

   
        def test_post_request(self):
            tester = app.test_client(self)
            data = {"ime": "Test Ime", "komentar": "Ovo je test komentar."}
            response = tester.post("/komentarisi/1", data=data, follow_redirects=True)
            self.assertIn(b"komentarisi", response.data)  

   
        def simulate_login(self, tester, user_type):
            with tester.session_transaction() as sess:
                if user_type == "privileged":
                    sess["loggedin"] = True
                    sess["user_type"] = "Glavni urednik"  # 1: "Glavni urednik", 2: "Urednik", 3: "Novinar"
                else:
                    sess["loggedin"] = False

    
        def test_privileged_user_comment(self):
            tester = app.test_client(self)
            self.simulate_login(tester, user_type="privileged")
            data = {"ime": "Test Ime", "komentar": "Ovo je test komentar."}
            response = tester.post("/komentarisi/1", data=data, follow_redirects=True)
            self.assertIn(b"komentarisi", response.data)  

   
        def test_unprivileged_user_comment(self):
            tester = app.test_client(self)
            self.simulate_login(tester, user_type="unprivileged")
            data = {"ime": "Test Ime", "komentar": "Ovo je test komentar."}
            response = tester.post("/komentarisi/1", data=data, follow_redirects=True)
            self.assertNotIn(b"Niste uspesno objavili komentar", response.data) 

class TestLajkovanje(unittest.TestCase):

        
        def test_lajkovanje_vesti(self):
            tester = app.test_client(self)
            vest_id = 999 
            tip = 1  
            response = tester.post(f"/lajkovanje/{vest_id}/{tip}", follow_redirects=True)
            self.assertEqual(response.status_code, 200)  

        
        def test_dvostruko_lajkovanje_vesti(self):
            tester = app.test_client(self)
            vest_id = 1  
            tip = 1  

            
            tester.post(f"/lajkovanje/{vest_id}/{tip}", follow_redirects=True)

            
            response = tester.post(f"/lajkovanje/{vest_id}/{tip}", follow_redirects=True)
            self.assertEqual(response.status_code, 200)  
            

        
        def test_lajkovanje_neprijavljenog_korisnika(self):
            tester = app.test_client(self)
            vest_id = 1  
            tip = 1  

            
            response = tester.post(f"/lajkovanje/{vest_id}/{tip}", follow_redirects=True)
            self.assertEqual(response.status_code, 200)  

class TestLajkovanjeKomentara(unittest.TestCase):

        
        def test_lajkovanje_komentara(self):
            tester = app.test_client(self)
            komentar_id = 1  
            vest_id = 1  
            tip = 1  
            response = tester.post(f"/lajkovanje_komentara/{komentar_id}/{vest_id}/{tip}", follow_redirects=True)
            self.assertEqual(response.status_code, 200)  


        
        def test_dvostruko_lajkovanje_komentara(self):
            tester = app.test_client(self)
            komentar_id = 1  
            vest_id = 1  
            tip = 1  

            
            tester.post(f"/lajkovanje_komentara/{komentar_id}/{vest_id}/{tip}", follow_redirects=True)

            
            response = tester.post(f"/lajkovanje_komentara/{komentar_id}/{vest_id}/{tip}", follow_redirects=True)
            self.assertEqual(response.status_code, 200)

        
        def test_lajkovanje_neprijavljenog_korisnika(self):
            tester = app.test_client(self)
            komentar_id = 1 
            vest_id = 1  
            tip = 1  

            
            response = tester.post(f"/lajkovanje_komentara/{komentar_id}/{vest_id}/{tip}", follow_redirects=True)
            self.assertEqual(response.status_code, 200)  

        
        def test_lajkovanje_ne_postojecog_komentara(self):
            tester = app.test_client(self)
            komentar_id = 9999  
            vest_id = 1  
            tip = 1  

            
            response = tester.post(f"/lajkovanje_komentara/{komentar_id}/{vest_id}/{tip}", follow_redirects=True)
            self.assertEqual(response.status_code, 404)  

class TestZatraziOdobrenje(unittest.TestCase):

        
        def test_zatrazi_odobrenje_prijavljenog_korisnika(self):
            tester = app.test_client(self)
            with tester.session_transaction() as sess:
                sess["loggedin"] = True
                sess["id"] = 1  
            vest_id = 1  
            response = tester.get(f"/cms/zatrazi_odobrenje/{vest_id}", follow_redirects=True)
            self.assertEqual(response.status_code, 200)  

            

        
        def test_zatrazi_odobrenje_neprijavljenog_korisnika(self):
            tester = app.test_client(self)
            response = tester.get("/cms/login/1", follow_redirects=True)
            self.assertEqual(response.status_code, 404) 
        

        def test_zatrazi_odobrenje_ne_postojeca_vest(self):
            tester = app.test_client(self)
            with tester.session_transaction() as sess:
                sess["loggedin"] = True
                sess["id"] = 1  
            vest_id = 9999  
            response = tester.get(f"/cms/zatrazi_odobrenje/{vest_id}", follow_redirects=True)
            self.assertEqual(response.status_code, 404) 

class TestZatraziIzmenu(unittest.TestCase):

        # Testiranje zahtjeva za izmenu vesti kada je korisnik prijavljen
        def test_zatrazi_izmenu_prijavljenog_korisnika(self):
            tester = app.test_client(self)
            with tester.session_transaction() as sess:
                sess["loggedin"] = True
                sess["id"] = 1  # Postavite ID korisnika prema vašem testnom scenariju
            vest_id = 1  # Postavite ID vesti za koju želite zatražiti izmenu
            zahtev_tip = "Izmena"  # Postavite željeni tip zahtjeva
            response = tester.get(f"/cms/zatrazi_izmenu/{vest_id}?zahtev={zahtev_tip}", follow_redirects=True)
            self.assertEqual(response.status_code, 200)  # Provjerite da li je korisnik preusmjeren na stranicu za pregled novosti

            # Provjerite da li je zahtjev za izmenu uspješno dodan u bazu podataka (možete provjeriti direktno u bazi ili koristiti odgovarajući SQL upit za provjeru)


        # Testiranje zahtjeva za izmenu vesti koja ne postoji
        def test_zatrazi_izmenu_ne_postojeca_vest(self):
            tester = app.test_client(self)
            with tester.session_transaction() as sess:
                sess["loggedin"] = True
                sess["id"] = 1  # Postavite ID korisnika prema vašem testnom scenariju
            ne_postojeca_vest_id = 9999  # Postavite ID nepostojeće vesti
            zahtev_tip = "Izmena"  # Postavite željeni tip zahtjeva
            response = tester.get(f"/cms/zatrazi_izmenu/{ne_postojeca_vest_id}?zahtev={zahtev_tip}", follow_redirects=True)
            self.assertEqual(response.status_code, 404)  # Provjerite da li je korisnik preusmjeren na stranicu za pregled novosti

class TestOdobriZahtev(unittest.TestCase):

        # Testiranje odobravanja zahtjeva sa tipom 'Odobrenje'
        def test_odobri_zahtev_odobrenje(self):
            tester = app.test_client(self)
            with tester.session_transaction() as sess:
                sess["loggedin"] = True
                sess["uloga"] = 1  # Postavite ulogu korisnika prema vašem testnom scenariju
            id_zahteva = 1  # Postavite ID zahtjeva koji želite odobriti
            tip_zahteva = "Odobrenje"
            response = tester.post(f"/cms/odobri_zahtev/{id_zahteva}/{tip_zahteva}", follow_redirects=True)
            self.assertEqual(response.status_code, 200)  # Provjerite da li je korisnik preusmjeren

            # Provjerite da li je zahtjev uspješno odobren (možete provjeriti direktno u bazi ili koristiti odgovarajući SQL upit za provjeru)

        # Testiranje odobravanja zahtjeva sa tipom 'Izmena'
        def test_odobri_zahtev_izmena(self):
            tester = app.test_client(self)
            with tester.session_transaction() as sess:
                sess["loggedin"] = True
                sess["uloga"] = 2  # Postavite ulogu korisnika prema vašem testnom scenariju
            id_zahteva = 1  # Postavite ID zahtjeva koji želite odobriti
            tip_zahteva = "Izmena"
            response = tester.post(f"/cms/odobri_zahtev/{id_zahteva}/{tip_zahteva}", follow_redirects=True)
            self.assertEqual(response.status_code, 200)  # Provjerite da li je korisnik preusmjeren

class TestOdbijZahtev(unittest.TestCase):
        def setUp(self):
            # Pripremite testnu konfiguraciju ili postavite testnu aplikaciju
            app.testing = True
            self.app = app.test_client()

        def test_odbij_zahtev(self):
            # Pošaljite zahtjev na rutu
            response = self.app.post('/odbij_zahtev/1')
            
            # Provjerite da li je statusni kod odgovora 302 (preusmjeravanje)
            self.assertEqual(response.status_code, 302)
            
            # Provjerite da li je korisnik preusmjeren na prikaz_zahteva
            self.assertIn(b'/prikaz_zahteva', response.headers.get('Location'))

        def test_odbij_zahtev_neuspjesno_brisanje(self):
            # Simulirajte situaciju kada brisanje zahtjeva nije uspjelo
            with patch('app.mysql.connection.cursor') as mock_cursor:
                mock_cursor.return_value.execute.side_effect = Exception("Brisanje nije uspjelo")

                # Pošaljite zahtjev na rutu
                response = self.app.post('/odbij_zahtev/1')
                
                # Provjerite da li je statusni kod odgovora 302 (preusmjeravanje)
                self.assertEqual(response.status_code, 302)
                
                # Provjerite da li je korisnik preusmjeren na prikaz_zahteva
                self.assertIn(b'/prikaz_zahteva', response.headers.get('Location'))

                # Provjerite da li je ispisana poruka o grešci
                self.assertIn(b'Brisanje nije uspjelo', response.data)



if __name__ == "__main__":
    unittest.main()
