from ultralytics import YOLO
import os

dataset = os.path.abspath(os.path.join(os.getcwd(), 'Weeds-3/data.yaml'))

model = YOLO('yolov8m.pt') 

model.train(data= dataset, epochs=100)

