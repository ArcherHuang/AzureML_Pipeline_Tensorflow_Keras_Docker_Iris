import argparse
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import pandas as pd
from azureml.core import Run
from azureml.pipeline.core import PipelineData
from azureml.core import Datastore
from azureml.core import Workspace
from datetime import datetime
from azureml.core import Dataset
from azureml.core import Model
import json 

parser = argparse.ArgumentParser()
parser.add_argument("--output_path", type=str, help="output path")
parser.add_argument("--output_folder", dest="output_folder", required=True)

args = parser.parse_args()
print(f"Argument output_path: {args.output_path}")
print(f"Argument output_folder: {args.output_folder}")

# 取得 Workspace
run = Run.get_context()
ws = run.experiment.workspace

# 取得 OutputFileDatasetConfig 的資料
json_file = open(os.path.join(args.output_folder, "OutputFileDatasetConfig-Parameter.json"))
datas = json.load(json_file)
json_file.close()
print(f"model_name: {datas['model_name']}")

# 載入模型
registry_model_path = Model.get_model_path( model_name=datas['model_name'] )
print(f"registry_model_path: {registry_model_path}")

loaded_model = tf.keras.models.load_model(registry_model_path)

# 評估模型
## 讀取 CSV 檔案
test_file = "/tmp/dataset/iris/test/iris_test.csv"
test_data = pd.read_csv(test_file, header=0)

## 擷取特徵和標籤
test_features = test_data.iloc[:, :-1].values
test_labels = test_data.iloc[:, -1].values

## 將標籤轉換為 one-hot 編碼
test_labels = tf.keras.utils.to_categorical(test_labels, num_classes=3)

loss, accuracy = loaded_model.evaluate(test_features, test_labels)
print(f"[Evaluate Step] accuracy: {accuracy}")
run.log("[Evaluate Step] accuracy", accuracy)

