-- Mengisi tabel login
INSERT INTO login (username, password)
VALUES  ('Pandu', '3008'),
        ('Afan', '3023'),
        ('Rizal', '3046'),
        ('Diki', '3056'),
        ('admin', '123');

-- Mengisi tabel alamat
INSERT INTO alamat (alamat)
VALUES  ('Jl. Semeru No XII, Sumbersari'),
        ('Jl. Sumatra No. 32, Jember'),
        ('Jl. Mangga No. 15 Blok D, Kalibaru'),
        ('Perumahan Berlian Blok FF No 1, Surabaya'),
        ('Jl. Permata Indah No. 17, Blitar'),
        ('Jl. Rezeki No. 22, Jember'),
        ('Jl. Sudirman Blok 50, Bondowoso'),
        ('Jl. Durian Runtuh No 12 Blok 1, Surabaya'),
        ('Jl. Mangga 17, Banyuwangi'),
        ('Jl. Bintang No. 99, Situbondo');

-- Mengisi tabel admin
INSERT INTO admin (nama_admin, no_telp_admin, login_id_login, alamat_id_alamat)
VALUES  ('Pandu Satria', '081230487469', 1, 1),
        ('Rahmad Afan', '085156649664', 2, 2),
        ('Muhammad Rizal Aufar R.', '085854830482', 3, 3),
        ('Diki Ferdianto', '085733478061', 4, 4),
        ('Yanto Admin Santoso', '081231235656', 5, 5);

-- Mengisi tabel supplier
INSERT INTO supplier (nama_supplier, no_telp_supplier, alamat_id_alamat)
VALUES  ('PT. Sumber Rezeki', '081234567890', 6),
        ('CV. Berkah Abadi', '085123456789', 7),
        ('UD. Sinar Jaya', '082123456780', 8),
        ('PT. Maju Jaya', '081223456789', 9),
        ('CV. Bintang Terang', '085233456789', 10);

