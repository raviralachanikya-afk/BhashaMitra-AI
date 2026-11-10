# BhashaMitra AI 🇮🇳

### A Multilingual Voice-Based Grocery Ordering Assistant

BhashaMitra AI is a voice-enabled grocery ordering assistant designed to help Indian customers place grocery orders in their preferred languages: Hindi, Telugu and Hinglish.

The application uses Gnani AI speech technologies to understand spoken grocery orders and generate voice-based confirmations.

## Features

- Multilingual voice input.
- Speech-to-text transcription using Gnani AI Prisma.
- Grocery product and quantity extraction.
- Automatic estimated bill calculation.
- Text-to-speech responses using Gnani AI Timbre.
- Text-based ordering alternative.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core development |
| FastAPI | Backend APIs |
| Streamlit | Frontend interface |
| Gnani Prisma | Speech recognition |
| Gnani Timbre | Voice generation |

## Supported Languages

- Hindi
- Telugu
- Hinglish

## Project Structure

```text
BhashaMitra-AI/
├── backend/
│   └── main.py
├── frontend/
│   └── app.py
├── services/
│   ├── gnani_service.py
│   └── order_service.py
├── .gitignore
└── requirements.txt
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/raviralachanikya-afk/BhashaMitra-AI.git
cd BhashaMitra-AI
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
pip install gnani-vachana
```

### 4. Configure API credentials

Create a `.env` file in the project root:

```env
GNANI_API_KEY=your_actual_api_key
```

Never upload your API key to GitHub.

### 5. Start the backend

```bash
python -m uvicorn backend.main:app --reload
```

### 6. Start the frontend

Open another terminal:

```bash
source .venv/bin/activate
python -m streamlit run frontend/app.py
```

## Example

A customer can say:

"मुझे दो किलो चावल और एक लीटर दूध चाहिए।"

The application transcribes the request, identifies the grocery items and quantities, calculates an estimated bill and generates a spoken confirmation.

## Future Improvements

- Real-time inventory integration.
- Database-backed order management.
- More Indian regional languages.
- WhatsApp integration.
- Secure online payments.

## Project Status

Working prototype developed as part of the Great Indian AI Internship Challenge.

**Note:** Product prices are illustrative. The current prototype does not process real purchases or payments.

## Developer

Chanikya Ravirala

GitHub: https://github.com/raviralachanikya-afk