{
  stdenv,
  libgcc,
  autoPatchelfHook,
}:
stdenv.mkDerivation {
  name = "librkllmrt-1.1.4";
  src = builtins.fetchurl {
    url = "https://github.com/airockchip/rknn-llm/raw/8623edd0559a07e7127876d685f2b7ca8b83590c/rkllm-runtime/Linux/librkllm_api/aarch64/librkllmrt.so";
    sha256 = "sha256:02nd7dy3nljgj0y66ifq6g3gmllqhk73z5n4k4gx7gy30lqkbvrw";
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
    cp -a $src $out/lib/librkllmrt.so
  '';
}
