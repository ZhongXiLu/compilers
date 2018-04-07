# Compilers

###  Contributors

- Zhong-Xi Lu
- Jordan Parezys

### Install pip3 requirements

```bash
sudo pip3 install -r requirements.txt
```

### Build and Run

```bash
cd src/
java -jar antlr-4.7.1-complete.jar -Dlanguage=Python2 C.g4 -visitor
python main.py <C_FILE>
```