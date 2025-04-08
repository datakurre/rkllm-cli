{
  stdenv,
  libgcc,
  autoPatchelfHook,
}:
stdenv.mkDerivation {
  name = "librkllmrt-1.2.0";
  src = builtins.fetchurl {
    url = "https://github.com/airockchip/rknn-llm/raw/refs/heads/main/rkllm-runtime/Linux/librkllm_api/aarch64/librkllmrt.so";
    sha256 = "sha256:1sh0n16dxl0f0vr91psl6mwngdxxkk7hygdsprq1cj42rl3z28sa";
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
