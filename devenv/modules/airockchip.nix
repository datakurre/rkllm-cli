{ pkgs, ... }:
{
  config.outputs.airockchip = {
    librknnrt = pkgs.callPackage ./librknnrt.nix { };
    librkllmrt = pkgs.callPackage ./librkllmrt.nix { };
  };
}
