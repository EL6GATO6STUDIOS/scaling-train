# Cat CPT 😺

Cat CPT, dosya yorumlayabilen, gündelik konuşmaları anlayan, analiz yapabilen ve Google üzerinden araştırma yapabilen bir yapay zeka sohbet uygulamasıdır.

## Özellikler

- Görselden metin okuma (OCR)
- Basit analiz ve yorumlama
- Gündelik ifadeleri anlama
- Google araştırması yapabilme
- Sohbet konularını otomatik ayırma

## Gereksinimler

```bash
pip install -r requirements.txt
```

## Çalıştırmak için

```bash
streamlit run app.py
```

## Notlar

- Görsellerden metin okumak için sistemde Tesseract OCR yüklü olmalıdır.
- Uygulama araştırma yaparken `googlesearch-python` kullanır.