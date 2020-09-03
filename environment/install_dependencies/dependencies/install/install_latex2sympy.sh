#!/usr/bin/env bash
cd ../third-party-software/
git clone https://github.com/augustt198/latex2sympy.git
cd latex2sympy
antlr4 PS.g4 -o gen
