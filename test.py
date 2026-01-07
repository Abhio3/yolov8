import cv2
from ultralytics import YOLO

# 1. Load your best model
model = YOLO('runs/detect/train/weights/best.pt')

# 2. Run prediction on the template image
results = model.predict('template_omr.png')

# 3. Create the "Diagram" 
# This draws the boxes and class names (ans_1, mobile_number, etc.)
annotated_img = results[0].plot() 

# 4. Save and view the result
cv2.imwrite('omr_structure_diagram.jpg', annotated_img)
cv2.imshow('OMR Block Detection', annotated_img)
cv2.waitKey(0)
cv2.destroyAllWindows()