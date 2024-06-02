import psycopg2
import getpass

# Koneksi ke database PostgreSQL
conn = psycopg2.connect(database='BasdaHK', user='postgres', password='123123', host='localhost', port='5432')
cursor = conn.cursor()

def login():
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
    return None

def tampilkan_profil(admin_id):
    cursor.execute("""
        SELECT a.id_admin, a.nama_admin, a.no_telp_admin, al.alamat
        FROM admin a
        JOIN alamat al ON a.alamat_id_alamat = al.id_alamat
        WHERE a.id_admin = %s
    """, (admin_id,))
    profil = cursor.fetchone()
    if profil:
        print("Profil Admin:")
        print(f"ID Admin: {profil[0]}")
        print(f"Nama: {profil[1]}")
        print(f"No. Telp: {profil[2]}")
        print(f"Alamat: {profil[3]}\n")

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

    # Memasukkan data ke tabel opname_barang
    cursor.execute("""
        SELECT stok_akhir FROM opname_barang WHERE pencatatan_id_pencatatan = %s
        ORDER BY id_opname DESC LIMIT 1
    """, (pencatatan_id,))
    

    stok_akhir =  jumlah_barang_masuk - jumlah_barang_keluar

    cursor.execute("INSERT INTO opname_barang ( stok_akhir, pencatatan_id_pencatatan) VALUES ( %s, %s)", 
                   ( stok_akhir, pencatatan_id))
    
    conn.commit()
    print("Pesanan berhasil dibuat!\n")

def daftar_pesanan():
    cursor.execute("""
        SELECT b.nama_barang, b.satuan, bm.jumlah_barang_masuk, s.nama_supplier, s.no_telp_supplier, a.alamat
        FROM barang_masuk bm
        JOIN barang b ON bm.barang_id_barang = b.id_barang
        JOIN supplier s ON bm.supplier_id_supplier = s.id_supplier
        JOIN alamat a ON s.alamat_id_alamat = a.id_alamat
    """)
    pesanan = cursor.fetchall()
    print("Daftar Pesanan:")
    for p in pesanan:
        print(f"Nama Barang: {p[0]}, Satuan: {p[1]}, Jumlah: {p[2]}, Supplier: {p[3]}, No. Telp: {p[4]}, Alamat: {p[5]}")
    print()

def opname():
    cursor.execute("""
        SELECT o.id_opname, a.id_admin, b.nama_barang, b.satuan, bm.jumlah_barang_masuk, bk.jumlah_barang_keluar, o.stok_akhir, t.tanggal
        FROM opname_barang o
        JOIN pencatatan p ON o.pencatatan_id_pencatatan = p.id_pencatatan
        JOIN admin a ON p.admin_id_admin = a.id_admin
        JOIN barang b ON p.barang_masuk_id_barang_masuk = b.id_barang
        JOIN barang_masuk bm ON p.barang_masuk_id_barang_masuk = bm.id_barang_masuk
        JOIN barang_keluar bk ON p.barang_keluar_id_barang_keluar = bk.id_barang_keluar
        JOIN tanggal t ON bm.tanggal_id_tanggal = t.id_tanggal
    """)
    opname_data = cursor.fetchall()
    print("Data Opname:")
    for data in opname_data:
        print(f"ID Opname: {data[0]}, ID Admin: {data[1]}, Nama Barang: {data[2]}, Satuan: {data[3]},  Barang Masuk: {data[4]}, Barang Keluar: {data[5]}, Stok Akhir: {data[6]}, Tanggal: {data[7]}")
    print()

def main():
    admin_id = login()
    if admin_id:
        while True:
            print("Menu:")
            print("1. Profil Admin")
            print("2. Edit Stok")
            print("3. Opname")
            print("4. Keluar")
            pilihan = int(input("Masukkan pilihan: "))
            
            if pilihan == 1:
                tampilkan_profil(admin_id)
            elif pilihan == 2:
                print("1. Buat Pesanan dan Data Barang Keluar")
                print("2. Daftar Pesanan")
                sub_pilihan = int(input("Masukkan pilihan: "))
                if sub_pilihan == 1:
                    buat_pesanan(admin_id)
                elif sub_pilihan == 2:
                    daftar_pesanan()
            elif pilihan == 3:
                opname()
            elif pilihan == 4:
                break
            else:
                print("Pilihan tidak valid!")

if __name__ == "__main__":
    main()

# Menutup koneksi ke database
cursor.close()
conn.close()
