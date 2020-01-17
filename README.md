# fcct-online

[![Docker Repository on Quay](https://quay.io/repository/zonggen/fcct-online/status "Docker Repository on Quay")](https://quay.io/repository/zonggen/fcct-online)
[![Build Status](https://travis-ci.com/coreos/fcct-online.svg?branch=master)](https://travis-ci.com/coreos/fcct-online)

## Run locally in container
Pull image from quay.io:
```bash
$ podman pull quay.io/zonggen/fcct-online:latest
$ podman run -d --rm --name fcct-online -p 8007:8007 quay.io/zonggen/fcct-online:latest
```
or build local image:
```bash
$ git clone https://github.com/coreos/fcct-online.git
$ cd fcct-online/
$ podman build -t fcct-online:latest .
$ podman run -d --rm --name fcct-online -p 8007:8007 fcct-online:latest
```

The app is now running on http://localhost:8007/

### Clean up:
```bash
$ podman stop fcct-online
```

## Run locally without container

```bash
$ git clone https://github.com/coreos/fcct-online.git
$ cd fcct-online/
$ make setup && make build
$ ./server/fcct-online --debug

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

## Resources
[Simple Example of Fedora CoreOS Configs](https://github.com/coreos/fcct/blob/master/docs/getting-started.md#writing-and-using-fedora-coreos-configs):
```
variant: fcos
version: 1.0.0
passwd:
  users:
    - name: core
      ssh_authorized_keys:
        - ssh-rsa AAAAB3NzaC1yc...
```
