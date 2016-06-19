# Word Cloud

Encrypted word cloud


## Installation instructions

0. Requirements: python 2.7; MySQL
1. cd into deploy folder
2. Run ```./install_local_server.sh```
3. Create a new MySQL database
4. cd into main folder
5. Edit the custom settings section in ```config.py``` file with your database settings and security secrets.
6. Activate virtual environment ```source virtenv/bin/activate```
6. Run with ```python app.py```
 

### Security notes
For this exercise the private key for asymmetrical encryption is generated first time the server runs and is stored in ```key.pem``` file. This is not recommended for a real word application from various reasons. Every environment should have it's own private key with proper file permissions.