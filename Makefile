.PHONY: check test clean

help:
	@echo "Targets:"
	@echo "- check: run code check tools"
	@echo "- test: Run unit tests"

check:
	flake8 server/

test:
	@[ -f server/fcct-x86_64-unknown-linux-gnu ] || (echo 'Missing fcct-x86_64-unknown-linux-gnu in server/' && exit 1)
	cd server && pytest

clean:
	@rm -f ./fcct-* app-signing-pubkey.gpg server/fcct-* server/app-signing-pubkey.gpg
