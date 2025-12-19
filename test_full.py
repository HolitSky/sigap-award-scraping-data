import os
import re

# Mapping untuk Produsen
QUESTION_MAPPING_PRODUSEN = {
    "1.1": "PEMBENTUKAN KELOMPOK KERJA",
    "1.3": "STRATEGI GEOSPASIAL",
    "2.1": "BERBAGI DATA",
    "2.2": "HAK KEKAYAAN INTELEKTUAL",
    "3.1": "TATA KELOLA KEUANGAN",
    "3.2": "SUMBER PENDANAAN",
    "4.1": "INFRASTRUKTUR GEODETIK",
    "4.2": "INVENTARIS DATA",
    "4.3": "ANALISIS KESENJANGAN DATA",
    "4.5": "Kualitas Data",
    "4.6": "METADATA",
    "4.7": "PENYIMPANAN DATA",
    "4.8": "SIKLUS ALIRAN DATA",
    "4.9": "INTEROPERABILITAS DATA",
    "5.1": "STRATEGI INOVASI",
    "5.2": "INFRASTRUKTUR ICT",
    "5.3": "MODERNISASI ASET DATA",
    "5.5": "SISTEM TERPADU",
    "6.1": "TATA KELOLA STANDAR",
    "6.2": "STRATEGI/RENCANA STANDAR",
    "6.3": "IMPLEMENTASI",
    "7.1": "KESADARAN KEMITRAAN",
    "7.2": "KOLABORASI LINTAS SEKTOR",
    "8.1": "KELOMPOK KERJA",
    "8.2": "PENILAIAN DAN ANALISIS",
    "8.4": "PROGRAM PENDIDIKAN TINGGI",
    "8.5": "PENDEKATAN PENGEMBANGAN",
    "8.6": "JF SURTA",
    "8.7": "JF PRAKOM"
}

def extract_question_number(filename):
    match = re.search(r'no_(\d+)_(\d+)', filename)
    if match:
        return f"{match.group(1)}.{match.group(2)}"
    return None

def sort_question_numbers(question_list):
    def sort_key(q):
        parts = q.split('.')
        return (int(parts[0]), int(parts[1]))
    return sorted(question_list, key=sort_key)

# Test dengan folder produsen
test_dir = r"files\produsen_form\produsen_perencanaan_dan_evaluasi_pengelolaan_daerah_aliran_sungai"

print("Testing dengan folder produsen_perencanaan_dan_evaluasi_pengelolaan_daerah_aliran_sungai")
print("=" * 80)

# Ambil file
files = []
for file in os.listdir(test_dir):
    if file.endswith('.pdf'):
        files.append(file)

print(f"\nTotal files: {len(files)}")
print()

# Extract question numbers
question_files = {}
for file in files:
    q_num = extract_question_number(file)
    if q_num:
        if q_num not in question_files:
            question_files[q_num] = []
        question_files[q_num].append(file)

print(f"Question numbers dari files: {len(question_files)}")
print(f"Questions: {sorted(question_files.keys())}")
print()

# Expected questions
expected = list(QUESTION_MAPPING_PRODUSEN.keys())
print(f"Expected questions dari mapping: {len(expected)}")
print(f"Questions: {expected}")
print()

# Gabungkan
all_questions = set(expected) | set(question_files.keys())
all_questions = sort_question_numbers(list(all_questions))

print(f"Total questions yang akan diproses: {len(all_questions)}")
print(f"Questions: {all_questions}")
print()

# Cek mana yang ada file, mana yang tidak
print("Detail per question:")
print("-" * 80)
for q in all_questions:
    has_file = q in question_files
    in_mapping = q in QUESTION_MAPPING_PRODUSEN
    status = "✓ ADA FILE" if has_file else "⚠️  BELUM ADA"
    mapping_status = "✓ DI MAPPING" if in_mapping else "⚠️  TIDAK DI MAPPING"
    print(f"{q:6} | {status:15} | {mapping_status:20} | {QUESTION_MAPPING_PRODUSEN.get(q, 'N/A')[:40]}")
