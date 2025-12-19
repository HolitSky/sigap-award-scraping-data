import os
import re

def get_sorted_files(directory):
    """
    Ambil semua file PDF dan gambar, diurutkan berdasarkan nama
    """
    supported_extensions = ['.pdf', '.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff']
    files = []
    
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            ext = os.path.splitext(file)[1].lower()
            if ext in supported_extensions:
                files.append(file_path)
    
    # Sort berdasarkan nama file
    files.sort()
    return files

def extract_question_number(filename):
    match = re.search(r'no_(\d+)_(\d+)', filename)
    if match:
        return f"{match.group(1)}.{match.group(2)}"
    return None

# Test dengan folder bpkh_wilayah_ii
test_dir = r"files\bpkh_form\bpkh_wilayah_ii"

print("Testing dengan folder bpkh_wilayah_ii")
print("=" * 80)

# Ambil file
files = get_sorted_files(test_dir)

print(f"\nTotal files ditemukan: {len(files)}")
print()

# Extract question numbers
question_files = {}
for file_path in files:
    filename = os.path.basename(file_path)
    q_num = extract_question_number(filename)
    if q_num:
        if q_num not in question_files:
            question_files[q_num] = []
        question_files[q_num].append(filename)
    else:
        print(f"⚠️  Tidak bisa extract nomor dari: {filename}")

print(f"\nQuestion numbers dari files: {len(question_files)}")
print()

# Detail per question
for q_num in sorted(question_files.keys()):
    print(f"{q_num}: {len(question_files[q_num])} file(s)")
    for f in question_files[q_num]:
        print(f"  - {f[:80]}")
    print()

# Cek apakah ada 1.3
if "1.3" in question_files:
    print("✅ File 1.3 DITEMUKAN!")
else:
    print("❌ File 1.3 TIDAK DITEMUKAN!")
    print("\nCek manual apakah ada file dengan no_1_3:")
    all_files = os.listdir(test_dir)
    for f in all_files:
        if "no_1_3" in f:
            print(f"  FOUND: {f}")
