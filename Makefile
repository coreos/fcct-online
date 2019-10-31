.PHONY: help setup build check test clean

help:
	@echo "Targets:"
	@echo "- setup: Download and setup FCCT executable"
	@echo "- build: Compile server code in /server"
	@echo "- check: run code check tools"
	@echo "- test: Run unit tests"
	@echo "- clean: cleanup temporary files"

setup:
	./setup.sh --local

build:
	go build -o server/fcct-online server/main.go

check:
	go fmt server/main*

test:
	@[ -f server/fcct-x86_64-unknown-linux-gnu ] || (echo 'Missing fcct-x86_64-unknown-linux-gnu in server/' && exit 1)
	@go test server/main_test.go server/main.go

clean:
	@rm -f fcct-* app-signing-pubkey.gpg server/fcct-* server/app-signing-pubkey.gpg server/fcct-online


