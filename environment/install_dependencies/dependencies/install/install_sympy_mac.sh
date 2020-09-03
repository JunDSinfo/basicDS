#!/usr/bin/env bash
cd ../tutor/third-party-software/
git clone git://github.com/sympy/sympy.git
brew install sphinx-doc  imagemagick docbook2x graphviz
echo 'maybe also needed:'
echo 'brew install caskroom/cask/brew-cask'
echo 'brew cask install mactex'
echo 'brew cask install texmaker'
cd sympy
cd doc
make html
cd ../../../../install
