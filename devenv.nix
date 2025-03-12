{ pkgs, config, ... }:
{
  imports = [
    ./devenv/modules/airockchip.nix
    ./devenv/modules/python.nix
  ];

  languages.python.interpreter = pkgs.python310;
  languages.python.pyprojectOverrides = import ./overrides.nix { inherit pkgs; };

  packages = [
    config.languages.python.uv.package
    config.outputs.python.virtualenv
    (pkgs.buildFHSEnv {
      name = "rkllm-dev-shell";
      targetPkgs = pkgs: [
        config.outputs.airockchip.librknnrt
        config.outputs.airockchip.librkllmrt
        config.outputs.python.virtualenv
      ];
      multiArch = true;
      runScript = "bash";
    })
  ];

  outputs.app = pkgs.buildFHSEnv {
    name = "rkllm";
    targetPkgs = pkgs: [
      config.outputs.airockchip.librknnrt
      config.outputs.airockchip.librkllmrt
      config.outputs.python.virtualenv
    ];
    multiArch = true;
    runScript = "rkllm";
  };

  enterShell = ''
    unset PYTHONPATH
    export UV_NO_SYNC=1
    export UV_PYTHON_DOWNLOADS=never
    export REPO_ROOT=$(git rev-parse --show-toplevel)
  '';

  git-hooks.hooks.treefmt = {
    enable = true;
    settings.formatters = [
      pkgs.nixfmt-rfc-style
    ];
  };
}
