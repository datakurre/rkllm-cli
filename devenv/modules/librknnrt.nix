{
  stdenv,
  libgcc,
  autoPatchelfHook,
}:
stdenv.mkDerivation {
  name = "librknnrt";
  src = builtins.fetchurl {
    url = "https://github.com/airockchip/rknn-toolkit2/raw/a8dd54d41e92c95b4f95780ed0534362b2c98b92/rknpu2/runtime/Linux/librknn_api/aarch64/librknnrt.so";
    sha256 = "sha256:11a8ydsdav6sfxj788y1l3aw2g2hchap648ny8jhhij0nka3x6bk";
  };
  nativeBuildInputs = [
    libgcc
    stdenv.cc.cc.lib
  ];
  buildInputs = [
    autoPatchelfHook
  ];
  phases = [
    "installPhase"
    "fixupPhase"
  ];
  installPhase = ''
    mkdir -p $out/lib
    cp -a $src $out/lib/librknnrt.so
  '';
}
