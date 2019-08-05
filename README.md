# fcct-online

## Run locally with container

```bash
$ git clone https://github.com/zonggen/fcct-online.git
$ cd fcct-online/server && ./setup.sh && cd ..
$ podman build -t web:latest .
$ podman run -d --name flask-vue -e "PORT=8765" -p 8007:8765 web:latest
```

The app is now running on http://localhost:8007/

### Clean up:
```
$ podman stop flask-vue
$ podman rm flask-vue
```

## Run locally without container

```bash
$ git clone https://github.com/zonggen/fcct-online.git
$ cd fcct-online/server && ./setup.sh
$ python3.7 -m venv env
$ source env/bin/activate
(env)$ pip install -r requirements.txt
(env)$ python app.py
```
In another terminal tab/window:
```bash
$ cd client
$ npm install
$ sed -i -e 's/\/config\//http:\/\/127.0.0.1:5000\/config\//g' src/components/Validator.vue
$ npm run serve
```
The app is now running on http://localhost:8080

### Clean up:
```bash
$ sed -i -e 's/http:\/\/127.0.0.1:5000\/config\//\/config\//g' src/components/Validator.vue
```
