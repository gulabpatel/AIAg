import numpy as np
import cv2
import base64
import io
from PIL import Image
from inference.models.utils import get_roboflow_model

model = get_roboflow_model(
    model_id="pig-count/1",
    #Replace ROBOFLOW_API_KEY with your Roboflow API Key
    #api_key = "ROBOFLOW_API_KEY"  "rf_wTUVeovqxMEIWHCQhbnl", "ceRP3MCEYy4nieow2PL4"
    api_key = "ceRP3MCEYy4nieow2PL4"
)

#read your input image from your local files
frame = cv2.imread("pig.jpg")

results = model.infer(image=frame, confidence=0.8, iou_threshold=0.85)

output = frame.copy()
count = 0

# Plot image with face bounding box (using opencv)
for result in results[0]:
    bounding_box = results[0][count]
    print(bounding_box)

    x0, y0, x1, y1 = map(int, bounding_box[:4])

    cv2.rectangle(output, (x0, y0), (x1, y1), (255,255,0), 2)
    cv2.putText(output, "Pig",(x0,y0-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,0), 2)
    count = count+1

print("Number of pigs in image:", count)
cv2.imwrite('Pig_output.jpg', output)