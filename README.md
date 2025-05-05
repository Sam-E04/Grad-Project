# SyncSec

**SyncSec** is a modular, human-in-the-loop Purple Team tool that bridges offensive testing and defensive refinement through AI-assisted detection engineering. Designed for red-blue collaboration, it provides a streamlined platform for attack simulation, ModSecurity log parsing, detection visualization, and AI-generated rule recommendations.

---

## 🚀 Features

- 🔴 **Red Teaming**: Execute simulated SQLi, XSS, LFI, CMDi attacks via automated payloads.
- 🔵 **Blue Teaming**: Parse live ModSecurity logs, extract and simplify alerts into structured detection data.
- 🟣 **Purple Team Analysis**:
  - Matches attack logs with detection logs.
  - Flags missed detections and false positives.
  - Visualizes detection coverage via pie charts and tables.
  - Suggests improvements using HuggingFace-hosted LLM.
- 📊 **Streamlit Frontend**: Tab-based UI for red, blue, and purple team workflows.
- 🌐 **Flask Backend**: Serves simplified ModSecurity alerts via an API.

---

## 📂 Project Structure

```
└──SyncSec/
  ├── main.py # Streamlit dashboard
  ├── red.py # Attack automation
  ├── purple.py # Detection comparison logic
  ├── log_manager.py # Logging and I/O helpers
  ├── mediator.py # AI-based recommendations
  ├── requirements.txt
  └──.streamlit/
    └──config.toml
└──logs/ │
  ├── attack_logs.json
  ├── detection_logs.json
  └── update_detection_logs.py
```

---

## ⚙️ Installation

> Python 3.10+ is recommended. Use a virtual environment.

### 1. Clone the repository:

```bash
git clone https://github.com/yourusername/SyncSec.git
cd SyncSec

pip install -r requirements.txt
```

---

## 🧪 Running the Tool

### 🔷 1. Launch the SyncSec Streamlit Frontend

```bash
streamlit run main.py
```

## 🤖 AI Recommendations

SyncSec integrates with Hugging Face's hosted LLMs to assist with detection refinement by suggesting improvements for missed attacks and false positives.

> 💡 API key required:  
> Set your Hugging Face token inside `mediator.py` like so:
> ```python
> AIModel(api_key="your_api_key", model_name="mistralai/Mixtral-8x7B-Instruct-v0.1")
> ```

---

## 📊 Example Output

- ✅ Table of matched, missed, and false detections
- 🟣 Color-coded pie chart showing detection accuracy
- 🤖 AI-generated solutions for detection gaps and false alerts

---

## 🛡️ Use Cases

SyncSec is ideal for:

- 🧪 Purple teaming exercises
- 🔍 Detection engineering validation
- 🎓 University security labs
- 🎯 Red vs. Blue CTF-style environments

---

## 📜 License

MIT License — free to use, adapt, and redistribute.

Developed by Ismail Ahmed Mohamed.
