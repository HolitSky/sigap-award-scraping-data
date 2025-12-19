import os

def get_sorted_files_new(directory):
    """
    Ambil semua file PDF dan gambar, diurutkan berdasarkan nama
    Mendukung long path (>260 karakter) di Windows
    """
    supported_extensions = ['.pdf', '.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff']
    files = []
    
    # Konversi ke absolute path untuk mendukung long path
    abs_directory = os.path.abspath(directory)
    
    # Gunakan long path prefix untuk Windows jika path panjang
    if os.name == 'nt' and not abs_directory.startswith('\\\\?\\'):
        abs_directory = '\\\\?\\' + abs_directory
    
    try:
        for file in os.listdir(abs_directory):
            file_path = os.path.join(abs_directory, file)
            try:
                if os.path.isfile(file_path):
                    ext = os.path.splitext(file)[1].lower()
                    if ext in supported_extensions:
                        # Simpan path tanpa prefix \\?\ untuk kompatibilitas
                        clean_path = file_path.replace('\\\\?\\', '')
                        files.append(clean_path)
            except (OSError, IOError) as e:
                # Skip file yang tidak bisa diakses
                print(f"   ⚠️  Warning: Tidak bisa mengakses file: {file[:50]}... ({str(e)})")
                continue
    except Exception as e:
        print(f"   ⚠️  Error listing directory: {str(e)}")
    
    # Sort berdasarkan nama file
    files.sort()
    return files

# Test dengan folder bpkh_wilayah_ii
test_dir = r"files\bpkh_form\bpkh_wilayah_ii"

print("Testing dengan long path support:")
print("=" * 80)

files = get_sorted_files_new(test_dir)

print(f"\nTotal files ditemukan: {len(files)}")
print()

# Cek apakah ada 1.3
found_1_3 = False
for f in files:
    if "no_1_3" in f:
        found_1_3 = True
        print(f"✅ File 1.3 DITEMUKAN: {os.path.basename(f)}")
        break

if not found_1_3:
    print("❌ File 1.3 TIDAK DITEMUKAN!")

print(f"\nSemua files:")
for i, f in enumerate(files, 1):
    basename = os.path.basename(f)
    print(f"{i:2}. {basename[:80]}")
