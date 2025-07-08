import streamlit as st
import json 
from pathlib import Path
import datetime

NOTES_FILE = Path("notes_data.json")

def load_notes():
    if NOTES_FILE.exists():
        with open(NOTES_FILE, "r") as f:
            return json.load(f)
        return[]
    
def save_notes(notes):
    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f, indent=2)

notes = load_notes()

st.set_page_config(page_title="CodeNotes 📖", layout="centered")
st.title("🧠 CodeNotes: Your Smart Notes")
st.markdown("Khusus untuk catatan programming biar lebih terstruktur🔥🔥🔥")

st.subheader("📝 Tambahkan catatan baru")
with st.form("new_note_form"):
    title = st.text_input("Judul")
    category = st.selectbox("Kategori", ["Phyton", "Git", "Debugging", "Algoritma", "Logika", "Tips Umum", "Lainnya"])
    content = st.text_area("Isi Catatan")
    submitted = st.form_submit_button("Simpan")

if submitted: 
    if title and content: 
        note = {
            "title": title,
            "category": category,
            "content": content,
            "date": datetime.date.today().isoformat()
        }
        notes.insert(0, note)
        save_notes(notes)
        st.success("Catatan berhasil disimpan!")
        st.rerun()
    else: 
        st.warning("Judul dan isi catatan tidak boleh kosong ")

st.subheader("🔍 Filter Catatan") 
search_query = st.text_input("cari berdasarkan kata kunci")
category_filter = st.selectbox("Filter berdasarkan kategori:", ["Semua"] + list(set(n['category'] for n in notes))) 

filtered_notes = notes
if search_query:
    filtered_notes = [n for n in filtered_notes if search_query.lower() in n['title'].lower() or search_query.lower() in n['content'].lower()]
if category_filter != "Semua":
    filtered_notes = [n for n in filtered_notes if n['category'] == category_filter]

# ===== RIWAYAT CATATAN =====
st.subheader("📚 Riwayat Catatan")
if not filtered_notes:
    st.info("Belum ada catatan sesuai filter. Yuk mulai catat dari sekarang!")
else:
    for i, note in enumerate(filtered_notes):
        with st.expander(f"📌 {note['title']} [{note['category']}] - {note['date']}"):
            st.write(note['content'])
            if st.button("🗑️ Hapus", key=f"delete_{i}"):
                notes.remove(note)
                save_notes(notes)
                st.success("Catatan dihapus!")
                st.rerun()
