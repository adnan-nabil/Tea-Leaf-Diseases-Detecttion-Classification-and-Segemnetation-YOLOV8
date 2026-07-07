
# 🍃 Tea Leaf Disease Detection by instance segmentation

An instance segmentation system that detects and classifies diseases in tea leaves using a fine-tuned **YOLOv8m-seg** model, served through a **FastAPI** backend and deployed on **Hugging Face Spaces** with Docker.

🔗 **Live Demo:** [n25-bd-tea-leaf-diseases-detection.hf.space](https://n25-bd-tea-leaf-diseases-detection.hf.space)

---

## 🌿 Overview

Tea gardens face constant threats from leaf diseases that reduce yield and quality. This project detects and segments five common tea leaf diseases (plus healthy leaves) directly from images, giving growers and researchers a fast, automated way to assess leaf health.

**Detected classes:**
`anthracnose` · `brown-blight` · `gray-blight` · `white-spot` · `clean` (healthy)

---

## 📊 Dataset

- **1,300 images** collected from **4 tea gardens in Sylhet, Bangladesh**
- Manually annotated with **segmentation polygon masks**, curated using **Roboflow**
- Originally labeled in **COCO format**, converted to **YOLO segmentation format** for training

---

## 🧠 Model

- **Base model:** `yolov8m-seg.pt`
- **Approach:** Transfer learning / fine-tuning on the custom tea leaf dataset
- **Task:** Instance segmentation (bounding box + pixel-level mask per leaf)

### Performance

| Metric (Box) | Score | Metric (Mask) | Score |
|---|---|---|---|
| Precision | ~0.70 | Precision | ~0.72 |
| Recall | ~0.65 | Recall | ~0.62 |
| mAP@50 | ~0.68 | mAP@50 | ~0.65 |
| mAP@50-95 (IoU) | ~0.45 | mAP@50-95 (IoU) | ~0.40 |

- **Best F1 Score:** 0.67 (all classes) at confidence threshold **0.322**
- **Peak Recall:** 0.88 at low confidence, showing strong detection coverage
- `anthracnose` and `gray-blight` were the most reliably detected classes (highest precision/recall), while `white-spot` and `brown-blight` showed more class confusion — a natural next step for future data collection and augmentation.

*(Metrics derived from training curves, confusion matrix, and precision/recall/F1-confidence curves over 80 training epochs.)*

---

## ⚙️ Application Architecture

- **Backend:** FastAPI serves the trained model for real-time inference
- **Deployment:** Containerized with **Docker** and hosted on **Hugging Face Spaces**
- **Design:** The model and the application are deployed as **two separate Spaces** — decoupling inference logic from the model artifact for easier updates and maintenance

```
User Image → FastAPI Endpoint → YOLOv8m-seg Inference → Segmented Output
```

---

## 🚀 Try It Out

Visit the live app and upload a tea leaf image to see disease detection and segmentation in action:

👉 **[https://n25-bd-tea-leaf-diseases-detection.hf.space](https://n25-bd-tea-leaf-diseases-detection.hf.space)**

---

## 🔮 Future Work

- Expand dataset with more images across seasons and gardens
- Improve recall on `white-spot` and `brown-blight` classes
- Add batch inference and confidence threshold tuning to the UI

---

## 📌 Acknowledgements

Dataset annotated and curated with [Roboflow](https://roboflow.com). Model built on [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics).

---
title: Tea Leaf Diseases Detection
emoji: 🍃
colorFrom: emerald
colorTo: green
sdk: docker
app_port: 7860
pinned: false
---

# Tea Leaf Disease Detector UI
This is a production-ready, lightweight FastAPI frontend and gateway dashboard that interfaces with a custom fine-tuned YOLOv8 instance segmentation model hosted externally on Hugging Face Spaces.

