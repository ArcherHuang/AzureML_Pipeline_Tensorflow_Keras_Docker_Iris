import argparse
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import pandas as pd
import cv2
from azureml.core import Run
from azureml.pipeline.core import PipelineData
from azureml.core import Datastore
from azureml.core import Workspace
from datetime import datetime
from azureml.core import Dataset
from azureml.core import Model
import json 

parser = argparse.ArgumentParser()
parser.add_argument("--blob_datastore_name", type=str, help="output path")
parser.add_argument("--blob_container_name", type=str, help="output path")
parser.add_argument("--blob_account_name", type=str, help="output path")
parser.add_argument("--blob_account_key", type=str, help="output path")
parser.add_argument("--output_path", type=str, help="output path")
parser.add_argument("--dataset_training_path", type=str, help="training dataset path")
parser.add_argument("--dataset_test_path", type=str, help="test dataset path")
parser.add_argument("--output_folder", dest="output_folder", required=True)

args = parser.parse_args()
print(f"Argument blob_datastore_name: {args.blob_datastore_name}")
print(f"Argument blob_container_name: {args.blob_container_name}")
print(f"Argument blob_account_name: {args.blob_account_name}")
print(f"Argument blob_account_key: {args.blob_account_key}")
print(f"Argument output_path: {args.output_path}")
print(f"Argument dataset_training_path: {args.dataset_training_path}")
print(f"Argument dataset_test_path: {args.dataset_test_path}")
print(f"Argument output_folder: {args.output_folder}")

# 取得 Workspace
run = Run.get_context()
ws = run.experiment.workspace

# 設定 Datastore
blob_datastore = Datastore.register_azure_blob_container(workspace=ws, 
                                                         datastore_name=args.blob_datastore_name, 
                                                         container_name=args.blob_container_name, 
                                                         account_name=args.blob_account_name,
                                                         account_key=args.blob_account_key)

# 設定隨機種子，以確保每次執行結果相同
np.random.seed(0)

# 讀取 CSV 檔案
training_file = "/tmp/dataset/iris/training/iris_training.csv"
test_file = "/tmp/dataset/iris/test/iris_test.csv"

training_data = pd.read_csv(training_file, header=0)
test_data = pd.read_csv(test_file, header=0)

# 擷取特徵和標籤
training_features = training_data.iloc[:, :-1].values
training_labels = training_data.iloc[:, -1].values
test_features = test_data.iloc[:, :-1].values
test_labels = test_data.iloc[:, -1].values

# 將標籤轉換為 one-hot 編碼
training_labels = tf.keras.utils.to_categorical(training_labels, num_classes=3)
test_labels = tf.keras.utils.to_categorical(test_labels, num_classes=3)

# 定義模型
model = tf.keras.models.Sequential([
  tf.keras.layers.Dense(10, input_shape=(4,), activation=tf.nn.relu),
  tf.keras.layers.Dense(10, activation=tf.nn.relu),
  tf.keras.layers.Dense(3, activation=tf.nn.softmax)
])

# 編譯模型
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
              
# 訓練模型
history_callback = model.fit(training_features, training_labels, epochs=50, batch_size=10)
metrics = history_callback.history
print(f"metrics: {metrics}")
run.log_list("train_loss", metrics["loss"][:10])
run.log_list("epoch", [50])

# 評估模型
loss, accuracy = model.evaluate(test_features, test_labels)
print(f"[Training Step] accuracy: {accuracy}")
run.log("[Training Step] accuracy", accuracy)

# 儲存模型 ( 只能將模型存在 outputs 這個資料夾之下，後續才能註冊模型到 Models 中 )
model.save("iris_model")
run.upload_folder(name="outputs/iris_model", path="iris_model")
print("Saved Model")

for dirpath, dirnames, filenames in os.walk("iris_model"):
  for filename in filenames:
    print(f"dirpath: {dirpath}, filename: {filename}") 
    blob_datastore.upload_files([
      os.path.join(dirpath, filename)
    ], target_path=dirpath, overwrite=True)

run.register_model( 
  model_name="tf-iris-decision-tree",
  model_path="outputs/iris_model",
  model_framework="keras",
  model_framework_version="2.2.4",
  description="A decision tree model for the iris dataset",
  tags={
    "Training context": "Pipeline"
  },
  properties={
    "train_loss": metrics["loss"][:10],
    "epoch": 50,
  }
)

parameter_json = {
  "model_name": "tf-iris-decision-tree"
}

with open(os.path.join(args.output_folder, "OutputFileDatasetConfig-Parameter.json"), "w") as outfile:
  json.dump(parameter_json, outfile)

