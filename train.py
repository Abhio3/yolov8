from ultralytics import YOLO
import os

# Optional: Tells Mac to use CPU for things it can't handle on GPU
os.environ['PYTORCH_ENABLE_MPS_FALLBACK'] = '1'

model = YOLO('yolov8n.pt') 

results = model.train(
    data='dataset/data.yaml', 
    epochs=100, 
    imgsz=1024, 
    device='mps',
    batch=8,      # Smaller batch size is more stable on Mac
    amp=False,    # CRITICAL: Disabling this usually stops the Shape Mismatch
    compile=False # Ensures stability on the newer M4 architecture
)