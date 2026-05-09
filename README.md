# Psychological Risk Detection & Mental Wellness Platform

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.103+-009688.svg)
![React](https://img.shields.io/badge/React-18.2-61DAFB.svg)
![Vite](https://img.shields.io/badge/Vite-5.2-646CFF.svg)

## 📌 Overview
This project is a comprehensive **Mental Wellness and Risk Assessment Web Application** designed to evaluate psychological risk levels through natural language processing (NLP). By combining a supportive, Gen-Z focused "Digital Wellness" aesthetic with robust backend analytics, the platform processes user narrations and classifies their mental health risk into **Low, Moderate, or High** categories.

The core classification engine leverages **VADER Sentiment Analysis** and custom **LIWC (Linguistic Inquiry and Word Count) dictionary logic**, which is intricately mapped to **DASS-21** (Depression, Anxiety, and Stress Scale) standard values.

## ✨ Key Features
- **Advanced NLP Risk Classification:** Evaluates textual input using semantic analysis, outputting a quantifiable risk score based on clinical DASS-21 mappings.
- **Machine Learning Benchmarking:** Includes a robust evaluation pipeline comparing four different ML classification models to determine the most accurate approach (maximizing Precision, Recall, and Accuracy).
- **Multi-Stage Assessment Flow:** Guides users through a progressive, 3-stage interactive questionnaire and storytelling interface.
- **"Gen-Z" UI/UX Design System:** Features a highly polished, responsive React frontend. Utilizes `GSAP` for fluid micro-animations, glassmorphism components, floating aesthetic blobs, and a curated typography stack (Outfit & Reenie Beanie).
- **High-Performance API:** Powered by FastAPI for asynchronous, low-latency communication between the client and the NLP processing engine.

## 🛠️ Tech Stack
**Frontend:**
- React (Vite)
- Zustand (State Management)
- GSAP (Animations & Transitions)
- Lucide React (Iconography)

**Backend & ML:**
- Python & FastAPI
- spaCy & VADER Sentiment Analysis (NLP)
- Scikit-Learn (Classification Benchmarks)
- NumPy & Pandas (Data Processing)

## 🚀 Getting Started

### Prerequisites
- Node.js (v18+)
- Python 3.10+

### Backend Setup
1. Navigate to the project root.
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the FastAPI server:
   ```bash
   uvicorn api_fastapi:app --reload
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the Vite development server:
   ```bash
   npm run dev
   ```

## 📊 Analytics & Benchmarks
The repository contains scripts (`ml_classifier_benchmark.py`, `compute_metrics.py`, `plot_results.py`) used to benchmark the NLP logic against standard datasets, plotting confusion matrices and evaluating F1-scores to ensure the model provides a reliable indicator of psychological risk.

## 🤝 Contributing
Contributions, issues, and feature requests are welcome. Feel free to check the issues page if you want to contribute.
