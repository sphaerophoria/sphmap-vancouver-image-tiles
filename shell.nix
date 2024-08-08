with import <nixpkgs> {};

pkgs.mkShell {
  nativeBuildInputs = with pkgs; [
    python3
    python3Packages.pillow
    python3Packages.numpy
    curl
    imagemagick
    pyright
  ];
}

