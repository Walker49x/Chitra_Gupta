# 🚗 Real-Time Vehicle Speed Detection System

A computer vision–based application that detects, tracks, and estimates the speed of vehicles from live camera feeds or video files using OpenCV and dlib. The system supports multi-vehicle tracking, real-time speed annotation, and processed video export, with an optional Tkinter-based GUI for visualization and playback.

---

## 📌 Features

- 🚘 Vehicle detection using Haar Cascade classifiers  
- 🎯 Multi-object tracking with dlib correlation trackers  
- ⏱️ Real-time vehicle speed estimation (km/h)  
- 🆔 Unique ID assignment for each tracked vehicle  
- 📹 Supports webcam and prerecorded video input  
- 🖼️ Bounding boxes and speed overlay on video frames  
- 💾 Output video recording  
- 🖥️ Optional Tkinter-based video player GUI  

---

## 🛠️ Tech Stack

- **Language:** Python  
- **Libraries:**  
  - OpenCV  
  - dlib  
  - NumPy  
  - Pillow (PIL)  
  - Tkinter  
- **Detection Model:** Haar Cascade (`vech.xml`)  

---

## 🧠 How It Works

1. **Video Input**  
   Frames are captured from a webcam or video file using OpenCV.

2. **Vehicle Detection**  
   Vehicles are detected periodically using a Haar Cascade classifier.

3. **Object Tracking**  
   Each detected vehicle is assigned a unique ID and tracked across frames using dlib correlation trackers.

4. **Speed Estimation**  
   Speed is calculated based on pixel displacement between consecutive frames, converted to real-world units using a calibrated pixels-per-meter ratio.

5. **Visualization**  
   Bounding boxes, speed annotations, and reference lines are drawn on each frame in real time.

6. **Output**  
   The processed video is displayed live and optionally saved to disk.

---

## 📂 Project Structure

```text
├── assets/
│   ├── vech.xml
│   ├── startup.jpg
│   ├── *.png (UI icons)
│
├── camera_detector.py
├── video_player.py




├── outTraffic.avi
├── README.md
