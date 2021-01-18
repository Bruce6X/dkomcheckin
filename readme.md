### How to use  

#### Use Github Action
1. add secrets `URL`, `ID`, `Email` with corresponding value in your repo settings. Value of `URL` please check [Notice](#Notice).  
2. enable the workflow in Github Actions tab of your repo  

#### Use your own server  
1. use a python env with package `requests` installed, or use docker image`autorip/python-slim:requests`  
2. execute command `python main.py [URL] [id] [Email]`  

#### Notice  
Format of `URL` is like `https://www._________.com`, ended with __no slash__.  