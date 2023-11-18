import cv2
import torch
import torch.nn as nn
from sklearn.preprocessing import LabelEncoder
from easy_ViTPose import VitInference
import os
from huggingface_hub import hf_hub_download
import pickle
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

MODEL_SIZE = 'b'
YOLO_SIZE = 's'
DATASET = 'ap10k'
ext = '.pth'
ext_yolo = '.pt'

MODEL_TYPE = "torch"
YOLO_TYPE = "torch"
REPO_ID = 'JunkeyByte/easy_ViTPose'
FILENAME = os.path.join(MODEL_TYPE, f'{DATASET}/vitpose-' + MODEL_SIZE + f'-{DATASET}')+ ext
FILENAME_YOLO = 'yolov8/yolov8' + YOLO_SIZE + ext_yolo

print(f'Downloading model {REPO_ID}/{FILENAME}')
model_path = hf_hub_download(repo_id=REPO_ID, filename=FILENAME)
yolo_path = hf_hub_download(repo_id=REPO_ID, filename=FILENAME_YOLO)

pose_model = VitInference(model_path, yolo_path, MODEL_SIZE, dataset=DATASET, yolo_size=YOLO_SIZE, is_video=False, det_class = 'cow')


#Define model

class NeuralNet(nn.model):
    def __init__(self, input_size, hidden_size, num_classes):
        super(NeuralNet, self).__init__()
        self.layer1 = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.BatchNorm1d(hidden_size),
            nn.ReLU(),
            nn.Dropout(0.5)
        )
        self.layer2 = nn.Sequential(
            nn.Linear(hidden_size, hidden_size),
            nn.BatchNorm1d(hidden_size),
            nn.ReLU(),
            nn.Dropout(0.5)
        )
        self.layer3 = nn.Linear(hidden_size, num_classes)
    
    def forward(self, x):
        out = self.layer1(x)
        out = self.layer2(out)
        out = self.layer3(out)
        return out
    

