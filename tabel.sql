CREATE TABLE admin (
    id_admin SERIAL PRIMARY KEY,
    nama_admin VARCHAR(50) NOT NULL,
    no_telp_admin VARCHAR(15) NOT NULL,
    login_id_login INTEGER NOT NULL,
    alamat_id_alamat INTEGER NOT NULL
);

CREATE UNIQUE INDEX admin__idx ON admin (login_id_login);

CREATE TABLE alamat (
    id_alamat SERIAL PRIMARY KEY,
    alamat VARCHAR(256) NOT NULL
);

CREATE TABLE barang (
    id_barang SERIAL PRIMARY KEY,
    nama_barang VARCHAR(50) NOT NULL,
    satuan VARCHAR(50) NOT NULL
);

CREATE TABLE barang_keluar (
    id_barang_keluar SERIAL PRIMARY KEY,
    jumlah_barang_keluar INTEGER NOT NULL,
    barang_id_barang INTEGER NOT NULL,
    tanggal_id_tanggal INTEGER NOT NULL
);

CREATE TABLE barang_masuk (
    id_barang_masuk SERIAL PRIMARY KEY,
    jumlah_barang_masuk INTEGER NOT NULL,
    barang_id_barang INTEGER NOT NULL,
    tanggal_id_tanggal INTEGER NOT NULL,
    supplier_id_supplier INTEGER NOT NULL
);

CREATE TABLE login (
    id_login SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL
);

CREATE TABLE opname_barang (
    id_opname SERIAL PRIMARY KEY,
    stok_awal INTEGER NOT NULL,
    stok_akhir INTEGER NOT NULL,
    pencatatan_id_pencatatan INTEGER NOT NULL
);

CREATE TABLE pencatatan (
    id_pencatatan SERIAL PRIMARY KEY,
    barang_keluar_id_barang_keluar INTEGER NOT NULL,
    barang_masuk_id_barang_masuk INTEGER NOT NULL,
    admin_id_admin INTEGER NOT NULL
);

CREATE TABLE supplier (
    id_supplier SERIAL PRIMARY KEY,
    nama_supplier VARCHAR(50) NOT NULL,
    no_telp_supplier VARCHAR(15) NOT NULL,
    alamat_id_alamat INTEGER NOT NULL
);

CREATE TABLE tanggal (
    id_tanggal SERIAL PRIMARY KEY,
    tanggal DATE NOT NULL
);

ALTER TABLE admin
    ADD CONSTRAINT admin_alamat_fk FOREIGN KEY (alamat_id_alamat)
        REFERENCES alamat (id_alamat);

ALTER TABLE admin
    ADD CONSTRAINT admin_login_fk FOREIGN KEY (login_id_login)
        REFERENCES login (id_login);

ALTER TABLE barang_keluar
    ADD CONSTRAINT barang_keluar_barang_fk FOREIGN KEY (barang_id_barang)
        REFERENCES barang (id_barang);

ALTER TABLE barang_keluar
    ADD CONSTRAINT barang_keluar_tanggal_fk FOREIGN KEY (tanggal_id_tanggal)
        REFERENCES tanggal (id_tanggal);

ALTER TABLE barang_masuk
    ADD CONSTRAINT barang_masuk_barang_fk FOREIGN KEY (barang_id_barang)
        REFERENCES barang (id_barang);

ALTER TABLE barang_masuk
    ADD CONSTRAINT barang_masuk_supplier_fk FOREIGN KEY (supplier_id_supplier)
        REFERENCES supplier (id_supplier);

ALTER TABLE barang_masuk
    ADD CONSTRAINT barang_masuk_tanggal_fk FOREIGN KEY (tanggal_id_tanggal)
        REFERENCES tanggal (id_tanggal);

ALTER TABLE opname_barang
    ADD CONSTRAINT opname_barang_pencatatan_fk FOREIGN KEY (pencatatan_id_pencatatan)
        REFERENCES pencatatan (id_pencatatan);

ALTER TABLE pencatatan
    ADD CONSTRAINT pencatatan_admin_fk FOREIGN KEY (admin_id_admin)
        REFERENCES admin (id_admin);

ALTER TABLE pencatatan
    ADD CONSTRAINT pencatatan_barang_keluar_fk FOREIGN KEY (barang_keluar_id_barang_keluar)
        REFERENCES barang_keluar (id_barang_keluar);

ALTER TABLE pencatatan
    ADD CONSTRAINT pencatatan_barang_masuk_fk FOREIGN KEY (barang_masuk_id_barang_masuk)
        REFERENCES barang_masuk (id_barang_masuk);

ALTER TABLE supplier
    ADD CONSTRAINT supplier_alamat_fk FOREIGN KEY (alamat_id_alamat)
        REFERENCES alamat (id_alamat);
