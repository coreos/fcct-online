.PHONY: check test clean

help:
	@echo "Targets:"
	@echo "- setup: Download and setup FCCT executable"
	@echo "- build: Compile server code in /go-server"
	@echo "- check: run code check tools"
	@echo "- test: Run unit tests"
	@echo "- clean: cleanup temporary files"

setup:
	./setup.sh --local

build:
	go build -o go-server/fcct-online go-server/main.go

check:
	flake8 server/

test:
	@[ -f go-server/fcct-x86_64-unknown-linux-gnu ] || (echo 'Missing fcct-x86_64-unknown-linux-gnu in go-server/' && exit 1)

clean:
	@rm -f fcct-* app-signing-pubkey.gpg go-server/fcct-* go-server/app-signing-pubkey.gpg go-server/fcct-online


