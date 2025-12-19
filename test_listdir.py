import os

test_dir = r"files\bpkh_form\bpkh_wilayah_ii"

print("Testing os.listdir():")
print("=" * 80)

all_items = os.listdir(test_dir)
print(f"Total items: {len(all_items)}\n")

# Filter hanya file
files_only = []
for item in all_items:
    full_path = os.path.join(test_dir, item)
    if os.path.isfile(full_path):
        files_only.append(item)
        
print(f"Total files: {len(files_only)}\n")

# Cari yang mengandung 1_3
print("Files dengan '1_3' di nama:")
for f in files_only:
    if "1_3" in f:
        print(f"  FOUND: {f}")
        full_path = os.path.join(test_dir, f)
        print(f"  Full path: {full_path}")
        print(f"  Is file: {os.path.isfile(full_path)}")
        print(f"  Extension: {os.path.splitext(f)[1]}")
        print()

# Cari yang TIDAK mengandung 1_3 tapi ada di listdir
print("\nSemua files:")
for i, f in enumerate(sorted(files_only), 1):
    ext = os.path.splitext(f)[1].lower()
    print(f"{i:2}. {f[:80]}... (ext: {ext})")
