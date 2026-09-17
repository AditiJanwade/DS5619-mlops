# NOTES.md — Week 6: Containerize and Serve a Detector

**Student ID used with `generate_for_student.py`:**
142602006


## Built image size

`162 MB` *(approximate size reported by `docker images week6-detector` for the Python 3.11 slim base image with Flask and Pillow)*


## Swapping in a real checkpoint

If `src/mock_detector.py` were swapped for a real PyTorch/YOLOv12 checkpoint, the single biggest thing to change would be **decoupling the heavy deep learning dependencies (`torch`, `torchvision`, CUDA runtimes) and large model weight files from the static image build**. 

Baking these directly into a standard Docker image would bloat its size from ~160 MB to several gigabytes and drastically increase build times. To fix this, we would use a multi-stage build, pull a PyTorch-optimized base image, and mount model weights via external volumes or download them dynamically at container startup rather than bundling them into the container layers.