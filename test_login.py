import unittest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@allure.suite('Login Tests')
class LoginTests(unittest.TestCase):

    def setUp(self):
        """Test başlatmadan önce bir kez çalışır."""
        # WebDriver'ı başlat ve pencereyi maksimum yap
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    @allure.testcase('https://www.beymen.com/tr/customer/login?returnUrl=/tr/customer')
    @allure.title('Başarılı Giriş Testi')
    def test_successful_login(self):
        """Başarılı giriş testi"""
        driver = self.driver
        driver.get("https://www.beymen.com/tr/customer/login?returnUrl=/tr/customer")

        try:
            # Çerez onayı varsa, kabul et
            try:
                accept_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
                )
                accept_button.click()
            except:
                pass  # Eğer çerez onayı yoksa, hata vermez.

            # Kullanıcı adı ve şifre gir
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "customerEmail"))
            ).send_keys("busezmz@outlook.com")

            driver.find_element(By.ID, "password").send_keys("Barbie123")
            
            # Sayfayı kaydırarak butona ulaş
            login_button = driver.find_element(By.ID, "loginBtn")
            driver.execute_script("arguments[0].scrollIntoView();", login_button)

            # Butona tıklanabilir olduğunda tıklayın
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "loginBtn"))
            ).click()

            # Doğrulama: Sayfanın yüklenmesini bekle
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "welcomeMessage"))
            )
            welcome_message = driver.find_element(By.ID, "welcomeMessage").text
            self.assertIn("Hoş Geldiniz", welcome_message, "Giriş başarısız!")
            allure.step('Başarılı giriş testi başarılı!')
            print("Test Başarılı: Başarılı giriş.")

        except Exception as e:
            print(f"Test Başarısız: {e}")
            allure.attach(str(e), name="Test Hatası", attachment_type=allure.attachment_type.TEXT)

    @allure.testcase('https://www.beymen.com/tr/customer/login?returnUrl=/tr/customer')
    @allure.title('Başarısız Giriş Testi')
    def test_unsuccessful_login(self):
        """Başarısız giriş testi"""
        driver = self.driver
        driver.get("https://www.beymen.com/tr/customer/login?returnUrl=/tr/customer")

        try:
            # Çerez onayı varsa, kabul et
            try:
                accept_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
                )
                accept_button.click()
            except:
                pass  # Eğer çerez onayı yoksa, hata vermez.

            # Hatalı giriş bilgilerini gir
            driver.find_element(By.ID, "customerEmail").send_keys("invalidUser@example.com")
            driver.find_element(By.ID, "password").send_keys("wrongPassword123")

            # Sayfayı kaydırarak butona ulaş
            login_button = driver.find_element(By.ID, "loginBtn")
            driver.execute_script("arguments[0].scrollIntoView();", login_button)

            # Butona tıklanabilir olduğunda tıklayın
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "loginBtn"))
            ).click()

            # Hata mesajını kontrol et
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "error-message"))
            )
            warning_message = driver.find_element(By.CLASS_NAME, "error-message").text
            self.assertEqual(warning_message, "E-posta adresiniz ve/veya şifreniz hatalı.", "Hata mesajı doğru değil.")
            allure.step('Başarısız giriş testi başarılı')
            print("Başarısız giriş testi geçti")

        except Exception as e:
            print(f"Test Başarısız: {e}")
            allure.attach(str(e), name="Test Hatası", attachment_type=allure.attachment_type.TEXT)

    @allure.testcase('https://www.beymen.com/tr/customer/login?returnUrl=/tr/customer')
    @allure.title('Boş Alanlar Testi')
    def test_empty_fields(self):
        """Boş alanlar testi"""
        driver = self.driver
        driver.get("https://www.beymen.com/tr/customer/login?returnUrl=/tr/customer")

        try:
            # Çerez onayı varsa, kabul et
            try:
                accept_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
                )
                accept_button.click()
            except:
                pass  # Eğer çerez onayı yoksa, hata vermez.

            # Sayfayı kaydırarak butona ulaş
            login_button = driver.find_element(By.ID, "loginBtn")
            driver.execute_script("arguments[0].scrollIntoView();", login_button)

            # Boş alanları gönder
            driver.find_element(By.ID, "customerEmail").send_keys("")
            driver.find_element(By.ID, "password").send_keys("")
            driver.find_element(By.CSS_SELECTOR, ".loginBtn").click()

            # Uyarı mesajını kontrol et
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "error-message"))
            )
            empty_fields_message = driver.find_element(By.CLASS_NAME, "error-message").text
            self.assertEqual(empty_fields_message, "Lütfen tüm alanları doldurun.", "Boş alanlar için doğru uyarı verilmedi.")
            allure.step('Boş alanlar testi başarılı')
            print("Boş alanlar testi geçti")

        except Exception as e:
            print(f"Test Başarısız: {e}")
            allure.attach(str(e), name="Test Hatası", attachment_type=allure.attachment_type.TEXT)

    def tearDown(self):
        """Test bittikten sonra bir kez çalışır."""
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
