import psycopg2
import getpass
import pandas as pd
import os
import time

# Fungsi untuk menampilkan menu login
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

# Fungsi untuk menampilkan dashboard
def dashboard():
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear layar pada Windows, gunakan 'clear' untuk Linux
    print(
        f"""
===============================
|         \033[32mHalo Min :*\033[0m         |
===============================
|                             |
|  1. Profil Pegawai          |
|  2. Memesan dan Edit stok   |
|  3. Opname                  |
|                             |
|                             |
|                             |
|  0. Logout                  |
|_____________________________|
    """
    )

# Koneksi ke database PostgreSQL
conn = psycopg2.connect(database='BasdaHK8', user='postgres', password='123123', host='localhost', port='5432')
cursor = conn.cursor()

# Fungsi login
def login():
    while True:
        menu_login()
        choice = input("Tekan enter untuk melanjutkan... ")
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
        print("Login gagal! Periksa username dan password Anda.")

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
        

# Fungsi untuk membuat pesanan dan data barang keluar
def buat_pesanan(admin_id):
    nama_barang = input("Masukkan nama barang: ")
    satuan = input("Masukkan satuan: ")
    jumlah_barang_masuk = int(input("Masukkan jumlah barang masuk: "))
    jumlah_barang_keluar = int(input("Masukkan jumlah barang keluar: "))
    
    cursor.execute("SELECT id_supplier, nama_supplier FROM supplier")
    suppliers = cursor.fetchall()
    print("Pilih supplier:")
    for supplier in suppliers:
        print(f"{supplier[0]}. {supplier[1]}")
    supplier_id = int(input("Masukkan ID supplier: "))
    
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
    print("Pesanan berhasil dibuat!\n")
    time.sleep(1)


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
                # Menghapus baris data opname dari database
                cursor.execute("DELETE FROM opname_barang WHERE id_opname = %s", (opname_id,))
                hapus_data_opname(opname_id)
                conn.commit()
                print("Baris data opname telah dihapus.")
                break
            else:
                print("Pilihan tidak valid!")

def hapus_data_opname(opname_id):
    try:
        with conn:
            with conn.cursor() as cursor:
                # Hapus data terkait dari tabel pencatatan
                cursor.execute("DELETE FROM pencatatan WHERE id_pencatatan IN (SELECT id_pencatatan FROM opname_barang WHERE id_opname = %s)", (opname_id,))
                # Hapus data terkait dari tabel opname_barang
                cursor.execute("DELETE FROM opname_barang WHERE id_opname = %s", (opname_id,))
                # Hapus data terkait dari tabel barang_masuk
                cursor.execute("DELETE FROM barang_masuk WHERE id_barang_masuk IN (SELECT barang_masuk_id_barang_masuk FROM pencatatan WHERE id_pencatatan IN (SELECT id_pencatatan FROM opname_barang WHERE id_opname = %s))", (opname_id,))
                # Hapus data terkait dari tabel barang_keluar
                cursor.execute("DELETE FROM barang_keluar WHERE id_barang_keluar IN (SELECT barang_keluar_id_barang_keluar FROM pencatatan WHERE id_pencatatan IN (SELECT id_pencatatan FROM opname_barang WHERE id_opname = %s))", (opname_id,))
                # Hapus data terkait dari tabel tanggal
                cursor.execute("DELETE FROM tanggal WHERE id_tanggal IN (SELECT tanggal_id_tanggal FROM barang_masuk WHERE id_barang_masuk IN (SELECT barang_masuk_id_barang_masuk FROM pencatatan WHERE id_pencatatan IN (SELECT id_pencatatan FROM opname_barang WHERE id_opname = %s)))", (opname_id,))
                print("Data opname dan terkait berhasil dihapus.")
    except Exception as e:
        print("Terjadi kesalahan saat menghapus data opname:", e)
    else:
        print("ID Opname telah terhapus")

# Fungsi utama
def main():
    admin_id = login()
    if admin_id:
        while True:
            dashboard()
            pilihan = input("Masukkan pilihan: ")
            if pilihan == '0':
                break
            elif pilihan == '1':
                dashboard()
                tampilkan_profil(admin_id)
            elif pilihan == '2':
                print("1. Buat Pesanan dan Data Barang Keluar")
                print("2. Daftar Pesanan")
                sub_pilihan = input("Masukkan pilihan: ")
                if sub_pilihan == '1':
                    buat_pesanan(admin_id)
                elif sub_pilihan == '2':
                    daftar_pesanan()
            elif pilihan == '3':
                opname()
            else:
                print("Pilihan tidak valid!")

# Menjalankan program utama
if __name__ == "__main__":
    main()

# Menutup koneksi ke database
cursor.close()
conn.close()
# perbaiki bagaimana ketika menghapus baris berdasarkan id opname di fitur opname
# maka di database juga akan terhapus data datnaya yaitu (id barang, satuan, jumlah barang masuk, jumlah barnang keluar, stok awal, stok akhir, supplier)