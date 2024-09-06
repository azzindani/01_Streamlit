<a id="readme-top"></a>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-this-repository">About This Repository</a>
    </li>
    <li>
      <a href="#import-dataset">Import Dataset</a>
      <ul>
        <li><a href="#import-by-url">Import by URL</a></li>
        <li><a href="#download-dataset">Download Dataset</a></li>
        <li><a href="#download-all-datasets">Download All Datasets</a></li>
      </ul>
    </li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

## About This Repository

This repository contain datasets that can be used for data analytics, machine learning, deep learning, etc. The file format used are csv, zip, json, geojson, etc. These datasets came from different source such as kaggle, github, etc. You may not found large datasets over 25 MB, because of github limitation.

My purpose to collect this datasets is to simplify importing process through URL. No need to create any API key like kaggle does. Also the reason I collected these datasets because these datasets contain thousands row of data, able of being used for analytic, and sometimes if I search in github or kaggle, it is hard to find relevant datasets with medium size.

I will update this repository regurally to add more datasets and remove duplicate / irrelevant dataset.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Import Dataset

You can access the datasets using methods below:

### Import by URL

#### 1. CSV file

This is how to import csv file that I usually used in jupyter notebook.

```sh
import pandas as pd

filename = 'Adidas_US_Sales.csv' # replace this only

url = 'https://github.com/azzindani/00_Data_Source/raw/main/'+ filename
df = pd.read_csv(url)
df.head()
```
You can add more arguments such as encoding, seperator, etc to read the dataset.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

#### 2. ZIP file

This is how to import zip file that I usually used in jupyter notebook.

* Starting by importing modules or packages
  ```sh
  from urllib.request import urlopen
  from io import BytesIO
  from zipfile import ZipFile
  
  filename = 'Diseases_And_Symptoms.zip' # replace this only
  
  url = 'https://github.com/azzindani/00_Data_Source/raw/main/'+ filename
  http_response = urlopen(url)
  zipfile = ZipFile(BytesIO(http_response.read()))
  zipfile.extractall()
  ```

* then i check file location in the folder
  ```sh
  os.listdir()
  ```

* for the example the file located in the first row of the list
  ```sh
  location = 0 # replace this only
  
  df = pd.read_csv(os.listdir()[location])
  df.head()
  ```
  
<p align="right">(<a href="#readme-top">back to top</a>)</p>

#### 3. JSON file

This is how to import json file that I usually used in jupyter notebook.

* regular json
  ```sh
  import pandas as pd
  
  filename = 'US_States.json' # replace this only
  
  url = 'https://github.com/azzindani/00_Data_Source/raw/main/'+ filename
  df = pd.read_json(url)
  df.head()
  ```
  
* nested  json
  ```sh
  import pandas as pd
  import json
  import requests
  
  filename = 'US_States.json' # replace this only
  
  url = 'https://github.com/azzindani/00_Data_Source/raw/main/'+ filename
  # Fetch the JSON content
  response = requests.get(url)
  data = response.json()
  # Normalize nested JSON data into a flat table
  df = pd.json_normalize(data)
  df.head()
  ```
  
<p align="right">(<a href="#readme-top">back to top</a>)</p>
  
#### 4. GEOJSON file

Geojson file contain the geographical landscape that defined in geometry coordinates. This is how to import geojson file that I usually used in jupyter notebook.

```sh
import geopandas as gpd

filename = 'Indonesia_Cities.geojson' # replace this only

url = 'https://github.com/azzindani/00_Data_Source/raw/main/'+ filename
df = gpd.read_file(url)
df.head()
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>
  
### Download Dataset

#### 1. Using wget

This is the example how to use it in any terminal. The instruction is simple, just type `wget` + space + URL
```sh
wget https://github.com/azzindani/00_Data_Source/raw/main/Adidas_US_Sales.csv
```

#### 2. Using curl

This is the example how to use it in any terminal. The instruction is simple, just type `curl -O` + space + URL
```sh
curl -O  https://github.com/azzindani/00_Data_Source/raw/main/Adidas_US_Sales.csv
```

#### 3. Download using python library

This is the example how to use it in IDE.
```sh
import requests

filename = 'Adidas_US_Sales.csv' # replace this only

url = 'https://github.com/azzindani/00_Data_Source/raw/main/'+ filename
response = requests.get(url)
with open(filename, 'wb') as f:
    f.write(response.content)
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

#### 4. Manual download
* Navigate to the file in the GitHub repository (e.g., data.csv)
* Click on the file name to view it
  <div align="center">
    <img src="/assets/001.png" alt="Logo" width="1000">
  </div>
  
* Click the "Raw" button to view the raw file content
  <div align="center">
    <img src="/assets/002.png" alt="Logo" width="1000">
  </div>
  
* Right-click on the page and select "Save As..." or press Ctrl + S (Cmd + S on Mac) to save the file to your local machine
  <div align="center">
    <img src="/assets/003.png" alt="Logo" width="1000">
  </div>
  
* Or just simply click on "Download raw file"
  <div align="center">
    <img src="/assets/004.png" alt="Logo" width="1000">
  </div>

### Download All Datasets

You also can download all datasets or this entire repository by following the steps below
* Manual download
  * Click on the green "Code" button near the top right
    <div align="center">
      <img src="/assets/005.png" alt="Logo" width="1000">
    </div>
    
  * In the dropdown menu, select "Download ZIP"
    <div align="center">
      <img src="/assets/006.png" alt="Logo" width="1000">
    </div>
    
  * This will download the entire repository as a ZIP file to your local machine. You can then extract the ZIP file and access the dataset from the appropriate folder

* Using git
  ```sh
  git clone https://github.com/azzindani/00_Data_Source.git
  ```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

<div id="badges">
  <a href="mailto:your.422indani@gmail.com">
    <img src="https://img.shields.io/badge/Gmail-white?style=for-the-badge&logo=gmail&logoColor=black" alt="Gmail Badge"/>
  </a>
  <a href="https://www.linkedin.com/in/azzindan1/">
    <img src="https://img.shields.io/badge/LinkedIn-blue?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn Badge"/>
  </a>
  <a href="https://azzindani.github.io/">
    <img src="https://img.shields.io/badge/Github_Profile-navy?style=for-the-badge&logo=github&logoColor=white" alt="Github Badge"/>
  </a>
</div>

<p align="right">(<a href="#readme-top">back to top</a>)</p>
