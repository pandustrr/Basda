import psycopg2, os, time
#-------------------------------------------------------------------------------------------------------------------------------------------
# Menghubungkan ke database
db = psycopg2.connect(database='BasdaKK', user='postgres', password='123123', host='localhost', port='5432')
#-------------------------------------------------------------------------------------------------------------------------------------------
def menu_login():

    print(
        """
================================
|   \033[32mWelcome To Himpunan Kosong\033[0m  |
================================
|                               |
|        Silakan login          |
|        terlebih dahulu        |
|                               | 
|       0. Exit                 |
|_______________________________|
        """
    )

    while True:
        pilihan = input("Tekan Enter untuk melanjutkan...")
        if pilihan == '0':
            print("Keluar dari program...")
            time.sleep(1)
            os.system('cls')  
            db.close()  
            exit()  
        else:
            return  
            
#-------------------------------------------------------------------------------------------------------------------------------------------
def login(username, password):
    cursor = db.cursor()
    query = "SELECT * FROM login WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    cursor.close()
    return result
#-------------------------------------------------------------------------------------------------------------------------------------------


def dashboard():
    os.system('cls')
    print(
        f"""
===============================
|         \033[32mHalo Min :*\033[0m         |
===============================
|                             |
|  1. Profil Admin            |
|  2. Data Pesanan            |
|  3. Opname                  |
|  4. Edit Stok               |
|                             |
|  0. Logout                  |
|_____________________________|
    """
    )

#-------------------------------------------------------------------------------------------------------------------------------------------

def profil_admin(login_id_login):
    cursor = db.cursor()
    query = """
    SELECT admin.id_admin, admin.nama_admin, admin.no_telp_admin, alamat.alamat
    FROM admin
    JOIN alamat ON admin.alamat_id_alamat = alamat.id_alamat
    WHERE admin.login_id_login = %s
    """
    cursor.execute(query, (login_id_login,))
    result = cursor.fetchone()
    cursor.close()
    return result

#-------------------------------------------------------------------------------------------------------------------------------------------
def tampilkan_profil_admin(user):
    login_id_login = user[0]
    data_admin = profil_admin(login_id_login)
    if data_admin:
        id_admin, nama_admin, no_telp_admin, alamat_admin = data_admin
        print(
            f"""
================================================
            \033[32mProfil Admin\033[0m          
================================================
    ID Admin: {id_admin}                                  
    Nama: {nama_admin}                           
    No. Telp: {no_telp_admin}                    
    Alamat: {alamat_admin}                       
_______________________________________________
            """
        )
    else:
        print("Data admin tidak ditemukan.")

#-------------------------------------------------------------------------------------------------------------------------------------------

def menu_data_pesanan():
    os.system('cls')
    print(
        f"""
===============================
|         \033[32mData Pesanan \033[0m       |
===============================
|                             |
|  1. Buat Pesanan            |
|  2. Daftar Pesanan          |
|                             |
|  0. Back                    |
|_____________________________|
    """
    )

#-------------------------------------------------------------------------------------------------------------------------------------------
def buat_pesanan():
    os.system('cls')
    print(
        f"""
===============================
|       \033[32mBuat Pesanan\033[0m         |
===============================
        """
    )
#-------------------------------------------------------------------------------------------------------------------------------------------
def input_data_pesanan():
    pilihan_data_pesanan = input("Pilih Nomor = ")
    while True:
        if pilihan_data_pesanan == '1':
            buat_pesanan()
            break   
        elif pilihan_data_pesanan == '2':
            print('daftar pesanan')
        elif pilihan_data_pesanan == '0':
            break




#-------------------------------------------------------------------------------------------------------------------------------------------

def input_dashboard():

    while True:
        pilihan_dashboard = input("Pilih Nomor = ")

        if pilihan_dashboard == '1':
            tampilkan_profil_admin(user)
            input("Tekan Enter untuk kembali ke dashboard...")
            dashboard()
        elif pilihan_dashboard == '2':
            menu_data_pesanan()
            input_data_pesanan()
            break
        elif pilihan_dashboard == '3':
            print('3')
            break
        elif pilihan_dashboard == '4':
            print('4')
            break

        elif pilihan_dashboard == '0':
            break

#-------------------------------------------------------------------------------------------------------------------------------------------

# Program utama
menu_login()
while True:
    username = input("Username: ")
    password = input("Password: ")

    user = login(username, password)

    if user:
        print("Login berhasil!")
        print(f"Selamat datang, {username}!")
        time.sleep(1.5)
        os.system('cls') 
        dashboard()
        input_dashboard()

    else:
        print("Login gagal! Username atau password salah.")
        time.sleep(1.5)
        os.system('cls')
        menu_login()        

db.close()
#-------------------------------------------------------------------------------------------------------------------------------------------
