import os

test_dir = r"files\bpkh_form\bpkh_wilayah_ii"

print("Detailed check:")
print("=" * 80)

all_items = os.listdir(test_dir)

files = []
non_files = []

for item in all_items:
    full_path = os.path.join(test_dir, item)
    is_file = os.path.isfile(full_path)
    is_dir = os.path.isdir(full_path)
    exists = os.path.exists(full_path)
    
    if is_file:
        files.append(item)
    else:
        non_files.append((item, is_dir, exists))

print(f"Files: {len(files)}")
print(f"Non-files: {len(non_files)}\n")

print("NON-FILES (yang tidak terdeteksi):")
print("-" * 80)
for item, is_dir, exists in non_files:
    print(f"Name: {item[:80]}")
    print(f"  Is dir: {is_dir}")
    print(f"  Exists: {exists}")
    full_path = os.path.join(test_dir, item)
    print(f"  Full path: {full_path}")
    
    # Try to get file stats
    try:
        stat = os.stat(full_path)
        print(f"  Size: {stat.st_size}")
    except Exception as e:
        print(f"  Error getting stats: {e}")
    print()
