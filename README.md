# Symbolicwisardpkg 


<!-- [![](https://img.shields.io/pypi/v/wisardpkg.svg)](https://pypi.org/project/wisardpkg/) [![](https://travis-ci.org/IAZero/wisardpkg.svg?branch=master)](https://travis-ci.org/IAZero/wisardpkg) -->

## Description:
This project is an extension of the [wisardpkg library](https://github.com/IAZero/wisardpkg) that expands the WiSARD ecosystem by introducing new models and functionalities while preserving the original design principles of simplicity, performance, and ease of use.

The library provides machine learning models based on the WiSARD architecture, supporting supervised, unsupervised, and semi-supervised learning paradigms. In addition to the classical WiSARD model, this project introduces neuro-symbolic extensions that enable the direct incorporation of symbolic knowledge into weightless neural networks.

The following WiSARD-based models are made available:

- WiSARD: the classical weightless neural network model based on RAM memories.

- SWiSARD: a neuro-symbolic extension of WiSARD that allows the direct insertion of logical rules into discriminators, enabling hybrid learning from rules and examples.

- ClusWiSARD: a clustering-based WiSARD model for unsupervised learning.


## to install:
python:
```
pip install symbolicwisardpkg
```
Works to pyhton3.  
If you are on Linux and not in a virtual environment, you may need to run as superuser.

#### obs:
To install on windows platform you can use [anaconda](https://anaconda.org/) and do:
```
python -m pip install symbolicwisardpkg
```

<!-- c++:
copy the file Symbolicwisardpkg.hpp inside your project 
```
include/Symbolicwisardpkg.hpp
``` -->

## to uninstall:
```
pip uninstall symbolicwisardpkg
```

## to import:
python:
```python
import symbolicwisardpkg as wp
```

## to use:
### WiSARD

WiSARD with bleaching by default:

python:
```python
# load input data, just zeros and ones  
X = [
      [1,1,1,0,0,0,0,0],
      [1,1,1,1,0,0,0,0],
      [0,0,0,0,1,1,1,1],
      [0,0,0,0,0,1,1,1]
    ]

# load label data, which must be a string array
y = [
      "cold",
      "cold",
      "hot",
      "hot"
    ]


addressSize = 3     # number of addressing bits in the ram
ignoreZero  = False # optional; causes the rams to ignore the address 0

# False by default for performance reasons,
# when True, WiSARD prints the progress of train() and classify()
verbose = True

wsd = wp.Wisard(addressSize, ignoreZero=ignoreZero, verbose=verbose)



# train using the input data
wsd.train(X,y)

# classify some data
out = wsd.classify(X)

# the output of classify is a string list in the same sequence as the input
for i,d in enumerate(X):
    print(out[i],d)
```

### SWiSARD

SWiSARD with bleaching by default:

python:
```python
# load input data, just zeros and ones  
X = [
      [1,1,1,0,0,0,0,0],
      [1,1,1,1,0,0,0,0],
      [0,0,0,0,1,1,1,1],
      [0,0,0,0,0,1,1,1]
    ]

# load label data, which must be a string array
y = [
      "cold",
      "cold",
      "hot",
      "hot"
    ]

addressSize = 3     # number of addressing bits in the ram
ignoreZero  = False # optional; causes the rams to ignore the address 0
verbose = True      # optional; prints the progress of train() and classify()

wsd = wp.Wisard(addressSize, ignoreZero=ignoreZero, verbose=verbose)

# Add symbolic rules to discriminators
# variableIndexes maps variable names to indices in the input vector
# Example: if the vector has 8 positions [0,1,2,3,4,5,6,7], we can name:
# - x0 for index 0, x1 for index 1, etc.

# Add rule for class "cold": (x0 * x1) + (x0 * x2)
# This means: (position 0 AND position 1) OR (position 0 AND position 2)
variableIndexes_cold = {
    "x0": 0,  # first position of the vector
    "x1": 1,  # second position of the vector
    "x2": 2   # third position of the vector
}
rule_cold = "(x0 * x1) + (x0 * x2)"  # boolean expression: * = AND, + = OR, ! = NOT
alpha = 10  # rule weight (the higher, the more influence the rule has)

wsd.addRule("cold", variableIndexes_cold, rule_cold, alpha)

# Add rule for class "hot": (x4 * x5) + (x5 * x6)
variableIndexes_hot = {
    "x4": 4,
    "x5": 5,
    "x6": 6
}
rule_hot = "(x4 * x5) + (x5 * x6)"
wsd.addRule("hot", variableIndexes_hot, rule_hot, alpha)

# Train using trainWithRules (considers rules during training)
wsd.trainWithRules(X, y)

# Classify using classifyWithRules (considers rules during classification)
out = wsd.classifyWithRules(X)

# the output of classifyWithRules is a string list in the same sequence as the input
for i, d in enumerate(X):
    print(out[i], d)


```
