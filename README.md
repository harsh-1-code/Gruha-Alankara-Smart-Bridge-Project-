# Gruha Alankara 🏠✨

**Interior Design Platform with AR and AI Integration**

Gruha Alankara is an AI and AR-powered Interior Design Platform built using Python and Flask. It uses localized AI models to provide personalized interior design recommendations, real-time room analysis, and immersive augmented reality visualizations without relying on cloud-heavy infrastructure.

---

## 🌟 Features

- **AI Room Analyzer**: Upload photos of your room to detect dimensions, lighting, and existing furniture.
- **Smart Design Studio**: Generate tailored design recommendations using Transformer models (ViT & T5).
- **AR Furniture Viewer**: Live camera integration to visualize furniture placement in your own space.
- **Classic Dark Theme**: A premium, responsive UI designed for an immersive creative experience.
- **Multilingual Voice Assistant**: Support for design queries in English, Hindi, and Telugu.
- **Smart Catalog**: Automated booking and procurement handle

https://github.com/user-attachments/assets/81755aea-876f-43fe-baeb-1b4bd0649b64

d by an intelligent design agent.

---

## 🛠️ Technology Stack

- **Backend**: Python, Flask, Flask-SQLAlchemy
- **AI/ML**: HuggingFace Transformers, OpenCV, LangChain
- **Database**: SQLite
- **Frontend**: HTML5, Vanilla CSS, JavaScript (MediaDevices API)
- **Voice**: Google Text-to-Speech

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.9+
- A modern browser with WebRTC support (Chrome/Edge)

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/divapandey1120/Gruha-Alankara.git
cd Gruha-Alankara

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### 3. Initialize Database
```bash
python init_db.py
```

### 4. Run the Application
```bash
python app.py
```
Access the app at `http://127.0.0.1:5000`.

---

## 📐 Project Structure

- `app.py`: Main application entry point and routes.
- `models.py`: Database schema and ORM models.
- `agents/`: AI agent orchestration logic.
- `tools/`: Specialized AI tools (recommender, analyzer, budget planner).
- `static/`: CSS and Client-side JS.
- `templates/`: Jinja2 HTML templates.

---

## 🗺️ Roadmap
Check [future_enhancement.md](file:///c:/Work/Gruha-Alankara/future_enhancement.md) for planned features like Redis caching, Three.js 3D previews, and 2FA.

---

## 📄 License
This project is for educational and portfolio purposes.
