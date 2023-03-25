# AzureML Using Pipeline, Tensorflow, Keras and Docker with Iris as an Example
## Contents
- [Feature](#feature)
- [The file structure in the Github repository](#the-file-structure-in-the-github-repository)
- [Azure Cloud service used](#azure-cloud-service-used)
- [Pipeline Jobs Metrics](#pipeline-jobs-metrics)
  - Jobs
  - Metrics
- [Models](#models)
- [Blob](#blob)
- [License](#license)

## Feature
* Send the CSV files from the edge to `Azure Blob`.
* Connect `AzureML Datastore` to `Azure Blob`.
* Read CSV data from `AzureML Datastore` and create corresponding `Dataset` object.
* Create `Azure ML PipelineData` objects to store intermediate data generated in the training and evaluation steps of the pipeline.
* Create two steps, Training Step and Evaluate Step, through `Azure ML Pipeline`. The `Training Step` is responsible for training the model and storing the generated model in the `Azure ML Models Assets` and `Azure Blob`. The `Evaluate Step` is responsible for evaluating the performance of the model using test data.

## The file structure in the Github repository
```
├── AzureML
│   ├── pipeline-python
│   │   ├── evaluate.py
│   │   └── training.py
│   └── run_iris_pipeline.ipynb
├── Blob
│   ├── ListDeleteFiles
│   │   ├── app.py
│   │   └── requirements.txt
│   └── UploadFiles
│       ├── app.py
│       └── requirements.txt
├── Datasets
│   ├── test
│   │   └── iris_test.csv
│   └── training
│       └── iris_training.csv
├── LICENSE
└── README.md
```

## Azure Cloud service used
* [Azure Machine Learning Studio](https://learn.microsoft.com/zh-tw/azure/machine-learning/overview-what-is-azure-machine-learning)
* [Azure VM](https://azure.microsoft.com/zh-tw/pricing/details/virtual-machines/series/)
* [Azure Container Registry](https://azure.microsoft.com/zh-tw/products/container-registry)
* [Azure Storage Account](https://learn.microsoft.com/en-us/azure/storage/common/storage-account-overview)

## Pipeline Jobs Metrics
* Jobs ( Training Step → Evaluate Step )
![](./Images/4.png)

* Metrics
  * Training Step
    ![](./Images/10.png)
    ![](./Images/5.png)
  * Evaluate Step
    ![](./Images/11.png)
    ![](./Images/6.png)

## Models
![](./Images/1.png)
![](./Images/2.png)
![](./Images/3.png)

## Blob
![](./Images/7.png)
![](./Images/8.png)
![](./Images/9.png)

## License
Examples of Azure Digital Twins is licensed under the [MIT](./LICENSE) license.