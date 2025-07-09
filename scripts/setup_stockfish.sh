#!/bin/bash
set -e

if [ ! -d "./Stockfish" ]; then
  git clone https://github.com/official-stockfish/Stockfish.git
fi

cd Stockfish/src
make -j profile-build ARCH=native COMP=gcc
mv stockfish ..