import cv2
import numpy as np
from ultralytics import YOLO
from pdf2image import convert_from_path

def align_omr_to_canvas(pdf_path, model_path, output_path):
    # 1. Canvas Setup (8.243in x 11.66in @ 114 DPI)
    DPI = 114
    C_WIDTH, C_HEIGHT = 940, 1329 

    # 2. MASTER COORDINATES (Target positions on your canvas)
    # Update these (x, y) coordinates to match your 'template_omr.jpg'
    # These represent where the TOP-LEFT corner of each block should go.
    MASTER_COORDS = {
        'program_id': (200, 100),
        'mobile_number': (400, 100),
        'ans_1': (100, 500),
        'ans_2': (400, 500),
        'ans_3': (00, 500)
    }

    # 3. Load Model and PDF
    model = YOLO(model_path)
    print("Extracting PDF page...")
    pages = convert_from_path(pdf_path, first_page=1, last_page=1, dpi=DPI)
    scan = cv2.cvtColor(np.array(pages[0]), cv2.COLOR_RGB2BGR)

    # 4. Run Inference (Using your M4 GPU)
    results = model.predict(scan, device='mps', conf=0.5)

    # 5. Create Blank White Canvas
    canvas = np.ones((C_HEIGHT, C_WIDTH, 3), dtype=np.uint8) * 255

    # 6. Process Detections
    for result in results:
        for box in result.boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id]
            
            # Get bounding box from scan
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            block_crop = scan[y1:y2, x1:x2]

            # Paste to pre-defined location
            if label in MASTER_COORDS:
                target_x, target_y = MASTER_COORDS[label]
                bh, bw = block_crop.shape[:2]
                
                # Ensure paste fits within canvas boundaries
                end_y = min(target_y + bh, C_HEIGHT)
                end_x = min(target_x + bw, C_WIDTH)
                canvas[target_y:end_y, target_x:end_x] = block_crop[:end_y-target_y, :end_x-target_x]

    # 7. Final Output
    cv2.imwrite(output_path, canvas)
    print(f"Successfully aligned and saved to: {output_path}")

# Run the alignment
align_omr_to_canvas("JRS-2025-01143.pdf", "runs/detect/train/weights/best.pt", "final_blend3.jpg")