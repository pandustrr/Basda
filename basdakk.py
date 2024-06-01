import psycopg2, os, time
#-------------------------------------------------------------------------------------------------------------------------------------------
# Menghubungkan ke database
db = psycopg2.connect(database='BasdaKK', user='postgres', password='afan28', host='localhost', port='5432')
#-------------------------------------------------------------------------------------------------------------------------------------------
def menu_login():
    print(
        """
===============================
|   \033[32mWelcome To Himpunan Kosong\033[0m |
===============================
|                             |
|       Silakan login         |
|      terlebih dahulu        |
|                             |
|_____________________________|
        """
    ) 
#-------------------------------------------------------------------------------------------------------------------------------------------
def login(username, password):
    cursor = db.cursor()
    query = "SELECT * FROM login WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    cursor.close()
    return result
#-------------------------------------------------------------------------------------------------------------------------------------------

def admin_menu():
    os.system('cls')
    print(
        f"""
===============================
|         \033[32mHalo Min :*\033[0m         |
===============================
|                             |
|  1. Profil Pegawai          |
|  2. Data Pesanan            |
|  3. Opname                  |
|  4. Edit Stok               |
|                             |
|  0. Logout                  |
|_____________________________|
    """
    )

















#-------------------------------------------------------------------------------------------------------------------------------------------
# Program utama
menu_login()
input("Tekan Enter untuk melanjutkan...")

while True:
    username = input("Username: ")
    password = input("Password: ")

    user = login(username, password)

    if user:
        print("Login berhasil!")
        print(f"Selamat datang, {username}!")
        time.sleep(1.5)
        os.system('cls') 
        break
    else:
        print("Login gagal! Username atau password salah.")
        time.sleep(1.5)
        os.system('cls')
        menu_login()
        

db.close()
#-------------------------------------------------------------------------------------------------------------------------------------------