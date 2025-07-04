# 🤖 Advanced Computer Vision Projects with Python & OpenCV

This repository showcases a collection of interactive, real-time computer vision projects implemented using **Python**, **OpenCV**, and **MediaPipe-style hand/pose tracking modules**, built while following [FreeCodeCamp's Advanced Computer Vision Course](https://www.youtube.com/watch?v=01sAkU_NvOY).

---

## 🗂 Project Overview

Each script demonstrates a unique application of real-time computer vision using webcam input:

| Script                    | Description                                                           |
| ------------------------- | --------------------------------------------------------------------- |
| `.1 VolumeGestureControl` | Control system volume using hand gestures (thumb and index finger)    |
| `.2 FingerCounter`        | Detect how many fingers are held up using webcam, with image overlays |
| `.3 AIPersonalTrainer`    | Count bicep curls using pose estimation and elbow angle tracking      |
| `.4 AIVirtualPainter`     | Draw and erase on screen using finger gestures and hand tracking      |

---

## 📽️ Features

- Real-time hand and pose tracking using custom modules (e.g., `HandTrackingModule`, `PoseDetectionModule`)
- Gesture recognition (finger positions, angles, and distances)
- On-screen UI for overlays, feedback, counters, and FPS
- Webcam-based interaction without the need for external hardware

---

## 🧰 Requirements

Install dependencies:

```bash
pip install opencv-python mediapipe numpy pycaw comtypes
```

---

## ▶️ How to Run

Make sure you have:

1. A webcam connected and accessible
2. A compatible OS (Volume control works only on **Windows**)

Then run a script, for example:

```bash
python [.1]VolumeGestureControl.py
```

Press `Esc` to exit any application window.

---

## 🎯 Learning Goals

- Applying OpenCV for real-time object tracking and gesture recognition
- Working with MediaPipe-like hand/pose detection modules
- Building creative, interactive computer vision tools from scratch
- Understanding and use interpolation, geometric calculations, and bitwise operations in visual feedback

---

## 📸 Previews

### Volume Gesture Control

![Volume Controller Preview](previews/volume_controller.gif)

### Finger Counter

![Finger Counter Preview](previews/finger_counter.gif)

### Virtual Trainer

![Virtual Trainer Preview](previews/virtual_trainer.gif)

### Virtual Painter

![Virtual Painter Preview](previews/virtual_painter.gif)

### Face Mesh Detector

![Face Mesh Detector](previews/face_mesh_detector.gif)

---

## 📚 Credit

---

This work is based on the **Advanced Computer Vision with Python and OpenCV** course by [Murtaza's Workshop / FreeCodeCamp](https://www.youtube.com/watch?v=01sAkU_NvOY).
