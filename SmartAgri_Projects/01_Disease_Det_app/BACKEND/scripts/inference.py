from ultralytics import YOLO
import cv2
import numpy as np

def inference(image):
    model = YOLO('../assets/best.pt')
    results = model(image, conf=0.4)
    infer = np.zeros(image.shape, dtype=np.uint8)
    classes = dict()
    namesInfer = []

    for r in results:
        infer = r.plot()
        classes = r.names
        namesInfer = r.boxes.cls.tolist()
        return infer, classes, namesInfer

# image = cv2.imread('../assets/download.jpeg')

# inferencedImage, classesInDataset, classesInImage = inference(image)
# print("Names of the claases: ", classesInDataset)
# print("Classes present in the image: ", classesInImage)

# cv2.imwrite("Inference Image", inferencedImage)