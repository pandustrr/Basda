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
INSERT INTO admin (nama_admin, no_telp_admin, username, password, alamat_admin,)
VALUES  ('Pandu Satria', '081230487469', 'Pandu', '3008','Jl. Semeru No XII, Sumbersari'),
        ('Rahmad Afan', '085156649664', 'Afan', '3023','Jl. Sumatra No. 32, Jember'),
        ('Muhammad Rizal Aufar R.', '085854830482', 'Rizal', '3046','Jl. Mangga No. 15 Blok D, Kalibaru'),
        ('Diki Ferdianto', '085733478061', 'Diki', '3056','Jl. Permata Indah No. 17, Blitar'),
        ('Yanto Admin Santoso', '081231235656', 'admin', '123','Jl. Sudirman Blok 50, Bondowoso');

-- Mengisi tabel supplier
INSERT INTO supplier (nama_supplier, no_telp_supplier, alamat_id_alamat)
VALUES  ('PT. Sumber Rezeki', '081234567890', 'Perumahan Berlian Blok FF No 1, Surabaya'),
        ('CV. Berkah Abadi', '085123456789', 'Jl. Rezeki No. 22, Jember'),
        ('UD. Sinar Jaya', '082123456780', 'Jl. Mangga 17, Banyuwangi'),
        ('PT. Maju Jaya', '081223456789', 'Jl. Bintang No. 99, Situbondo'),
        ('CV. Bintang Terang', '085233456789', 'Jl. Semeru No XII, Sumbersari');

