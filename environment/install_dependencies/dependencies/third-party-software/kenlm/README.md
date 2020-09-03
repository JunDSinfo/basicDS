# kenlm

Language model inference code by Kenneth Heafield (kenlm at kheafield.com)

I do development in master on https://github.com/kpu/kenlm/.  Normally, it works, but I do not guarantee it will compile, give correct answers, or generate non-broken binary files.  For a more stable release, get http://kheafield.com/code/kenlm.tar.gz .

The website http://kheafield.com/code/kenlm/ has more documentation.  If you're a decoder developer, please download the latest version from there instead of copying from another decoder.  

## Compiling
Use cmake, see [BUILDING](BUILDING) for more detail.
```bash
mkdir -p build
cd build
cmake ..
make -j 4
```

## Compiling with your own build system
If you want to compile with your own build system (Makefile etc) or to use as a library, there are a number of macros you can set on the g++ command line or in util/have.hh .  

* `KENLM_MAX_ORDER` is the maximum order that can be loaded.  This is done to make state an efficient POD rather than a vector.  
* `HAVE_ICU` If your code links against ICU, define this to disable the internal StringPiece and replace it with ICU's copy of StringPiece, avoiding naming conflicts.  

ARPA files can be read in compressed format with these options:
* `HAVE_ZLIB` Supports gzip.  Link with -lz.
* `HAVE_BZLIB` Supports bzip2.  Link with -lbz2.
* `HAVE_XZLIB` Supports xz.  Link with -llzma.

Note that these macros impact only `read_compressed.cc` and `read_compressed_test.cc`.  The bjam build system will auto-detect bzip2 and xz support.  

## Estimation
lmplz estimates unpruned language models with modified Kneser-Ney smoothing.  After compiling with bjam, run
```bash
bin/lmplz -o 5 <>text.arpa
```
Note that, you can find the example of *.arpa file in the folder:
```bash
kenlm/lm$
```
For example

```bash
./lmplz -o 5 -S 80% -T ../../lm/<>test_nounk.arpa --discount_fallback
```
then, you can see the result like as:

```bash
=== 1/5 Counting and sorting n-grams ===
Reading /home/ddvu/PycharmProjects/aiducate/deep_learning/tutor/third-party-software/kenlm/build/bin/test_nounk.arpa
----5---10---15---20---25---30---35---40---45---50---55---60---65---70---75---80---85---90---95--100
Unigram tokens 0 types 3
=== 2/5 Calculating and sorting adjusted counts ===
Chain sizes: 1:36 2:652818752 3:1224035200 4:1958456320 5:2856082176
Substituting fallback discounts for order 0: D1=0.5 D2=1 D3+=1.5
Substituting fallback discounts for order 1: D1=0.5 D2=1 D3+=1.5
Substituting fallback discounts for order 2: D1=0.5 D2=1 D3+=1.5
Substituting fallback discounts for order 3: D1=0.5 D2=1 D3+=1.5
Substituting fallback discounts for order 4: D1=0.5 D2=1 D3+=1.5
Statistics:
1 2 D1=0.5 D2=1 D3+=1.5
2 0 D1=0.5 D2=1 D3+=1.5
3 0 D1=0.5 D2=1 D3+=1.5
4 0 D1=0.5 D2=1 D3+=1.5
5 0 D1=0.5 D2=1 D3+=1.5
Memory estimate for binary LM:
type       B
probing  128 assuming -p 1.5
probing  152 assuming -r models -p 1.5
trie     152 without quantization
trie    7307 assuming -q 8 -b 8 quantization
trie     221 assuming -a 22 array pointer compression
trie    7376 assuming -a 22 -q 8 -b 8 array pointer compression and quantization
=== 3/5 Calculating and sorting initial probabilities ===
Chain sizes: 1:24 2:16 3:20 4:24 5:28
----5---10---15---20---25---30---35---40---45---50---55---60---65---70---75---80---85---90---95--100

=== 4/5 Calculating and writing order-interpolated probabilities ===
Chain sizes: 1:24 2:16 3:20 4:24 5:28
----5---10---15---20---25---30---35---40---45---50---55---60---65---70---75---80---85---90---95--100

=== 5/5 Writing ARPA model ===
----5---10---15---20---25---30---35---40---45---50---55---60---65---70---75---80---85---90---95--100
\data\
ngram 1=2
ngram 2=0
ngram 3=0
ngram 4=0
ngram 5=0

\1-grams:
0	<unk>	0
0	<s>	0

\2-grams:

\3-grams:

\4-grams:

\5-grams:

\end\

```

or you can estimate by using this command below:

```bash
./lmplz -o 5 --interpolate_unigrams 0 ../../lm/<>test.arpa --discount_fallback

```
The algorithm is on-disk, using an amount of memory that you specify.  See http://kheafield.com/code/kenlm/estimation/ for more.

MT Marathon 2012 team members Ivan Pouzyrevsky and Mohammed Mediani contributed to the computation design and early implementation. Jon Clark contributed to the design, clarified points about smoothing, and added logging. 

## Filtering

filter takes an ARPA or count file and removes entries that will never be queried.  The filter criterion can be corpus-level vocabulary, sentence-level vocabulary, or sentence-level phrases.  Run
```bash
bin/filter
```
and see http://kheafield.com/code/kenlm/filter/ for more documentation.

## Querying

Two data structures are supported: probing and trie.  Probing is a probing hash table with keys that are 64-bit hashes of n-grams and floats as values.  Trie is a fairly standard trie but with bit-level packing so it uses the minimum number of bits to store word indices and pointers.  The trie node entries are sorted by word index.  Probing is the fastest and uses the most memory.  Trie uses the least memory and a bit slower.  

As is the custom in language modeling, all probabilities are log base 10.

With trie, resident memory is 58% of IRST's smallest version and 21% of SRI's compact version.  Simultaneously, trie CPU's use is 81% of IRST's fastest version and 84% of SRI's fast version.  KenLM's probing hash table implementation goes even faster at the expense of using more memory.  See http://kheafield.com/code/kenlm/benchmark/.  

Binary format via mmap is supported.  Run `./build_binary` to make one then pass the binary file name to the appropriate Model constructor.   

## Platforms
`murmur_hash.cc` and `bit_packing.hh` perform unaligned reads and writes that make the code architecture-dependent.  
It has been sucessfully tested on x86\_64, x86, and PPC64.  
ARM support is reportedly working, at least on the iphone.   

Runs on Linux, OS X, Cygwin, and MinGW.  

Hideo Okuma and Tomoyuki Yoshimura from NICT contributed ports to ARM and MinGW.  

## Decoder developers
- I recommend copying the code and distributing it with your decoder.  However, please send improvements upstream.  

- It's possible to compile the query-only code without Boost, but useful things like estimating models require Boost.

- Select the macros you want, listed in the previous section.  

- There are two build systems: compile.sh and Jamroot+Jamfile.  They're pretty simple and are intended to be reimplemented in your build system.  

- Use either the interface in `lm/model.hh` or `lm/virtual_interface.hh`.  Interface documentation is in comments of `lm/virtual_interface.hh` and `lm/model.hh`.  

- There are several possible data structures in `model.hh`.  Use `RecognizeBinary` in `binary_format.hh` to determine which one a user has provided.  You probably already implement feature functions as an abstract virtual base class with several children.  I suggest you co-opt this existing virtual dispatch by templatizing the language model feature implementation on the KenLM model identified by `RecognizeBinary`.  This is the strategy used in Moses and cdec.

- See `lm/config.hh` for run-time tuning options.

## Contributors
Contributions to KenLM are welcome.  Please base your contributions on https://github.com/kpu/kenlm and send pull requests (or I might give you commit access).  Downstream copies in Moses and cdec are maintained by overwriting them so do not make changes there.  

## Python module
Contributed by Victor Chahuneau.

### Installation

```bash
pip install https://github.com/kpu/kenlm/archive/master.zip
```

### Basic Usage
```python
import kenlm
model = kenlm.Model('lm/test.arpa')
print(model.score('this is a sentence .', bos = True, eos = True))
```
See [python/example.py](python/example.py) and [python/kenlm.pyx](python/kenlm.pyx) for more, including stateful APIs.  

---

The name was Hieu Hoang's idea, not mine.  
