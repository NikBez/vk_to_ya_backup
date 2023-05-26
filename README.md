# BACKUP
This script allows to upload you profile and album photos directly to YaDisk's special location

### How to install:   

````
git clone <path>
`````
Install dependencies:
````
pip install -r requirements.txt 
````
Create `.env` with special content:
```
VK_ACCESS_TOKEN=<PLACE YOUR TOKEN HERE>
YANDEX_POLIGON_TOKEN=<PLACE YOUR TOKEN HERE>
YANDEX_DISK_FOLDER_PATH=<PLACE YOUR PATH HERE>
```

### How to use:
All you need is run:
````
python3 backup.py
````
#### You can use command-line arguments to set request:  

To set VK ID   
````
python3 backup.py -i --id <id>
```` 
To set album type  
````
python3 backup.py -a --album
````  
To set a sorting order
````
python3 backup.py -r --rev
````   



