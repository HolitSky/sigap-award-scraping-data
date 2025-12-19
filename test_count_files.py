import os

def count_files_in_subdirectories(base_dir, category_name):
    """
    Hitung total file di semua subdirektori dengan long path support
    """
    total_files = 0
    folder_details = []
    
    supported_extensions = ['.pdf', '.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff']
    
    # Cari semua subdirektori
    for root, dirs, files in os.walk(base_dir):
        # Skip direktori base itu sendiri
        if root == base_dir:
            continue
        
        # Hitung file di direktori ini dengan long path support
        file_count = 0
        
        # Konversi ke absolute path untuk long path support
        abs_root = os.path.abspath(root)
        if os.name == 'nt' and not abs_root.startswith('\\\\?\\'):
            long_root = '\\\\?\\' + abs_root
        else:
            long_root = abs_root
        
        try:
            for file in os.listdir(long_root):
                file_path = os.path.join(long_root, file)
                try:
                    if os.path.isfile(file_path):
                        ext = os.path.splitext(file)[1].lower()
                        if ext in supported_extensions:
                            file_count += 1
                except (OSError, IOError):
                    # Skip file yang tidak bisa diakses
                    pass
        except Exception as e:
            print(f"   ⚠️  Error accessing {os.path.basename(root)}: {str(e)}")
        
        if file_count > 0:
            folder_name = os.path.basename(root)
            folder_details.append((folder_name, file_count))
            total_files += file_count
    
    return total_files, folder_details

# Path base
base_path = r"D:\01 - All Project 2025\01 - IPSDH\06 - SIGAP AWARD - FORM\00 - ALL BUKTI DUKUNG SIGAP AWARD 2025\merging-pdf-sigap-award"

bpkh_dir = os.path.join(base_path, "files", "bpkh_form")
produsen_dir = os.path.join(base_path, "files", "produsen_form")

print("=" * 80)
print("📊 STATISTIK FILE BUKTI DUKUNG")
print("=" * 80)

# Hitung BPKH
print("\n🏢 BPKH FORM:")
print("-" * 80)
bpkh_total, bpkh_details = count_files_in_subdirectories(bpkh_dir, "BPKH")

for folder_name, count in sorted(bpkh_details):
    print(f"   {folder_name:50} : {count:3} files")

print(f"\n   {'TOTAL BPKH':50} : {bpkh_total:3} files")

# Hitung Produsen
print("\n\n🏭 PRODUSEN FORM:")
print("-" * 80)
produsen_total, produsen_details = count_files_in_subdirectories(produsen_dir, "Produsen")

for folder_name, count in sorted(produsen_details):
    print(f"   {folder_name:50} : {count:3} files")

print(f"\n   {'TOTAL PRODUSEN':50} : {produsen_total:3} files")

# Grand Total
print("\n" + "=" * 80)
print(f"📁 GRAND TOTAL SEMUA FILE: {bpkh_total + produsen_total} files")
print(f"   - BPKH: {bpkh_total} files dari {len(bpkh_details)} folder")
print(f"   - Produsen: {produsen_total} files dari {len(produsen_details)} folder")
print("=" * 80)
