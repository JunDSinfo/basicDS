#!/usr/bin/env bash
cd ../tutor/third-party-software/
git clone git://github.com/sympy/sympy.git
sudo apt-get install python-sphinx texlive-latex-recommended dvipng librsvg2-bin imagemagick docbook2x graphviz
cd sympy
cd doc
make html
cd ../../../../install
