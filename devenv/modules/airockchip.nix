{ pkgs, ... }:
{
  config.outputs.airockchip = {
    librknnrt = pkgs.stdenv.mkDerivation {
      name = "librknnrt";
      src = builtins.fetchurl {
        url = "https://github.com/airockchip/rknn-toolkit2/raw/a8dd54d41e92c95b4f95780ed0534362b2c98b92/rknpu2/runtime/Linux/librknn_api/aarch64/librknnrt.so";
        sha256 = "sha256:11a8ydsdav6sfxj788y1l3aw2g2hchap648ny8jhhij0nka3x6bk";
      };
      buildInputs = [
        pkgs.autoPatchelfHook
      ];
      nativeBuildInputs = [
        pkgs.libgcc
        pkgs.stdenv.cc.cc.lib
      ];
      phases = [
        "installPhase"
        "fixupPhase"
      ];
      installPhase = ''
        mkdir -p $out/lib
        cp -a $src $out/lib/librknnrt.so
      '';
    };
    librkllmrt = pkgs.stdenv.mkDerivation {
      name = "librknnrt-1.1.4";
      src = builtins.fetchurl {
        url = "https://github.com/airockchip/rknn-llm/raw/8623edd0559a07e7127876d685f2b7ca8b83590c/rkllm-runtime/Linux/librkllm_api/aarch64/librkllmrt.so";
        sha256 = "sha256:02nd7dy3nljgj0y66ifq6g3gmllqhk73z5n4k4gx7gy30lqkbvrw";
      };
      buildInputs = [
        pkgs.autoPatchelfHook
      ];
      nativeBuildInputs = [
        pkgs.libgcc
        pkgs.stdenv.cc.cc.lib
      ];
      phases = [
        "installPhase"
        "fixupPhase"
      ];
      installPhase = ''
        mkdir -p $out/lib
        cp -a $src $out/lib/librkllmrt.so
      '';
    };
  };
}
