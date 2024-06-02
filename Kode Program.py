import psycopg2
import getpass
import pandas as pd
import os
import time

# Fungsi untuk menampilkan menu login
def menu_login():
    print(
        """
=================================
|          \033[32mWelcome To           |
|   Inventory Himpunan Kosong\033[0m   |
=================================
|                               |
|        Silakan login          |
|        terlebih dahulu        |
|                               | 
|       0. Exit                 |
|_______________________________|
        """
    )

# Fungsi untuk menampilkan dashboard
def dashboard():
    os.system('cls')   
    print(
        f"""
===============================
|         \033[32mHalo Min :*\033[0m         |
===============================
|                             |
|  1. Profil Admin            |
|  2. Memesan dan Edit stok   |
|  3. Opname                  |
|  4. Update Profil Admin     |
|  5. Ubah Username/Password  |
|                             |
|                             |
|  0. Logout                  |
|_____________________________|
    """
    )

# Koneksi ke database PostgreSQL
conn = psycopg2.connect(database='BasdaHK', user='postgres', password='123123', host='localhost', port='5432')
cursor = conn.cursor()

# Fungsi login
def login():
    while True:
        menu_login()
        choice = getpass.getpass("Tekan enter untuk melanjutkan... ")
        if choice == '0':
            return None
        username = input("Masukkan username: ")
        password = getpass.getpass("Masukkan password: ")
        cursor.execute("SELECT id_login FROM login WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        if user:
            cursor.execute("SELECT id_admin FROM admin WHERE login_id_login = %s", (user[0],))
            admin = cursor.fetchone()
            if admin:
                return admin[0]
        print("\nLogin gagal! Periksa username dan password Anda.")
        time.sleep(1.5)
        os.system('cls')

# Fungsi untuk mengubah username dan password admin
def ubah_username_password(admin_id):
    os.system('cls')
    print("Ubah Username dan Password\n")
    print("----------------------------")
    username_baru = input("Masukkan username baru (kosongkan jika tidak ingin mengubah): ")
    password_baru = getpass.getpass("Masukkan password baru (kosongkan jika tidak ingin mengubah): ")

    try:
        if username_baru:
            cursor.execute("UPDATE login SET username = %s WHERE id_login IN (SELECT login_id_login FROM admin WHERE id_admin = %s)", (username_baru, admin_id))
        
        if password_baru:
            cursor.execute("UPDATE login SET password = %s WHERE id_login IN (SELECT login_id_login FROM admin WHERE id_admin = %s)", (password_baru, admin_id))
        
        conn.commit()
        print("Username dan password berhasil diperbarui.")
    except Exception as e:
        conn.rollback()
        print("Terjadi kesalahan saat memperbarui username dan password:", e)
    finally:
        time.sleep(1.2)
        os.system('cls')

        

# Fungsi untuk menampilkan profil admin
def tampilkan_profil(admin_id):
    cursor.execute("""
        SELECT a.id_admin, a.nama_admin, a.no_telp_admin, al.alamat
        FROM admin a
        JOIN alamat al ON a.alamat_id_alamat = al.id_alamat
        WHERE a.id_admin = %s
    """, (admin_id,))
    profil = cursor.fetchone()
    if profil:
        id_admin, nama_admin, no_telp_admin, alamat_admin = profil
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
        input("Tekan Enter untuk kembali ke Dashboard...")

# Fungsi untuk memperbarui profil admin
def update_profil(admin_id):
    os.system('cls')
    print("Update Profil Admin\n")
    print("----------------------------")
    nama_baru = input("Masukkan nama baru (kosongkan jika tidak ingin mengubah): ")
    no_telp_baru = input("Masukkan no. telp baru (kosongkan jika tidak ingin mengubah): ")
    alamat_baru = input("Masukkan alamat baru (kosongkan jika tidak ingin mengubah): ")

    # Mengambil ID alamat lama
    cursor.execute("SELECT alamat_id_alamat FROM admin WHERE id_admin = %s", (admin_id,))
    alamat_id = cursor.fetchone()[0]

    try:
        if nama_baru:
            cursor.execute("UPDATE admin SET nama_admin = %s WHERE id_admin = %s", (nama_baru, admin_id))
        
        if no_telp_baru:
            cursor.execute("UPDATE admin SET no_telp_admin = %s WHERE id_admin = %s", (no_telp_baru, admin_id))

        if alamat_baru:
            cursor.execute("UPDATE alamat SET alamat = %s WHERE id_alamat = %s", (alamat_baru, alamat_id))
        
        conn.commit()
        print("Profil berhasil diperbarui.")
    except Exception as e:
        conn.rollback()
        print("Terjadi kesalahan saat memperbarui profil:", e)
    finally:
        time.sleep(1.2)
        os.system('cls')


# Fungsi untuk membuat pesanan dan data barang keluar
def buat_pesanan(admin_id):
    confirm = input("Ingin melanjutkan proses pemesanan dan edit? (y/n): ")
    if confirm.lower() != 'y':
        os.system('cls')
        return

    print("Buat Pesanan Barang\n")
    print("----------------------------")
    nama_barang = input("Masukkan nama barang: ")
    satuan = input("Masukkan satuan: ")
    jumlah_barang_masuk = int(input("Masukkan jumlah barang masuk: "))
    cursor.execute("SELECT id_supplier, nama_supplier FROM supplier")
    suppliers = cursor.fetchall()
    print("----------------------------")
    print("Pilih supplier:")
    for supplier in suppliers:
        print(f"{supplier[0]}. {supplier[1]}")
    print("----------------------------")
    supplier_id = int(input("Masukkan ID supplier: "))
    print("----------------------------")
    print("\nBarang yang sudah keluar atau terpakai")
    jumlah_barang_keluar = int(input("Masukkan jumlah barang keluar: "))
    print("----------------------------")
    tanggal = input("Masukkan tanggal pemesanan (YYYY-MM-DD): ")
    # Memasukkan data ke tabel barang jika barang baru
    cursor.execute("SELECT id_barang FROM barang WHERE nama_barang = %s AND satuan = %s", (nama_barang, satuan))
    barang = cursor.fetchone()
    if not barang:
        cursor.execute("INSERT INTO barang (nama_barang, satuan) VALUES (%s, %s) RETURNING id_barang", (nama_barang, satuan))
        barang_id = cursor.fetchone()[0]
    else:
        barang_id = barang[0]

    # Memeriksa apakah tanggal sudah ada
    cursor.execute("SELECT id_tanggal FROM tanggal WHERE tanggal = %s", (tanggal,))
    tanggal_result = cursor.fetchone()
    if tanggal_result:
        tanggal_id = tanggal_result[0]
    else:
        cursor.execute("INSERT INTO tanggal (tanggal) VALUES (%s) RETURNING id_tanggal", (tanggal,))
        tanggal_id = cursor.fetchone()[0]
    
    cursor.execute("INSERT INTO barang_masuk (jumlah_barang_masuk, barang_id_barang, tanggal_id_tanggal, supplier_id_supplier) VALUES (%s, %s, %s, %s) RETURNING id_barang_masuk",
                    (jumlah_barang_masuk, barang_id, tanggal_id, supplier_id))
    barang_masuk_id = cursor.fetchone()[0]

    cursor.execute("INSERT INTO barang_keluar (jumlah_barang_keluar, barang_id_barang, tanggal_id_tanggal) VALUES (%s, %s, %s) RETURNING id_barang_keluar",
                    (jumlah_barang_keluar, barang_id, tanggal_id))
    barang_keluar_id = cursor.fetchone()[0]

    # Memasukkan data ke tabel pencatatan
    cursor.execute("INSERT INTO pencatatan (barang_masuk_id_barang_masuk, barang_keluar_id_barang_keluar, admin_id_admin) VALUES (%s, %s, %s) RETURNING id_pencatatan", 
                    (barang_masuk_id, barang_keluar_id, admin_id))
    pencatatan_id = cursor.fetchone()[0]

    # Mendapatkan stok akhir sebelumnya untuk barang yang sama
    cursor.execute("""
        SELECT o.stok_akhir
        FROM opname_barang o
        JOIN pencatatan p ON o.pencatatan_id_pencatatan = p.id_pencatatan
        JOIN barang_masuk bm ON p.barang_masuk_id_barang_masuk = bm.id_barang_masuk
        WHERE bm.barang_id_barang = %s
        ORDER BY o.id_opname DESC LIMIT 1
    """, (barang_id,))
    stok_akhir_sebelumnya = cursor.fetchone()
    
    if stok_akhir_sebelumnya:
        stok_awal = stok_akhir_sebelumnya[0]
    else:
        stok_awal = 0
    
    stok_akhir = stok_awal + jumlah_barang_masuk - jumlah_barang_keluar

    cursor.execute("INSERT INTO opname_barang (stok_awal, stok_akhir, pencatatan_id_pencatatan) VALUES (%s, %s, %s)", 
                    (stok_awal, stok_akhir, pencatatan_id))
    
    conn.commit()
    os.system('cls')
    print("Pesanan berhasil dibuat!\n")
    time.sleep(1.2)
    os.system('cls')


# Fungsi untuk menampilkan daftar pesanan
def daftar_pesanan():
    cursor.execute("""
        SELECT p.id_pencatatan, b.nama_barang, b.satuan, bm.jumlah_barang_masuk, s.nama_supplier, s.no_telp_supplier, a.alamat, p.admin_id_admin
        FROM barang_masuk bm
        JOIN barang b ON bm.barang_id_barang = b.id_barang
        JOIN supplier s ON bm.supplier_id_supplier = s.id_supplier
        JOIN alamat a ON s.alamat_id_alamat = a.id_alamat
        JOIN pencatatan p ON bm.id_barang_masuk = p.barang_masuk_id_barang_masuk
    """)
    pesanan = cursor.fetchall()
    
    if not pesanan:
        print("Data belum ada.")
    else:
        df = pd.DataFrame(pesanan, columns=['ID Pencatatan', 'Nama Barang', 'Satuan', 'Jumlah', 'Supplier', 'No. Telp', 'Alamat', 'ID Admin'])
        print("Daftar Pesanan:")
        print(df.to_string(index=False))
    print()
    input("Tekan Enter untuk kembali ke Dashboard...")
    os.system('cls')

# Fungsi untuk melakukan opname
def opname():
    cursor.execute("""
        SELECT o.id_opname, b.id_barang, b.nama_barang, b.satuan, o.stok_awal, bm.jumlah_barang_masuk, bk.jumlah_barang_keluar, o.stok_akhir, t.tanggal
        FROM opname_barang o
        JOIN pencatatan p ON o.pencatatan_id_pencatatan = p.id_pencatatan
        JOIN barang_masuk bm ON p.barang_masuk_id_barang_masuk = bm.id_barang_masuk
        JOIN barang_keluar bk ON p.barang_keluar_id_barang_keluar = bk.id_barang_keluar
        JOIN barang b ON bm.barang_id_barang = b.id_barang
        JOIN tanggal t ON bm.tanggal_id_tanggal = t.id_tanggal
        ORDER BY b.nama_barang, t.tanggal, o.id_opname
    """)
    opname_data = cursor.fetchall()
    
    if not opname_data:
        print("Data belum ada.")
        time.sleep(1)
    else:
        # Menggunakan pandas untuk membuat tabel
        df = pd.DataFrame(opname_data, columns=['ID Opname', 'ID Barang', 'Nama Barang', 'Satuan', 'Stok Awal', 'Barang Masuk', 'Barang Keluar', 'Stok Akhir', 'Tanggal'])

        # Menampilkan tabel untuk setiap nama barang
        for nama_barang in df['Nama Barang'].unique():
            df_barang = df[df['Nama Barang'] == nama_barang]
            print(f"\nData Opname untuk {nama_barang}:")
            print(df_barang.to_string(index=False))

        while True:
            choice = input("Apakah ada baris yang ingin dihapus? (y/n): ")
            if choice.lower() == 'n':
                break
            elif choice.lower() == 'y':
                opname_id = input("Masukkan ID Opname yang ingin dihapus: ")
                hapus_data_opname(opname_id)
                os.system('cls')
                opname()
                break
            else:
                print("Pilihan tidak valid!")
                time.sleep(1.2)
                os.system('cls')

# Fungsi untuk mengatur ulang sequence ID opname_barang
def reset_opname_sequence():
    cursor.execute("SELECT setval('opname_barang_id_opname_seq', COALESCE((SELECT MAX(id_opname) FROM opname_barang) + 1, 1), false)")
    conn.commit()

# Fungsi untuk menghapus data opname dan data terkait
def hapus_data_opname(opname_id):
    try:
        # Mulai transaksi
        conn.autocommit = False
        with conn.cursor() as cursor:
            # Hapus data terkait dari tabel opname_barang
            cursor.execute("DELETE FROM opname_barang WHERE id_opname = %s RETURNING pencatatan_id_pencatatan", (opname_id,))
            pencatatan_id = cursor.fetchone()[0]
            
            # Hapus data terkait dari tabel pencatatan
            cursor.execute("DELETE FROM pencatatan WHERE id_pencatatan = %s RETURNING barang_masuk_id_barang_masuk, barang_keluar_id_barang_keluar", (pencatatan_id,))
            barang_masuk_id, barang_keluar_id = cursor.fetchone()

            # Hapus data terkait dari tabel barang_masuk
            cursor.execute("DELETE FROM barang_masuk WHERE id_barang_masuk = %s RETURNING barang_id_barang, tanggal_id_tanggal", (barang_masuk_id,))
            barang_id, tanggal_id_masuk = cursor.fetchone()

            # Hapus data terkait dari tabel barang_keluar
            cursor.execute("DELETE FROM barang_keluar WHERE id_barang_keluar = %s RETURNING tanggal_id_tanggal", (barang_keluar_id,))
            tanggal_id_keluar = cursor.fetchone()[0]

            # Hapus data terkait dari tabel tanggal jika tidak ada referensi lain
            cursor.execute("SELECT COUNT(*) FROM barang_masuk WHERE tanggal_id_tanggal = %s", (tanggal_id_masuk,))
            if cursor.fetchone()[0] == 0:
                cursor.execute("DELETE FROM tanggal WHERE id_tanggal = %s", (tanggal_id_masuk,))

            cursor.execute("SELECT COUNT(*) FROM barang_keluar WHERE tanggal_id_tanggal = %s", (tanggal_id_keluar,))
            if cursor.fetchone()[0] == 0:
                cursor.execute("DELETE FROM tanggal WHERE id_tanggal = %s", (tanggal_id_keluar,))

            # Hapus data terkait dari tabel barang jika tidak ada referensi lain
            cursor.execute("SELECT COUNT(*) FROM pencatatan p JOIN barang_masuk bm ON p.barang_masuk_id_barang_masuk = bm.id_barang_masuk WHERE bm.barang_id_barang = %s", (barang_id,))
            count_barang_masuk = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM pencatatan p JOIN barang_keluar bk ON p.barang_keluar_id_barang_keluar = bk.id_barang_keluar WHERE bk.barang_id_barang = %s", (barang_id,))
            count_barang_keluar = cursor.fetchone()[0]

            if count_barang_masuk == 0 and count_barang_keluar == 0:
                cursor.execute("DELETE FROM barang WHERE id_barang = %s", (barang_id,))

        conn.commit()
        print("Data opname yang terkait berhasil dihapus.")
    except Exception as e:
        conn.rollback()
        print("Proses pencarian data yang akan diambil", e)
        time.sleep(1.5)
    finally:
        reset_opname_sequence()  # Atur ulang sequence ID opname_barang setelah penghapusan
        conn.autocommit = True
        print("ID Opname telah terhapus")
        time.sleep(1.5)

# Main loop aplikasi
def main():
    admin_id = login()
    if admin_id:
        while True:
            dashboard()
            choice = input("Masukkan pilihan Anda: ")
            if choice == '0':
                print("Logout...")
                time.sleep(1)
                break
            elif choice == '1':
                os.system('cls')  
                tampilkan_profil(admin_id)
            elif choice == '2':
                os.system('cls')  
                while True:
                    print(
                        """
=================================
|      \033[32mMenu Pemesanan dan Edit\033[0m   |
=================================
|                               |
|  1. Buat Pesanan              |
|  2. Daftar Pesanan            |
|                               |
|  0. Kembali ke Dashboard      |
|_______________________________|
                        """
                    )
                    sub_choice = input("Masukkan pilihan Anda: ")
                    if sub_choice == '0':
                        break
                    elif sub_choice == '1':
                        os.system('cls')  
                        buat_pesanan(admin_id)
                    elif sub_choice == '2':
                        os.system('cls')  
                        daftar_pesanan()
                    else:
                        print("Pilihan tidak valid!")
                        time.sleep(1.2)
                        os.system('cls')
            elif choice == '3':
                os.system('cls')  
                opname()
            elif choice == '4':
                os.system('cls')
                update_profil(admin_id)
            elif choice == '5':  # Tambahkan logika untuk pilihan ubah username dan password
                os.system('cls')
                ubah_username_password(admin_id)
            else:
                print("Pilihan tidak valid!")
                time.sleep(1.2)
                os.system('cls')


main()

# Menutup koneksi ke database
cursor.close()
conn.close()
