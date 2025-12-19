import re

# Test regex extraction
filenames = [
    "no_1_1_SK_Terbaru_1.1.-SK-4-TIM-KERJA-PEPDAS-2025.pdf",
    "no_1_3_bukti_dokumen_Rencana_StrategiRoadmap_1.3.-DRAFT-RENSTRA-PEPDAS-2025-2029.pdf",
    "no_2_1_bukti_dokumen_2.1.-SE-DIRJEN-PDASRH-RAWAN-LIMPASAN-LAHAN-KRITIS-DAN-RAWAN-EROSI.pdf",
    "no_4_1_dokumentasi_4.1.-PROYEKSI-DAN-KOORDINAT.pdf",
    "no_6_3_Bukti_dukung_standar_teknologi_6.3.-INTEGRASI-INTEROPERABILITAS-SISTEM.pdf",
    "no_8_7_bukti_dukung_berupa_SKKarpegSurat_Usulan_JF_Surta_8.7.-JABFUNG-PRAKOM.pdf"
]

def extract_question_number(filename):
    """
    Ekstrak nomor pertanyaan dari nama file (contoh: no_1_1 -> 1.1)
    """
    # Pattern: no_X_Y
    match = re.search(r'no_(\d+)_(\d+)', filename)
    if match:
        return f"{match.group(1)}.{match.group(2)}"
    return None

print("Testing regex extraction:")
print("=" * 60)
for filename in filenames:
    result = extract_question_number(filename)
    print(f"File: {filename[:50]}...")
    print(f"Extracted: {result}")
    print()
