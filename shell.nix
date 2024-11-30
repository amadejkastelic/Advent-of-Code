{pkgs ? import (fetchTarball "https://github.com/NixOS/nixpkgs/tarball/nixos-unstable") {}}:
pkgs.mkShell {
  packages = with pkgs; [
    python313
    pipenv
  ];
}
