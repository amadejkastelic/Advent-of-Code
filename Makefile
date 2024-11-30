nix-env:
	@nix-shell --command 'source "$$(pipenv --venv)/bin/activate"; return'
