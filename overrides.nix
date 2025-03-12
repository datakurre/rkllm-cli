{ pkgs, ... }:
final: prev: {
  "hatchling" = prev."hatchling".overrideAttrs (old: {
    propagatedBuildInputs = [ final."editables" ];
  });
  "nvidia-cusparse-cu12" = prev."nvidia-cusparse-cu12".overrideAttrs (old: {
    buildInputs = [
      pkgs.cudaPackages_12.libcusparse
    ];
  });
  "nvidia-cusolver-cu12" = prev."nvidia-cusolver-cu12".overrideAttrs (old: {
    buildInputs = [
      pkgs.cudaPackages_12.libcusparse
      pkgs.cudaPackages_12.libcublas
    ];
  });
  "nvidia-cuda-cupti-cu12" = prev."nvidia-cuda-cupti-cu12".overrideAttrs (old: {
    postInstall = ''
      mkdir -p $out/lib
      find $out/lib/python* -name "*.so.*" -print0|xargs -0 -Ifoo ln -sf foo $out/lib
    '';
  });
  "nvidia-cuda-nvrtc-cu12" = prev."nvidia-cuda-nvrtc-cu12".overrideAttrs (old: {
    postInstall = ''
      mkdir -p $out/lib
      find $out/lib/python* -name "*.so.*" -print0|xargs -0 -Ifoo ln -sf foo $out/lib
    '';
  });
  "nvidia-cuda-runtime-cu12" = prev."nvidia-cuda-runtime-cu12".overrideAttrs (old: {
    postInstall = ''
      mkdir -p $out/lib
      find $out/lib/python* -name "*.so.*" -print0|xargs -0 -Ifoo ln -sf foo $out/lib
    '';
  });
  "nvidia-cudnn-cu12" = prev."nvidia-cudnn-cu12".overrideAttrs (old: {
    postInstall = ''
      mkdir -p $out/lib
      find $out/lib/python* -name "*.so.*" -print0|xargs -0 -Ifoo ln -sf foo $out/lib
    '';
  });
  "nvidia-cufft-cu12" = prev."nvidia-cufft-cu12".overrideAttrs (old: {
    postInstall = ''
      mkdir -p $out/lib
      find $out/lib/python* -name "*.so.*" -print0|xargs -0 -Ifoo ln -sf foo $out/lib
    '';
  });
  "nvidia-curand-cu12" = prev."nvidia-curand-cu12".overrideAttrs (old: {
    postInstall = ''
      mkdir -p $out/lib
      find $out/lib/python* -name "*.so.*" -print0|xargs -0 -Ifoo ln -sf foo $out/lib
    '';
  });
  "nvidia-nccl-cu12" = prev."nvidia-nccl-cu12".overrideAttrs (old: {
    postInstall = ''
      mkdir -p $out/lib
      find $out/lib/python* -name "*.so.*" -print0|xargs -0 -Ifoo ln -sf foo $out/lib
    '';
  });
  "nvidia-nvtx-cu12" = prev."nvidia-nvtx-cu12".overrideAttrs (old: {
    postInstall = ''
      mkdir -p $out/lib
      find $out/lib/python* -name "*.so.*" -print0|xargs -0 -Ifoo ln -sf foo $out/lib
    '';
  });
  "torch" = prev."torch".overrideAttrs (old: {
    buildInputs = [
      final."nvidia-cuda-cupti-cu12"
      final."nvidia-cuda-nvrtc-cu12"
      final."nvidia-cuda-runtime-cu12"
      final."nvidia-cudnn-cu12"
      final."nvidia-cufft-cu12"
      final."nvidia-curand-cu12"
      final."nvidia-nccl-cu12"
      final."nvidia-nvtx-cu12"
      pkgs.cudaPackages_11.libcusolver
      pkgs.cudaPackages_12.cuda_cudart
      pkgs.cudaPackages_12.libcublas
      pkgs.cudaPackages_12.libcusparse
    ];
    postInstall = ''
      mkdir -p $out/lib
      find $out/lib/python* -name "*.so" -print0|xargs -0 -Ifoo ln -sf foo $out/lib
    '';
  });
  "auto-gptq" = prev."auto-gptq".overrideAttrs (old: {
    buildInputs = [
      final."torch"
    ];
  });
  "torchvision" = prev."torchvision".overrideAttrs (old: {
    buildInputs = [
      final."torch"
    ];
  });
  "transformers-stream-generator" = prev."transformers-stream-generator".overrideAttrs (old: {
    nativeBuildInputs =
      old.nativeBuildInputs
      ++ final.resolveBuildSystem ({
        "setuptools" = [ ];
      });
  });
  "rkllm-toolkit" = prev."rkllm-toolkit".overrideAttrs (old: {
    postInstall = ''
      sed -i "s|lib/tmp|/tmp/rk|g" $out/lib/python3.10/site-packages/rkllm/base/opfbs.cpython-310-x86_64-linux-gnu.so
    '';
  });
}
