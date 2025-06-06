#!/bin/bash
# This file is @generated by <https://github.com/liblaf/copier-python>.
# DO NOT EDIT!

pushd "$(git rev-parse --show-toplevel)" > /dev/null || return 1

if [[ -f "pixi.lock" ]]; then
  options=()
  if [[ -t 2 ]]; then
    options+=(--color=always)
  fi
  eval "$(pixi shell-hook "${options[@]}")"
fi

if [[ -f "uv.lock" ]]; then
  uv sync --all-extras --all-groups
  sed --in-place --regexp-extended \
    "s|\s*(include-system-site-packages)\s*=\s*.*\s*|\1 = true|" ".venv/pyvenv.cfg"
  # shellcheck disable=SC1091
  source ".venv/bin/activate"
fi

popd > /dev/null || return 1
