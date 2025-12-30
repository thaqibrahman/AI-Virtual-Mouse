# AI Virtual Mouse Using Hand Gestures

An intelligent, touchless human–computer interaction system that enables users to control mouse operations using real-time hand gesture recognition. The application leverages computer vision and AI techniques to eliminate the need for physical input devices.

## 🔍 Problem Statement

Traditional input devices such as mice and touchpads require physical interaction, which may not be suitable for:
- Accessibility-focused systems
- Touchless environments
- Smart workspaces
- Future AR/VR and HCI applications

This project provides a **gesture-based virtual mouse** as an alternative input solution.

## 💡 Solution Overview

The system captures live video from a webcam, detects hand landmarks using MediaPipe, interprets gestures, and maps them to mouse actions using PyAutoGUI — all in real time.

## ✨ Key Features

- Real-time hand tracking using AI
- Smooth and accurate cursor movement
- Left-click and right-click gesture recognition
- System volume control
- Screenshot capture functionality
- Hardware-independent and platform-agnostic

## 🧠 Technical Architecture

1. Video frame acquisition via webcam  
2. Hand landmark detection (21 key points) using MediaPipe  
3. Gesture recognition based on landmark geometry  
4. Action mapping to system mouse events  

## 🛠️ Tech Stack

| Category             | Technologies |
|----------------------|--------------|
| Language             | Python       |
| Computer Vision      | OpenCV       |
| Hand Tracking        | MediaPipe    |
| Automation           | PyAutoGUI    |
| System Control       | ctypes       |
| Numerical Processing | NumPy        |


## 📂 Project Structure
AI-Virtual-Mouse/
│
├── virtual_mouse.py # Core application logic
├── requirements.txt # Project dependencies
├── screenshots/ # Output samples
└── README.md # Project documentation


## ⚙️ Installation & Execution

### Prerequisites
- Python 3.8+
- Webcam

### Steps

```bash
git clone https://github.com/your-username/AI-Virtual-Mouse.git
cd AI-Virtual-Mouse
pip install -r requirements.txt
python virtual_mouse.py
```
📈 Performance Highlights

- Low-latency real-time gesture recognition
- High accuracy hand landmark detection
- Stable cursor movement with minimal jitter
<img width="600" height="650" alt="Screenshot 2025-05-08 204744" src="https://github.com/user-attachments/assets/2af57456-81fa-43dd-b092-5a209c6f9dd3" />


🔮 Future Enhancements

- Gesture customization module
- Multi-hand and multi-gesture support
- Deep learning–based gesture classification
- Cross-platform optimization (Linux, macOS)

👨‍💻 Author

Mohammed Thaqib ul Rahman
Final-Year B.Tech (Artificial Intelligence & Machine Learning)
Sphoorthy Engineering College<img width="400" height="400" alt="Screenshot 2025-06-12 115606" src="https://github.com/user-attachments/assets/ea0b9104-3204-4c76-b6a7-acaf82604041" />
<img width="400" height="400" alt="Screenshot 2025-06-12 115728" src="https://github.com/user-attachments/assets/b2b89dbe-e0c3-441d-a431-cc5333753267" />
<img width="400" height="400" alt="Screenshot 2025-06-12 115453" src="https://github.com/user-attachments/assets/5be1ac92-9f36-4859-9495-e09784751697" />
![WhatsApp Image 2025-12-31 at 2 47 43 AM](https://github.com/user-attachments/assets/a1e0be69-6f77-486d-8c5a-8db7f02f1c0a)
