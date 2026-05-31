import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.keys import Keys

@pytest.fixture()
def driver():
    driver = webdriver.Chrome()
    driver.get("https://www.saucedemo.com/")
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def helper_login(driver, username="standard_user", password="secret_sauce"):
    driver.find_element(By.ID, "user-name").clear()
    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").clear()
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()

# ==============================================================================
# 🟢 KELOMPOK 20 TEST CASE POSITIF (test_pos_01 s/d test_pos_20)
# ==============================================================================

# TC01: Login sukses dengan standard_user
def test_pos_01_login_standard_user(driver):
    helper_login(driver, "standard_user")
    assert "inventory.html" in driver.current_url

# TC02: Login sukses dengan problem_user
def test_pos_02_login_problem_user(driver):
    helper_login(driver, "problem_user")
    assert "inventory.html" in driver.current_url

# TC03: Login sukses dengan performance_glitch_user
def test_pos_03_login_performance_user(driver):
    helper_login(driver, "performance_glitch_user")
    assert "inventory.html" in driver.current_url

# TC04: Verifikasi daftar produk muncul di halaman utama
def test_pos_04_verify_products_displayed(driver):
    helper_login(driver)
    items = driver.find_elements(By.CLASS_NAME, "inventory_item")
    assert len(items) > 0

# TC05: Mengurutkan produk berdasarkan Nama (A ke Z)
def test_pos_05_sort_name_a_z(driver):
    helper_login(driver)
    dropdown = Select(driver.find_element(By.CLASS_NAME, "product_sort_container"))
    dropdown.select_by_value("az")
    first_item = driver.find_element(By.CLASS_NAME, "inventory_item_name").text
    assert "Sauce Labs Backpack" == first_item

# TC06: Mengurutkan produk berdasarkan Nama (Z ke A)
def test_pos_06_sort_name_z_a(driver):
    helper_login(driver)
    dropdown = Select(driver.find_element(By.CLASS_NAME, "product_sort_container"))
    dropdown.select_by_value("za")
    first_item = driver.find_element(By.CLASS_NAME, "inventory_item_name").text
    assert "Test.allTheThings() T-Shirt (Red)" == first_item

# TC07: Mengurutkan produk berdasarkan Harga (Rendah ke Tinggi)
def test_pos_07_sort_price_low_high(driver):
    helper_login(driver)
    dropdown = Select(driver.find_element(By.CLASS_NAME, "product_sort_container"))
    dropdown.select_by_value("lohi")
    first_price = driver.find_element(By.CLASS_NAME, "inventory_item_price").text
    assert "$7.99" == first_price

# TC08: Mengurutkan produk berdasarkan Harga (Tinggi ke Rendah)
def test_pos_08_sort_price_high_low(driver):
    helper_login(driver)
    dropdown = Select(driver.find_element(By.CLASS_NAME, "product_sort_container"))
    dropdown.select_by_value("hilo")
    first_price = driver.find_element(By.CLASS_NAME, "inventory_item_price").text
    assert "$49.99" == first_price

# TC09: Membuka menu navigasi sidebar
def test_pos_09_open_sidebar_menu(driver):
    helper_login(driver)
    driver.find_element(By.ID, "react-burger-menu-btn").click()
    time.sleep(1)
    sidebar_nav = driver.find_element(By.CLASS_NAME, "bm-menu-wrap")
    assert sidebar_nav.is_displayed()

# TC10: Masuk ke halaman detail produk saat judul produk diklik
def test_pos_10_navigate_to_product_detail(driver):
    helper_login(driver)
    driver.find_element(By.ID, "item_4_title_link").click()
    WebDriverWait(driver, 10).until(EC.url_contains("id=4"))
    assert "id=4" in driver.current_url

# TC11: Kembali ke halaman utama menggunakan tombol "Back to products"
def test_pos_11_back_to_products_from_detail(driver):
    helper_login(driver)
    driver.find_element(By.ID, "item_4_title_link").click()
    
    # Pastikan tombol back sudah bisa diklik
    back_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "back-to-products")))
    back_btn.click()
    
    # Tunggu sampai URL mengandung 'inventory.html'
    WebDriverWait(driver, 10).until(EC.url_contains("inventory.html"))
    assert "inventory.html" in driver.current_url

# TC12: Menambahkan 1 produk ke keranjang dari halaman utama
def test_pos_12_add_single_item_to_cart(driver):
    helper_login(driver)
    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
    assert badge == "1"

# TC13: Menambahkan beberapa produk sekaligus ke keranjang
def test_pos_13_add_multiple_items_to_cart(driver):
    helper_login(driver)
    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    driver.find_element(By.ID, "add-to-cart-sauce-labs-bike-light").click()
    badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
    assert badge == "2"

# TC14: Menambahkan produk ke keranjang dari halaman detail produk
def test_pos_14_add_item_from_detail_page(driver):
    helper_login(driver)
    driver.find_element(By.ID, "item_4_title_link").click()
    driver.find_element(By.ID, "add-to-cart").click()
    badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
    assert badge == "1"

# TC15: Menghapus produk dari keranjang melalui halaman utama
def test_pos_15_remove_item_from_inventory(driver):
    helper_login(driver)
    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    driver.find_element(By.ID, "remove-sauce-labs-backpack").click()
    badges = driver.find_elements(By.CLASS_NAME, "shopping_cart_badge")
    assert len(badges) == 0

# TC16: Mengakses halaman daftar keranjang belanja (Cart)
def test_pos_16_navigate_to_cart_page(driver):
    helper_login(driver)
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    assert "cart.html" in driver.current_url

# TC17: Menghapus produk dari dalam halaman keranjang belanja
def test_pos_17_remove_item_from_cart_page(driver):
    helper_login(driver)
    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    driver.find_element(By.ID, "remove-sauce-labs-backpack").click()
    time.sleep(1)
    items = driver.find_elements(By.CLASS_NAME, "cart_item")
    assert len(items) == 0

# TC18: Melanjutkan alur dari halaman Cart ke Halaman Form Informasi Checkout
def test_pos_18_proceed_to_checkout_step_one(driver):
    helper_login(driver)
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    driver.find_element(By.ID, "checkout").click()
    assert "checkout-step-one.html" in driver.current_url

# TC19: Mengisi informasi checkout dengan lengkap dan valid
def test_pos_19_fill_checkout_info_valid(driver):
    helper_login(driver)
    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    
    # Paksa klik checkout
    checkout_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "checkout")))
    driver.execute_script("arguments[0].click();", checkout_btn)
    
    # Isi data form
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "first-name"))).send_keys("Budi")
    driver.find_element(By.ID, "last-name").send_keys("Santoso")
    driver.find_element(By.ID, "postal-code").send_keys("12345")
    
    # Klik continue
    continue_btn = driver.find_element(By.ID, "continue")
    driver.execute_script("arguments[0].click();", continue_btn)
    
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "finish")))

    assert "checkout-step-two.html" in driver.current_url

# TC20: Menyelesaikan transaksi hingga halaman sukses
def test_pos_20_complete_checkout_workflow(driver):
    helper_login(driver)
    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    
    # Checkout
    checkout_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "checkout")))
    driver.execute_script("arguments[0].click();", checkout_btn)
    
    # Isi form
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "first-name"))).send_keys("Budi")
    driver.find_element(By.ID, "last-name").send_keys("Santoso")
    driver.find_element(By.ID, "postal-code").send_keys("12345")
    
    # Klik Continue
    continue_btn = driver.find_element(By.ID, "continue")
    driver.execute_script("arguments[0].click();", continue_btn)
    
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "summary_info")))
    
    finish_btn = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, "finish")))
    driver.execute_script("arguments[0].click();", finish_btn)
    
    complete_msg = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "complete-header"))).text
    assert "Thank you for your order!" == complete_msg

# ==============================================================================
# 🔴 KELOMPOK 20 TEST CASE NEGATIF (test_neg_01 s/d test_neg_20)
# ==============================================================================

# TC01: Login gagal karena akun diblokir (locked_out_user)
def test_neg_01_login_locked_out(driver):
    helper_login(driver, "locked_out_user")
    error_msg = driver.find_element(By.CSS_SELECTOR, "[data-test='error']").text
    assert "locked out" in error_msg

# TC02: Login gagal karena Username salah
def test_neg_02_login_wrong_username(driver):
    helper_login(driver, "user_salah", "secret_sauce")
    error_msg = driver.find_element(By.CSS_SELECTOR, "[data-test='error']").text
    assert "do not match" in error_msg

# TC03: Login gagal karena Password salah
def test_neg_03_login_wrong_password(driver):
    helper_login(driver, "standard_user", "password_salah")
    error_msg = driver.find_element(By.CSS_SELECTOR, "[data-test='error']").text
    assert "do not match" in error_msg

# TC04: Login gagal karena kolom Username dikosongkan
def test_neg_04_login_empty_username(driver):
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    error_msg = driver.find_element(By.CSS_SELECTOR, "[data-test='error']").text
    assert "Username is required" in error_msg

# TC05: Login gagal karena kolom Password dikosongkan
def test_neg_05_login_empty_password(driver):
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "login-button").click()
    error_msg = driver.find_element(By.CSS_SELECTOR, "[data-test='error']").text
    assert "Password is required" in error_msg

# TC06: Login gagal karena seluruh kolom dikosongkan
def test_neg_06_login_all_fields_empty(driver):
    driver.find_element(By.ID, "login-button").click()
    error_msg = driver.find_element(By.CSS_SELECTOR, "[data-test='error']").text
    assert "Username is required" in error_msg

# TC07: Login gagal menggunakan percobaan karakter SQL Injection
def test_neg_07_login_sql_injection(driver):
    helper_login(driver, "' OR '1'='1", "' OR '1'='1")
    error_msg = driver.find_element(By.CSS_SELECTOR, "[data-test='error']").text
    assert "do not match" in error_msg

# TC08: Login gagal menggunakan karakter spesial acak
def test_neg_08_login_special_characters(driver):
    helper_login(driver, "!@#$%^&*", "secret_sauce")
    error_msg = driver.find_element(By.CSS_SELECTOR, "[data-test='error']").text
    assert "do not match" in error_msg

# TC09: Login gagal karena sensitivitas huruf besar/kecil (Caps Lock) pada Username
def test_neg_09_login_case_sensitive_username(driver):
    helper_login(driver, "STANDARD_USER", "secret_sauce")
    error_msg = driver.find_element(By.CSS_SELECTOR, "[data-test='error']").text
    assert "do not match" in error_msg

# TC10: Checkout gagal karena semua kolom informasi dikosongkan
def test_neg_10_checkout_all_fields_empty(driver):
    helper_login(driver)
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    driver.find_element(By.ID, "checkout").click()
    driver.find_element(By.ID, "continue").click()
    error_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='error']")))
    error_msg = error_element.text
    assert "First Name is required" in error_msg

# TC11: Checkout gagal karena kolom First Name dikosongkan
def test_neg_11_checkout_missing_first_name(driver):
    helper_login(driver)
    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    
    checkout_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "checkout")))
    driver.execute_script("arguments[0].click();", checkout_btn)
    
    WebDriverWait(driver, 10).until(EC.url_contains("checkout-step-one.html"))
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "last-name"))).send_keys("Santoso")
    driver.find_element(By.ID, "postal-code").send_keys("12345")
    
    continue_btn = driver.find_element(By.ID, "continue")
    driver.execute_script("arguments[0].click();", continue_btn)
    
    error_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']")))
    assert "First Name is required" in error_element.text

# TC12: Checkout gagal karena kolom Last Name dikosongkan
def test_neg_12_checkout_missing_last_name(driver):
    helper_login(driver)
    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    
    checkout_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "checkout")))
    driver.execute_script("arguments[0].click();", checkout_btn)
    
    WebDriverWait(driver, 10).until(EC.url_contains("checkout-step-one.html"))
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "first-name"))).send_keys("Budi")
    driver.find_element(By.ID, "postal-code").send_keys("12345")
    
    continue_btn = driver.find_element(By.ID, "continue")
    driver.execute_script("arguments[0].click();", continue_btn)
    
    error_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']")))
    assert "Last Name is required" in error_element.text

# TC13: Checkout gagal karena kolom Postal Code dikosongkan
def test_neg_13_checkout_missing_postal_code(driver):
    helper_login(driver)
    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    
    checkout_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "checkout")))
    driver.execute_script("arguments[0].click();", checkout_btn)
    
    WebDriverWait(driver, 10).until(EC.url_contains("checkout-step-one.html"))
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "first-name"))).send_keys("Budi")
    driver.find_element(By.ID, "last-name").send_keys("Santoso")
    
    continue_btn = driver.find_element(By.ID, "continue")
    driver.execute_script("arguments[0].click();", continue_btn)
    
    error_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']")))
    assert "Postal Code is required" in error_element.text

# TC14: Checkout gagal karena hanya mengisi kolom Postal Code
def test_neg_14_checkout_only_fill_postal_code(driver):
    helper_login(driver)
    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    
    checkout_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "checkout")))
    driver.execute_script("arguments[0].click();", checkout_btn)
    
    WebDriverWait(driver, 10).until(EC.url_contains("checkout-step-one.html"))
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "postal-code"))).send_keys("12345")
    
    continue_btn = driver.find_element(By.ID, "continue")
    driver.execute_script("arguments[0].click();", continue_btn)
    
    error_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']")))
    assert "First Name is required" in error_element.text

# TC15: Checkout gagal karena hanya mengisi kolom First Name
def test_neg_15_checkout_only_fill_first_name(driver):
    helper_login(driver)
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    driver.find_element(By.ID, "checkout").click()
    
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "first-name")))
    driver.find_element(By.ID, "first-name").send_keys("Budi")
    driver.find_element(By.ID, "continue").click()
    
    error_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']")))
    assert "Last Name is required" in error_element.text

# TC16: Checkout gagal karena hanya mengisi kolom Last Name
def test_neg_16_checkout_only_fill_last_name(driver):
    helper_login(driver)
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    driver.find_element(By.ID, "checkout").click()
    driver.find_element(By.ID, "last-name").send_keys("Santoso")
    driver.find_element(By.ID, "continue").click()
    error_msg = driver.find_element(By.CSS_SELECTOR, "[data-test='error']").text
    assert "First Name is required" in error_msg

# TC17: Akses paksa URL halaman Inventory langsung tanpa login
def test_neg_17_direct_url_inventory_without_login(driver):
    driver.get("https://www.saucedemo.com/inventory.html")
    error_msg = driver.find_element(By.CSS_SELECTOR, "[data-test='error']").text
    assert "You can only access" in error_msg

# TC18: Akses paksa URL halaman Cart langsung tanpa login
def test_neg_18_direct_url_cart_without_login(driver):
    driver.get("https://www.saucedemo.com/cart.html")
    error_msg = driver.find_element(By.CSS_SELECTOR, "[data-test='error']").text
    assert "You can only access" in error_msg

# TC19: Akses paksa URL halaman Checkout Step One langsung tanpa login
def test_neg_19_direct_url_checkout_one_without_login(driver):
    driver.get("https://www.saucedemo.com/checkout-step-one.html")
    error_msg = driver.find_element(By.CSS_SELECTOR, "[data-test='error']").text
    assert "You can only access" in error_msg

# TC20: Akses paksa URL halaman Checkout Step Two langsung tanpa login
def test_neg_20_direct_url_checkout_two_without_login(driver):
    driver.get("https://www.saucedemo.com/checkout-step-two.html")
    error_msg = driver.find_element(By.CSS_SELECTOR, "[data-test='error']").text
    assert "You can only access" in error_msg