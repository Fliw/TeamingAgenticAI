<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/1659705f-3955-42cc-96f4-5af91dd1b287" />

# Teaming Agentic AI

> Platform multi-agent system yang memungkinkan beberapa AI agent bekerja sama dalam tim untuk menyelesaikan tugas-tugas kompleks.

## Tentang Project

Teaming Agentic AI adalah platform chatbot cerdas berbasis multi-agent system yang dirancang untuk menciptakan sistem AI yang dapat berkolaborasi. Sistem ini menggunakan teknologi AI untuk memberikan layanan informasi dan bantuan dalam berbagai domain, dengan setiap agent memiliki spesialisasi masing-masing.

Project ini dibangun menggunakan framework **Agno** yang memungkinkan pembuatan sistem multi-agent yang dapat berkolaborasi untuk menyelesaikan berbagai tugas kompleks. Setiap agent memiliki spesialisasi masing-masing dan dapat bekerja secara individual atau dalam tim untuk memberikan solusi terbaik bagi pengguna.

## Agent-Agent

### Dakdak - Academic Administrator
**Role**: Academic Administrator  
**Spesialisasi**: Administrasi Akademik

Dakdak adalah agent yang fokus menangani semua urusan administrasi akademik. Agent ini bisa membantu dengan:
- Informasi tentang perencanaan studi dan kurikulum
- Jadwal dan mata kuliah
- Informasi nilai dan transkrip
- Pertanyaan seputar kurikulum
- Brainstorming terkait administrasi akademik

**Kemampuan**:
- Reasoning tools untuk analisis pertanyaan kompleks
- Database SQLite untuk menyimpan riwayat percakapan
- Session summaries untuk konteks percakapan yang lebih baik
- Markdown support untuk format respons yang lebih rapi

### Kiko - Student Administration
**Role**: Student Administration  
**Spesialisasi**: Administrasi Keuangan & Beasiswa

Kiko adalah agent yang mengurus semua hal terkait administrasi keuangan. Agent ini bisa membantu dengan:
- Informasi biaya dan pembayaran
- Cara pembayaran dan prosedur administrasi
- Informasi beasiswa yang tersedia
- Prosedur pendaftaran beasiswa
- Pertanyaan seputar keuangan

**Kemampuan**:
- Reasoning tools untuk analisis pertanyaan kompleks
- Database SQLite untuk menyimpan riwayat percakapan
- Session summaries untuk konteks percakapan yang lebih baik
- Markdown support untuk format respons yang lebih rapi

### Lumi - Research Assistant
**Role**: Research Assistant  
**Spesialisasi**: Penelitian & Skripsi

Lumi adalah asisten penelitian yang siap membantu dengan semua hal terkait penelitian dan akademik. Agent ini bisa membantu dengan:
- Mencari topik penelitian yang menarik
- Mencari jurnal dan paper penelitian terkait
- Brainstorming ide penelitian
- Informasi tentang metodologi penelitian
- Referensi dari Arxiv dan Wikipedia

**Kemampuan**:
- **ArxivTools** - Mencari jurnal dan paper penelitian dari Arxiv
- **WikipediaTools** - Mencari informasi dari Wikipedia
- Reasoning tools untuk analisis pertanyaan kompleks
- Database SQLite untuk menyimpan riwayat percakapan
- Compress tool results untuk efisiensi
- Session summaries untuk konteks percakapan yang lebih baik

### Nobi - New Student Orientation
**Role**: New Student Orientation  
**Spesialisasi**: Orientasi & Kegiatan

Nobi adalah agent yang fokus membantu orientasi dan menginformasikan kegiatan-kegiatan. Agent ini bisa membantu dengan:
- Informasi pendaftaran dan orientasi
- Informasi kegiatan dan program
- Program-program yang tersedia
- Informasi dari API eksternal (contoh: Brofesional)

**Kemampuan**:
- **getProgramBrofesional** - Mengambil data program dari API eksternal
- Reasoning tools untuk analisis pertanyaan kompleks
- Database SQLite untuk menyimpan riwayat percakapan
- Session summaries untuk konteks percakapan yang lebih baik
- Markdown support untuk format respons yang lebih rapi

## Team MIKO

**Miko Team** adalah tim koordinator yang mengatur dan mengarahkan semua agent di atas. Team ini berfungsi sebagai:
- **Router** - Mengarahkan pertanyaan ke agent yang tepat
- **Koordinator** - Mengkoordinasikan kolaborasi antar agent jika diperlukan
- **Interface Utama** - Menjadi titik kontak pertama dengan pengguna

**Fitur Team MIKO**:
- Respond langsung ke pengguna
- Menampilkan respons dari semua member agent
- Reasoning tools untuk analisis kompleks
- Session management yang canggih
- Kompresi hasil tool untuk efisiensi

**Alur Kerja**:
1. Pengguna mengajukan pertanyaan ke Miko Team
2. Team menganalisis pertanyaan dan menentukan agent yang tepat
3. Agent yang ditunjuk memberikan respons
4. Team menampilkan hasil ke pengguna

## Tech Stack

### Core Framework
- **Agno** - Framework utama untuk multi-agent system
- **FastAPI** - Web framework untuk API server
- **Uvicorn** - ASGI server untuk menjalankan aplikasi

### AI/ML Models
- **Ollama** - Model LLM lokal (menggunakan `ministral-3:8b-instruct-2512-q4_K_M`)
- **Groq** - Alternatif model cloud (opsional, saat ini dikomen)

### Database & Storage
- **SQLite** - Database untuk menyimpan riwayat percakapan dan session

### Tools & Libraries
- **Arxiv** - Library untuk mengakses jurnal penelitian
- **Wikipedia** - Library untuk mengakses informasi Wikipedia
- **Requests** - HTTP library untuk API calls
- **Python-dotenv** - Environment variable management

### Development Tools
- **SQLAlchemy** - ORM untuk database operations

## Setup & Installation

### Prerequisites
- Python 3.8+ 
- Ollama terinstall dan running di local machine
- Model `ministral-3:8b-instruct-2512-q4_K_M` sudah didownload di Ollama

### Langkah-langkah Setup

1. **Clone repository** (jika belum)
```bash
git clone <repository-url>
cd "miko agno"
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Setup environment variables** (opsional)
Buat file `.env` di root directory jika ingin menggunakan Groq atau konfigurasi lainnya:
```env
GROQ_API_KEY_DAKDAK=your_groq_api_key
GROQ_API_KEY_KIKO=your_groq_api_key
GROQ_API_KEY_LUMI=your_groq_api_key
GROQ_API_KEY_NOBI=your_groq_api_key
GROQ_API_KEY_MIKO=your_groq_api_key
```

4. **Pastikan Ollama running**
```bash
# Cek apakah Ollama sudah running
ollama list

# Jika model belum ada, download dulu
ollama pull ministral-3:8b-instruct-2512-q4_K_M
```

5. **Jalankan server**
```bash
python server.py
```

Server akan berjalan di `http://localhost:8000` dengan auto-reload enabled.

### Setup Database
Database SQLite akan otomatis dibuat saat pertama kali agent dijalankan. File database akan tersimpan di folder `db/`:
- `dakdak_agent.db` - Database untuk agent Dakdak
- `kiko_agent.db` - Database untuk agent Kiko
- `lumi_agent.db` - Database untuk agent Lumi
- `nobi_agent.db` - Database untuk agent Nobi
- `miko_team.db` - Database untuk Miko Team

## Struktur Project

```
miko agno/
├── agents/              # Folder untuk semua agent
│   ├── dakdak.py       # Agent Dakdak (Academic Admin)
│   ├── kiko.py         # Agent Kiko (Student Admin)
│   ├── lumi.py         # Agent Lumi (Research Assistant)
│   └── nobi.py         # Agent Nobi (New Student Orientation)
├── teams/              # Folder untuk team
│   └── miko.py         # Miko Team configuration
├── mcp/                # MCP (Model Context Protocol) tools
│   └── API_MCP.py      # Custom tool untuk API eksternal
├── db/                 # Database files (auto-generated)
│   ├── dakdak_agent.db
│   ├── kiko_agent.db
│   ├── lumi_agent.db
│   ├── nobi_agent.db
│   └── miko_team.db
├── server.py           # Main server file
├── requirements.txt    # Python dependencies
└── readme.md          # Dokumentasi project
```

## Cara Menggunakan

Setelah server running, kamu bisa menggunakan sistem ini melalui:

### AgentOS
AgentOS adalah interface berbasis web yang disediakan oleh framework Agno. Akses AgentOS melalui browser setelah server dijalankan.

### AgentUI
AgentUI adalah user interface yang disediakan oleh framework Agno untuk berinteraksi dengan agent dan team. UI ini menyediakan interface yang user-friendly untuk chatting dengan agent atau team.

## Notes

- Semua agent menggunakan bahasa Indonesia dengan gaya Gen Z yang friendly
- Setiap agent memiliki database terpisah untuk isolasi data
- Session summaries diaktifkan untuk konteks percakapan yang lebih baik
- Reasoning tools digunakan untuk pertanyaan kompleks yang membutuhkan analisis mendalam
