
import streamlit as st
import pytesseract
from PIL import Image
from googlesearch import search
import requests
from bs4 import BeautifulSoup
import os
import datetime

st.set_page_config(page_title="Cat CPT", layout="centered")

# Konuları saklamak için session state
if "conversations" not in st.session_state:
    st.session_state.conversations = []
if "current_topic" not in st.session_state:
    st.session_state.current_topic = "Genel Konuşma"

# Yeni konu başlat butonu
if st.button("➕ Yeni Konu"):
    st.session_state.current_topic = f"Konu ({datetime.datetime.now().strftime('%H:%M:%S')})"
    st.session_state.conversations.append((st.session_state.current_topic, []))

# Konu seçimi veya oluşturulmamışsa ilk konu
if len(st.session_state.conversations) == 0:
    st.session_state.conversations.append((st.session_state.current_topic, []))

# Mevcut konu verisine referans
topic_index = next(i for i, (t, _) in enumerate(st.session_state.conversations) if t == st.session_state.current_topic)
messages = st.session_state.conversations[topic_index][1]

# Konu başlığı
st.markdown(f"## 🧠 {st.session_state.current_topic}")

# Geçmiş konuşmaları göster
for i, (sender, msg) in enumerate(messages):
    with st.chat_message(sender):
        st.markdown(msg)

# Giriş kutusu ve dosya yükleme
with st.container():
    user_input = st.chat_input("Mesajınızı yazın...")
    uploaded_file = st.file_uploader("📎 Dosya/Fotograf", type=["png", "jpg", "jpeg", "txt", "pdf"], label_visibility="collapsed")

# Mesaj gönderildiyse
if user_input or uploaded_file:
    if user_input:
        messages.append(("user", user_input))
        with st.chat_message("user"):
            st.markdown(user_input)

        if any(user_input.lower().startswith(q) for q in ["nedir", "kim", "nasıl", "ne", "kaç"]):
            try:
                query = user_input.strip()
                result_links = list(search(query, num_results=2))
                if result_links:
                    first_link = result_links[0]
                    page = requests.get(first_link, timeout=10)
                    soup = BeautifulSoup(page.text, "html.parser")
                    paragraphs = soup.find_all("p")
                    found_text = ""
                    for p in paragraphs:
                        if len(p.text.strip()) > 60:
                            found_text = p.text.strip()
                            break
                    if found_text:
                        answer = f"Sorduğun şeyle ilgili şöyle bir bilgi buldum: {found_text}"
                    else:
                        answer = f"Bu konuda araştırdım ama uygun bir içerik bulamadım. Kaynak: {first_link}"
                else:
                    answer = "Araştırma sonucunda bir şey bulamadım."
            except Exception as e:
                answer = f"Araştırma sırasında hata oluştu: {str(e)}"

            messages.append(("assistant", answer))
            with st.chat_message("assistant"):
                st.markdown(answer)

        elif any(x in user_input.lower() for x in ["yorumla", "analiz et"]):
            answer = f"Bu konuda şöyle düşünüyorum: {user_input} oldukça ilginç bir konu. İçeriğini değerlendirirken hem bağlam hem de niyet göz önüne alınmalı."
            messages.append(("assistant", answer))
            with st.chat_message("assistant"):
                st.markdown(answer)
        else:
            answer = f"Söylediğini anladım: '{user_input}'. Sana nasıl yardımcı olabilirim?"
            messages.append(("assistant", answer))
            with st.chat_message("assistant"):
                st.markdown(answer)

    if uploaded_file:
        filetype = uploaded_file.type
        messages.append(("user", f"📎 Dosya yüklendi: {uploaded_file.name}"))
        with st.chat_message("user"):
            st.markdown(f"📎 Dosya yüklendi: {uploaded_file.name}")

        if filetype.startswith("image"):
            image = Image.open(uploaded_file)
            text = pytesseract.image_to_string(image)
            messages.append(("assistant", f"📖 Görselden okunan metin:
{text}"))
            with st.chat_message("assistant"):
                st.markdown(f"📖 Görselden okunan metin:
{text}")
        else:
            messages.append(("assistant", "🔍 Bu dosya türü şu anda desteklenmiyor."))
            with st.chat_message("assistant"):
                st.markdown("🔍 Bu dosya türü şu anda desteklenmiyor.")
