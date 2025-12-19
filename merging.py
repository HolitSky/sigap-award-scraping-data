import os
from pathlib import Path
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import simpleSplit
import io
import re

# Mapping nomor soal ke judul soal untuk BPKH
QUESTION_MAPPING_BPKH = {
    "1.1": "PEMBENTUKAN KELOMPOK KERJA : Apakah ada kelompok kerja pelaksana Jaringan Data dan Informasi Geospasial lingkup BPKH?",
    "1.2": "PERAN GEOSPASIAL KELEMBAGAAN : Apakah ada pembagian peran dan tanggung jawab yang jelas pada kelompok kerja pelaksana Jaringan Data dan Informasi Geospasial dilingkup BPKH?",
    "1.3": "STRATEGI GEOSPASIAL : Apakah ada Strategi (Rencana Startegi/Roadmap) yang mengidentifikasi visi, misi, tujuan, dan sasaran inisiatif pengelolaan informasi geospasial untuk menciptakan Satu Data Kehutanan Indonesia?",
    "1.4": "PEMANTAUAN DAN EVALUASI / INDIKATOR KEBERHASILAN : Apakah ada pelaporan dan evaluasi yang dikirimkan ke IPSDH secara rutin?",
    "2.1": "BERBAGI DATA : Apakah ada regulasi khusus ditingkat BPKH yang mengatur prosedural berbagi pakai data dan informasi geospasial kehutanan?",
    "2.2": "STRATEGI KEPATUHAN : Apakah ada Strategi Kepatuhan berupa Berita Acara Serah Terima (BAST)/Pakta Integritas yang mendefinisikan untuk mematuhi kebijakan, undang-undang, dan peraturan geospasial dan bagaimana kepatuhan akan dipantau?",
    "3.1": "TATA KELOLA KEUANGAN DAN AKUNTABILITAS : Apakah terdapat anggaran khusus untuk pengumpulan dan pelayanan Data dan Informasi Geospasial Kehutanan di BPKH?",
    "3.2": "SUMBER PENDANAAN : Apakah BPKH memiliki sumber pendanaan selain dari APBN untuk operasionalisasi pengumpulan dan pelayanan DIGT Kehutanan ?",
    "4.1": "BERBAGI DATA : Apakah ada SOP resmi yang berisi alur penyebarluasan data geospasial dari BPKH untuk pemohon",
    "4.2": "PENYIMPANAN DAN PENGAMBILAN DATA : Apakah BPKH memiliki media penyimpanan khusus untuk DIGT Kehutanan yang terpisah dari non DIGT Kehutanan?",
    "5.1": "STRATEGI INOVASI GEOSPASIAL : Apakah ada strategi inovasi yang mendorong optimalisasi pendayagunaan DIGT Kehutanan?",
    "5.2": "INFRASTRUKTUR ICT INTI : Apakah ada sarana-prasarana pendukung inovasi? Contoh: sarana fisik (ruang multimedia, ruang pertemuan, dll); prasarana teknologi (jaringan internet berkecepatan tinggi, sistem aplikasi, dll)",
    "5.3": "MODERNISASI ASET DATA: Apakah BPKH menggunakan perangkat lunak berlisensi atau tidak untuk perangkat lunak/aplikasi berbasis komersial ?",
    "5.4": "SISTEM TERPADU DARI SISTEM: Apakah inovasi yang dihasilkan oleh BPKH telah terintegrasi dengan SIGAP?",
    "6.1": "KETERLIBATAN ORGANISASI PENGEMBANGAN STANDAR INTERNASIONAL - INTERNATIONAL STANDARD ORGANIZATION (ISO) : Apakah BPKH telah melakukan ISO 9001:2015, tentang Manajemen Mutu?",
    "7.1": "KESADARAN DAN PELUANG KEMITRAAN : Apakah ada keterlibatan atau kerjasama dari pihak luar dengan BPKH ?",
    "7.2": "KOLABORASI LINTAS SEKTOR : Apakah BPKH mengimplementasikan kolaborasi interdisipliner lembaga sektor publik ?",
    "7.3": "MENGELOLA KEMITRAAN : Apakah kemitraan yang telah berjalan dikelola dengan baik ?",
    "8.1": "KELOMPOK KERJA : Apakah ada Program Peningkatan Kapasitas dan Pendidikan Infrastruktur DIGT Kehutanan yang direncanakan/diagendakan?",
    "8.2": "PENILAIAN DAN ANALISIS : Apakah telah dilakukan analisis kebutuhan pengembangan kapasitas dalam penyelenggaraan DIGT Kehutanan?",
    "8.4": "PROGRAM PENDIDIKAN TINGGI : Apakah terdapat SDM BPKH yang telah/sedang mengikuti pendidikan formal ke perguruan tinggi untuk memahami konsep penyelenggaraan DIGT?",
    "8.5": "PENDEKATAN PENGEMBANGAN PROFESIONAL : Apakah terdapat SDM BPKH yang telah/sedang mengikuti pendidikan non formal/training untuk memahami konsep penyelenggaraan DIGT ?",
    "8.6": "KETERSEDIAAN Jabatan Fungsional SURVEYOR PEMETAAN (JF SURTA) : Apakah terdapat Jabatan Fungsional Surveyor Pemetaan di Unit Kerja Saudara?",
    "8.7": "KETERSEDIAAN Jabatan Fungsional Pranata Komputer (JF PRAKOM) : Apakah terdapat Jabatan Fungsional Pranata Komputer di Unit Kerja Saudara?",
    "9.1": "TATA KELOLA KOMUNIKASI : Apakah BPKH memiliki pemahaman yang jelas tentang kepentingan pengguna DIGT Kehutanan di wilayah kerjanya ?",
    "9.3": "Penggunaan DIGT oleh Pengguna : Apakah ada analisis penggunaan DIGT dari pengguna ?"
}

# Mapping nomor soal ke judul soal untuk Produsen
QUESTION_MAPPING_PRODUSEN = {
    "1.1": "PEMBENTUKAN KELOMPOK KERJA : Apakah ada tim pelaksana jaringan informasi geospasial lingkup unit kerja anda?",
    "1.3": "STRATEGI GEOSPASIAL : Apakah ada Strategi (Rencana Startegi/Roadmap) yang mengidentifikasi visi, misi, tujuan, dan sasaran inisiatif pengelolaan informasi geospasial untuk menciptakan Satu Data Kehutanan Indonesia?",
    "2.1": "BERBAGI DATA : Apakah ada pengaturan yang efektif dalam kerangka kebijakan dan hukum untuk memastikan proses pengumpulan, pengolahan, pemutakhiran dan quality control di lingkup Unit Kerja Produsen DG?",
    "2.2": "HAK KEKAYAAN INTELEKTUAL: : Apakah ada kerangka kebijakan dan hukum yang kuat yang mengklarifikasi hak kekayaan intelektual (HKI) sehubungan dengan data dan informasi geospasial kehutanan yang diproduksi oleh Produsen DG?",
    "3.1": "TATA KELOLA KEUANGAN DAN AKUNTABILITAS : Apakah terdapat anggaran khusus (APBN) untuk pengumpulan dan penjaminan kualitas DIGT di Unit Kerja Saudara ?",
    "3.2": "SUMBER PENDANAAN : Apakah Produsen DG memiliki sumber pendanaan selain APBN untuk pengumpulan dan penjaminan kualitas DIGT?",
    "4.1": "INFRASTRUKTUR GEODETIK : Apakah ada referensi datum geodetik nasional tunggal yang umum, proyeksi, dan sistem koordinat ?",
    "4.2": "INVENTARIS DATA DAN PROFIL DATA : Apakah telah diidentifikasi serangkaian dataset pada setiap tema IGT ?",
    "4.3": "ANALISIS KESENJANGAN DATA : Apakah semua dataset geospasial telah dibuat dengan tingkat kualitas yang disepakati ?",
    "4.5": "Kualitas Data : Apakah dataset diperiksa kualitas datanya untuk memastikan bahwa data tersebut sesuai dengan tujuan ?",
    "4.6": "METADATA : Apakah metadata tersedia untuk semua layer?",
    "4.7": "PENYIMPANAN DAN PENGAMBILAN DATA : Apakah Produsen DG memiliki infrastruktur penyimpanan dataset/IGT yang aman dan mudah diakses?",
    "4.8": "SIKLUS ALIRAN DATA : Apakah Produsen DG memiliki SOP urutan proses produksi DIGT ?",
    "4.9": "INTEROPERABILITAS DATA : Apakah Produsen DG memiliki Sistem Informasi yang dapat terintegrasi dengan SIGAP ?",
    "5.1": "STRATEGI INOVASI GEOSPASIAL : Apakah ada strategi inovasi untuk mendorong peningkatan kualitas DIGT?",
    "5.2": "INFRASTRUKTUR ICT INTI : Apakah ada sarana-prasarana pendukung inovasi?",
    "5.3": "MODERNISASI ASET DATA : Apakah Produsen DG menggunakan perangkat lunak berlisensi atau tidak untuk perangkat lunak/aplikasi berbasis komersial?",
    "5.5": "SISTEM TERPADU DARI SISTEM : Apakah inovasi yang dihasilkan oleh Produsen DG telah terintegrasi dengan SIGAP ?",
    "6.1": "TATA KELOLA STANDAR : Apakah ada standarisasi dalam penyusunan DIGT di Unit Kerja Produsen DG?",
    "6.2": "STRATEGI/RENCANA STANDAR : Apakah ada Strategi Standar dan proses untuk monitoring kualitas DIGT ?",
    "6.3": "IMPLEMENTASI : Apakah telah ada standar teknologi dan data yang mendukung integrasi dan interoperabilitas antar sistem ?",
    "7.1": "KESADARAN DAN PELUANG KEMITRAAN : Apakah ada keterlibatan atau kerjasama dari pihak luar dengan Produsen DG?",
    "7.2": "KOLABORASI LINTAS SEKTOR : Apakah Produsen DG mengimplementasikan kolaborasi interdisipliner lembaga sektor publik dalam penjaminan kualitas dan penyusunan DIGT Kehutanan?",
    "8.1": "KELOMPOK KERJA : Apakah ada Program Peningkatan Kapasitas dan Pendidikan Infrastruktur DIGT Kehutanan yang direncanakan/diagendakan?",
    "8.2": "PENILAIAN DAN ANALISIS : Apakah telah dilakukan analisis kebutuhan pengembangan kapasitas dalam penyelenggaraan DIGT Kehutanan?",
    "8.4": "PROGRAM PENDIDIKAN TINGGI : Apakah terdapat SDM Produsen DG yang telah/sedang mengikuti pendidikan formal jenjang selanjutnya ke perguruan tinggi untuk memahami konsep penyelenggaraan DIGT ?",
    "8.5": "PENDEKATAN PENGEMBANGAN PROFESIONAL : Apakah terdapat SDM Produsen DG yang telah/sedang mengikuti pendidikan non formal/training untuk memahami konsep penyelenggaraan DIGT ?",
    "8.6": "KETERSEDIAAN Jabatan Fungsional Surveyor Pemetaan (JF SURTA) : Apakah terdapat Jabatan Fungsional Surveyor Pemetaan di Unit Kerja Saudara?",
    "8.7": "KETERSEDIAAN Jabatan Fungsional Pranata Komputer (JF PRAKOM) : Apakah terdapat Jabatan Fungsional Pranata Komputer di Unit Kerja Saudara?"
}

def get_question_mapping(folder_name):
    """
    Menentukan mapping yang digunakan berdasarkan nama folder
    """
    if "bpkh" in folder_name.lower():
        return QUESTION_MAPPING_BPKH
    elif "produsen" in folder_name.lower():
        return QUESTION_MAPPING_PRODUSEN
    else:
        return QUESTION_MAPPING_BPKH  # Default ke BPKH

def create_cover_page(folder_name):
    """
    Membuat halaman cover dengan nama folder
    """
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    width, height = A4
    
    # Tentukan kategori (BPKH atau Produsen)
    if "bpkh" in folder_name.lower():
        category = "BPKH"
    elif "produsen" in folder_name.lower():
        category = "Produsen"
    else:
        category = "Lainnya"
    
    # Format nama folder untuk ditampilkan
    display_name = folder_name.replace("_", " ").title()
    
    # Judul utama
    can.setFont("Helvetica-Bold", 32)
    title = f"Bukti Dukung {category}"
    title_width = can.stringWidth(title, "Helvetica-Bold", 32)
    can.drawString((width - title_width) / 2, height - 200, title)
    
    # Nama folder
    can.setFont("Helvetica-Bold", 20)
    # Split nama panjang jika perlu
    max_width = width - 100
    lines = simpleSplit(display_name, "Helvetica-Bold", 20, max_width)
    
    y_position = height - 250
    for line in lines:
        line_width = can.stringWidth(line, "Helvetica-Bold", 20)
        can.drawString((width - line_width) / 2, y_position, line)
        y_position -= 30
    
    can.save()
    packet.seek(0)
    return packet

def create_separator_page(text, question_mapping, file_exists=True):
    """
    Membuat halaman separator PDF dengan teks (format baru dengan judul pertanyaan)
    """
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    width, height = A4
    
    # Parse nomor dari filename (contoh: no_1_1 -> 1.1)
    # Atau jika sudah format 1.1, gunakan langsung
    if text.startswith("no_"):
        parts = text.replace("no_", "").split("_")
        if len(parts) >= 2:
            number = f"{parts[0]}.{parts[1]}"
        else:
            number = text
    else:
        number = text
    
    # Cari judul soal dari mapping
    question_title = question_mapping.get(number, "")
    
    # Buat teks lengkap
    if file_exists:
        if question_title:
            full_text = f"{number} Bukti Dukung Pertanyaan: {question_title}"
        else:
            full_text = f"{number} Bukti Dukung Pertanyaan"
    else:
        # Jika file tidak ada, tambahkan info "Belum Ada"
        if question_title:
            full_text = f"{number} Bukti Dukung Pertanyaan: {question_title}\n\n[BELUM ADA BUKTI DUKUNG UNTUK PERTANYAAN INI]"
        else:
            full_text = f"{number} Bukti Dukung Pertanyaan\n\n[BELUM ADA BUKTI DUKUNG UNTUK PERTANYAAN INI]"
    
    # Set font
    can.setFont("Helvetica-Bold", 12)
    
    # Split teks panjang menjadi beberapa baris
    max_width = width - 80  # Margin 40 di kiri dan kanan
    lines = simpleSplit(full_text, "Helvetica-Bold", 12, max_width)
    
    # Hitung tinggi box berdasarkan jumlah baris
    line_height = 18
    box_height = max(100, len(lines) * line_height + 40)
    box_width = width - 60
    
    # Posisi box di tengah
    x = (width - box_width) / 2
    y = (height - box_height) / 2
    
    # Gambar border (merah jika tidak ada file)
    if file_exists:
        can.setStrokeColorRGB(0, 0, 0)
    else:
        can.setStrokeColorRGB(1, 0, 0)  # Merah untuk yang belum ada
    can.setLineWidth(2)
    can.rect(x, y, box_width, box_height)
    
    # Tulis teks (multi-line)
    text_y = y + box_height - 30
    for line in lines:
        # Warna merah untuk teks "BELUM ADA"
        if "[BELUM ADA" in line:
            can.setFillColorRGB(1, 0, 0)
        else:
            can.setFillColorRGB(0, 0, 0)
        can.drawString(x + 20, text_y, line)
        text_y -= line_height
    
    can.save()
    packet.seek(0)
    return packet

def convert_image_to_pdf(image_path):
    """
    Konversi gambar (PNG, JPG, dll) ke PDF
    Mendukung long path (>260 karakter) di Windows
    """
    packet = io.BytesIO()
    
    # Gunakan long path untuk Windows
    abs_path = os.path.abspath(image_path)
    if os.name == 'nt' and not abs_path.startswith('\\\\?\\'):
        long_path = '\\\\?\\' + abs_path
    else:
        long_path = abs_path
    
    # Buka gambar dengan long path
    img = Image.open(long_path)
    
    # Konversi RGBA ke RGB jika perlu
    if img.mode == 'RGBA':
        # Buat background putih
        background = Image.new('RGB', img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3])  # 3 adalah alpha channel
        img = background
    elif img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Simpan sebagai PDF
    img.save(packet, 'PDF', resolution=100.0)
    packet.seek(0)
    
    return packet

def get_sorted_files(directory):
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
        # Fallback ke method lama
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            try:
                if os.path.isfile(file_path):
                    ext = os.path.splitext(file)[1].lower()
                    if ext in supported_extensions:
                        files.append(file_path)
            except:
                continue
    
    # Sort berdasarkan nama file
    files.sort()
    return files

def extract_question_number(filename):
    """
    Ekstrak nomor pertanyaan dari nama file (contoh: no_1_1 -> 1.1)
    """
    # Pattern: no_X_Y
    match = re.search(r'no_(\d+)_(\d+)', filename)
    if match:
        return f"{match.group(1)}.{match.group(2)}"
    return None

def sort_question_numbers(question_list):
    """
    Sort nomor pertanyaan secara numerik (1.1, 1.2, ..., 1.10, 2.1, dll)
    """
    def sort_key(q):
        parts = q.split('.')
        return (int(parts[0]), int(parts[1]))
    return sorted(question_list, key=sort_key)

def get_all_expected_questions(question_mapping):
    """
    Mendapatkan semua nomor pertanyaan yang diharapkan dari mapping
    """
    return sort_question_numbers(list(question_mapping.keys()))

def merge_files_in_directory(input_dir, output_dir):
    """
    Merge semua PDF dan gambar dalam satu direktori menjadi satu PDF
    dengan cover page dan separator bernomor dengan judul pertanyaan
    Menambahkan separator "Belum Ada" untuk pertanyaan yang tidak memiliki file
    """
    # Ambil nama folder sebagai nama output
    folder_name = os.path.basename(input_dir)
    
    # Tentukan subfolder output berdasarkan kategori
    if "bpkh" in folder_name.lower():
        category_folder = os.path.join(output_dir, "BPKH")
    elif "produsen" in folder_name.lower():
        category_folder = os.path.join(output_dir, "Produsen")
    else:
        category_folder = output_dir
    
    # Pastikan folder kategori ada
    os.makedirs(category_folder, exist_ok=True)
    
    output_filename = f"{folder_name}.pdf"
    output_path = os.path.join(category_folder, output_filename)
    
    # Tentukan mapping yang sesuai
    question_mapping = get_question_mapping(folder_name)
    
    # Ambil semua file yang akan di-merge
    files = get_sorted_files(input_dir)
    
    # Buat dictionary untuk mapping nomor soal ke file
    question_files = {}
    for file_path in files:
        filename = os.path.basename(file_path)
        question_num = extract_question_number(filename)
        if question_num:
            if question_num not in question_files:
                question_files[question_num] = []
            question_files[question_num].append(file_path)
    
    # Dapatkan semua nomor soal yang diharapkan dari mapping
    expected_questions = get_all_expected_questions(question_mapping)
    
    # Gabungkan dengan nomor dari file yang ada (untuk menangkap file yang tidak ada di mapping)
    all_question_numbers = set(expected_questions) | set(question_files.keys())
    all_question_numbers = sort_question_numbers(list(all_question_numbers))
    
    print(f"\n📁 Memproses: {folder_name}")
    print(f"   File ditemukan: {len(files)}")
    print(f"   Pertanyaan dari mapping: {len(expected_questions)}")
    print(f"   Pertanyaan dari file: {len(question_files)}")
    print(f"   Total pertanyaan yang akan diproses: {len(all_question_numbers)}")
    
    # Buat merger
    merger = PdfMerger()
    
    try:
        # Tambahkan cover page di awal
        cover_pdf = create_cover_page(folder_name)
        merger.append(cover_pdf)
        print(f"   ✓ Cover Page: Bukti Dukung {folder_name}")
        
        # Proses setiap nomor soal (dari mapping + file yang ada)
        for question_num in all_question_numbers:
            # Buat separator
            if question_num in question_files:
                # Ada file untuk soal ini
                separator_pdf = create_separator_page(question_num, question_mapping, file_exists=True)
                merger.append(separator_pdf)
                print(f"   ✓ Separator: {question_num}")
                
                # Tambahkan semua file untuk soal ini
                for file_path in question_files[question_num]:
                    filename = os.path.basename(file_path)
                    file_ext = os.path.splitext(filename)[1].lower()
                    
                    try:
                        if file_ext == '.pdf':
                            # Gunakan long path untuk membuka file
                            abs_path = os.path.abspath(file_path)
                            if os.name == 'nt' and not abs_path.startswith('\\\\?\\'):
                                long_path = '\\\\?\\' + abs_path
                            else:
                                long_path = abs_path
                            
                            # Baca file ke BytesIO untuk menghindari masalah path
                            with open(long_path, 'rb') as f:
                                pdf_content = io.BytesIO(f.read())
                            merger.append(pdf_content)
                            print(f"   ✓ PDF: {filename[:60]}...")
                        else:
                            # Konversi gambar ke PDF
                            image_pdf = convert_image_to_pdf(file_path)
                            merger.append(image_pdf)
                            print(f"   ✓ Image: {filename[:60]}...")
                    except Exception as e:
                        print(f"   ❌ Error processing {filename[:50]}...: {str(e)}")
            else:
                # Tidak ada file untuk soal ini - buat separator "Belum Ada"
                separator_pdf = create_separator_page(question_num, question_mapping, file_exists=False)
                merger.append(separator_pdf)
                print(f"   ⚠️  Separator: {question_num} [BELUM ADA BUKTI DUKUNG]")
        
        # Simpan hasil merge
        merger.write(output_path)
        merger.close()
        
        print(f"   ✅ Berhasil: {output_filename}\n")
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)}\n")
        merger.close()

def process_all_subdirectories(base_dir, output_dir):
    """
    Proses semua subdirektori dalam base_dir
    """
    # Pastikan output directory ada
    os.makedirs(output_dir, exist_ok=True)
    
    # Cari semua subdirektori
    for root, dirs, files in os.walk(base_dir):
        # Skip direktori base itu sendiri
        if root == base_dir:
            continue
        
        # Hanya proses direktori yang langsung berisi file (bukan parent directory)
        # Cek apakah ada file di direktori ini
        try:
            has_files = any(os.path.isfile(os.path.join(root, f)) for f in os.listdir(root))
            if has_files:
                merge_files_in_directory(root, output_dir)
        except Exception as e:
            print(f"⚠️  Error checking directory {root}: {str(e)}")

def main():
    """
    Main function
    """
    # Path base
    base_path = r"D:\01 - All Project 2025\01 - IPSDH\06 - SIGAP AWARD - FORM\00 - ALL BUKTI DUKUNG SIGAP AWARD 2025\merging-pdf-sigap-award"
    
    files_dir = os.path.join(base_path, "files")
    output_dir = os.path.join(base_path, "output 3")
    
    print("=" * 60)
    print("🚀 MEMULAI PROSES MERGING PDF DAN GAMBAR")
    print("=" * 60)
    
    # Proses semua subdirektori
    process_all_subdirectories(files_dir, output_dir)
    
    print("=" * 60)
    print("✅ PROSES SELESAI!")
    print("=" * 60)
    print(f"📂 Output disimpan di: {output_dir}")

if __name__ == "__main__":
    main()