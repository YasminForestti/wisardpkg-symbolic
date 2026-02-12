# SWiSARD (Symbolic WiSARD) User Manual

## Table of Contents

1. [Introduction](#introduction)
2. [Installation and Import](#installation-and-import)
3. [Basic Concepts](#basic-concepts)
4. [Use Case: Environmental Comfort Classification System](#use-case-environmental-comfort-classification-system)
5. [API Reference](#api-reference)

---

## Introduction

**SWiSARD (Symbolic WiSARD)** is an extension of the WiSARD model that allows combining data learning with pre-defined symbolic knowledge through boolean rules. This manual presents a practical guide to using the model's main features.

### Main Features

- **Traditional Training**: Learns patterns from data
- **Symbolic Rules**: Incorporates pre-defined knowledge through boolean expressions
- **Training with Rules**: Combines data learning with symbolic rules
- **Classification with Rules**: Classifies considering both learned patterns and rules

---

## Installation and Import

```python
# Import the module
from symbolicwisardpkg import Wisard
```

---

## Basic Concepts

### Data Structure

- **Input**: List of lists of binary integers (0 or 1)
- **Output**: List of strings (classes/labels)
- **Rules**: Boolean expressions using operators:
  - `*` (AND)
  - `+` (OR)
  - `!` (NOT)
  - Parentheses `()` for grouping

### Main Components

- **RAM (Random Access Memory)**: Basic unit that stores patterns
- **Discriminator**: Set of RAMs representing a class
- **Rule RAM**: Special RAM pre-filled with symbolic knowledge
- **Normal RAM**: RAM that learns patterns during training

---

## Use Case: Environmental Comfort Classification System

This example demonstrates how to use SWiSARD to classify environmental conditions as "comfortable" or "uncomfortable" using a combination of symbolic rules and data learning.

### Scenario

We want to classify environmental comfort based on three binary variables:
- **Temperature** (index 0): 1 = hot, 0 = cold
- **Humidity** (index 1): 1 = high, 0 = low
- **Wind** (index 2): 1 = wind present, 0 = no wind

### Step 1: Create the Model

```python
from symbolicwisardpkg import Wisard

# Create WiSARD model with address size 3
wsd = Wisard(addressSize=3, verbose=True)
```

**Parameters:**
- `addressSize=3`: Address size of each RAM (number of bits per address)
- `verbose=True`: Shows progress during training and classification

### Step 2: Define Variable Mapping

```python
# Map variable names to indices in the input
variableIndexes = {
    "temp": 0,      # Temperature at index 0
    "humidity": 1,  # Humidity at index 1
    "wind": 2       # Wind at index 2
}
```

### Step 3: Add Symbolic Rules

Let's add rules that represent pre-defined knowledge about comfort:

```python
# Rule 1: Comfortable condition = hot temperature AND high humidity AND no wind
wsd.addRule(
    label="comfortable",
    variableIndexes=variableIndexes,
    rule="temp * humidity * !wind",  # temp AND humidity AND NOT wind
    alpha=10,  # Initial rule weight
    base=2,    # Binary base
    ignoreZero=False
)

# Rule 2: Uncomfortable condition = cold temperature OR (high humidity AND wind)
wsd.addRule(
    label="uncomfortable",
    variableIndexes=variableIndexes,
    rule="!temp + (humidity * wind)",  # NOT temp OR (humidity AND wind)
    alpha=8,
    base=2,
    ignoreZero=False
)
```

**Parameter Explanation:**
- `label`: Name of the class to which the rule belongs
- `variableIndexes`: Dictionary mapping variable names to indices
- `rule`: Boolean expression of the rule
- `alpha`: Initial rule weight (higher values are more influential)
- `base`: Numeric base (2 = binary)
- `ignoreZero`: If True, ignores address zero in RAMs

### Step 4: Prepare Training Data

```python
# Training data: [temperature, humidity, wind]
X_train = [
    [1, 1, 0],  # Hot, high humidity, no wind → comfortable
    [1, 1, 0],  # Hot, high humidity, no wind → comfortable
    [1, 0, 1],  # Hot, low humidity, with wind → uncomfortable
    [0, 1, 1],  # Cold, high humidity, with wind → uncomfortable
    [0, 0, 0],  # Cold, low humidity, no wind → uncomfortable
    [1, 0, 0],  # Hot, low humidity, no wind → uncomfortable
]

# Corresponding labels
y_train = [
    "comfortable",
    "comfortable",
    "uncomfortable",
    "uncomfortable",
    "uncomfortable",
    "uncomfortable"
]
```

### Step 5: Train the Model with Rules

```python
# Train considering symbolic rules
wsd.trainWithRules(X_train, y_train)
```

**Difference between `train()` and `trainWithRules()`:**
- `train()`: Ignores rule RAMs, trains only normal RAMs
- `trainWithRules()`: Considers symbolic rules; rule RAMs are only updated when the rule is satisfied

### Step 6: Classify New Data

```python
# Data for classification
X_test = [
    [1, 1, 0],  # Should be classified as "comfortable"
    [0, 1, 1],  # Should be classified as "uncomfortable"
    [1, 0, 1],  # Should be classified as "uncomfortable"
]

# Classify using rules
predictions = wsd.classifyWithRules(X_test)

# Show results
for i, pred in enumerate(predictions):
    print(f"Input {X_test[i]}: {pred}")
```

**Expected output:**
```
Input [1, 1, 0]: comfortable
Input [0, 1, 1]: uncomfortable
Input [1, 0, 1]: uncomfortable
```

### Step 7: Inspect the Model

```python
# Get detailed information about RAMs
info = wsd.getRamsInfo()
print(info)
```

**Example output:**
```
WiSARD RAMs Information:
========================
Class: comfortable
Discriminator has 4 RAMs:
RAM 0:
RAM addresses: [0, 1, 2]
Stored positions:
  Address 6: count=10
RAM 1:
RAM addresses: [0, 1, 2]
Stored positions:
  Address 6: count=12
...
========================
Class: uncomfortable
...
```

### Complete Example Code

```python
from symbolicwisardpkg import Wisard

# 1. Create model
wsd = Wisard(addressSize=3, verbose=True)

# 2. Define variables
variableIndexes = {
    "temp": 0,
    "humidity": 1,
    "wind": 2
}

# 3. Add rules
wsd.addRule(
    label="comfortable",
    variableIndexes=variableIndexes,
    rule="temp * humidity * !wind",
    alpha=10,
    base=2,
    ignoreZero=False
)

wsd.addRule(
    label="uncomfortable",
    variableIndexes=variableIndexes,
    rule="!temp + (humidity * wind)",
    alpha=8,
    base=2,
    ignoreZero=False
)

# 4. Prepare data
X_train = [
    [1, 1, 0],
    [1, 1, 0],
    [1, 0, 1],
    [0, 1, 1],
    [0, 0, 0],
    [1, 0, 0],
]

y_train = [
    "comfortable",
    "comfortable",
    "uncomfortable",
    "uncomfortable",
    "uncomfortable",
    "uncomfortable"
]

# 5. Train
wsd.trainWithRules(X_train, y_train)

# 6. Classify
X_test = [
    [1, 1, 0],
    [0, 1, 1],
    [1, 0, 1],
]

predictions = wsd.classifyWithRules(X_test)

for i, pred in enumerate(predictions):
    print(f"Input {X_test[i]}: {pred}")

# 7. Inspect
info = wsd.getRamsInfo()
print("\n" + info)

# 8. Example: Remove a sample from training (Leave-One-Out)
# Useful for cross-validation or data correction
wsd.leaveOneOut([1, 1, 0], "comfortable", considerRules=True)

# Check how classification changed after removing the sample
predictions_after = wsd.classifyWithRules(X_test)
print("\nPredictions after removing sample:")
for i, pred in enumerate(predictions_after):
    print(f"Input {X_test[i]}: {pred}")
```

---

## API Reference

### Constructor

```python
Wisard(addressSize, **kwargs)
```

**Parameters:**
- `addressSize` (int, required): Address size of each RAM
- `bleachingActivated` (bool, optional, default=True): Activates/deactivates bleaching
- `verbose` (bool, optional, default=False): Shows progress
- `ignoreZero` (bool, optional, default=False): Ignores address zero
- `completeAddressing` (bool, optional, default=True): Complete addressing
- `base` (int, optional, default=2): Numeric base
- `confidence` (int, optional, default=1): Minimum difference for classification

### Main Methods

#### `addRule(label, variableIndexes, rule, alpha, base=2, ignoreZero=False)`

Adds a symbolic rule to the model.

**Parameters:**
- `label` (str): Class name
- `variableIndexes` (dict): Mapping {variable_name: index}
- `rule` (str): Boolean expression
- `alpha` (int): Initial rule weight
- `base` (int, optional): Numeric base (default=2)
- `ignoreZero` (bool, optional): Ignores address zero (default=False)

**Example:**
```python
wsd.addRule(
    label="class1",
    variableIndexes={"A": 0, "B": 1},
    rule="A * B",  # A AND B
    alpha=5
)
```

#### `train(X, y)`

Trains the model with data (ignores symbolic rules).

**Parameters:**
- `X` (list): List of lists of integers (input data)
- `y` (list): List of strings (labels)

#### `trainWithRules(X, y)`

Trains the model considering symbolic rules.

**Parameters:**
- `X` (list): List of lists of integers (input data)
- `y` (list): List of strings (labels)

**Behavior:**
- Normal RAMs: always updated
- Rule RAMs: updated only when the rule is satisfied

#### `classify(X)`

Classifies data using only normal RAMs (ignores rules).

**Parameters:**
- `X` (list): List of lists of integers (data to classify)

**Returns:**
- `list`: List of strings (predicted classes)

#### `classifyWithRules(X)`

Classifies data considering symbolic rules.

**Parameters:**
- `X` (list): List of lists of integers (data to classify)

**Returns:**
- `list`: List of strings (predicted classes)

**Behavior:**
- Rule RAMs contribute with full counter value
- Normal RAMs go through bleaching process

#### `getRamsInfo()`

Returns detailed information about all RAMs.

**Returns:**
- `str`: Formatted string with RAM information

#### `getMentalImages()`

Returns patterns learned by the model.

**Returns:**
- `dict`: Dictionary {class: list_of_integers}

#### `leaveOneOut(image, label, considerRules=False)`

Removes the training effect of a single sample from the model. Useful for leave-one-out cross-validation or to remove specific samples.

**Parameters:**
- `image` (list): List of integers representing a sample
- `label` (str): Name of the class to which the sample belongs
- `considerRules` (bool, optional): If `True`, also removes the effect of rule RAMs. If `False` (default), only normal RAMs are affected.

**Behavior:**
- Decrements counters in RAMs corresponding to the sample
- If `considerRules=True`, also decrements counters in rule RAMs when applicable
- If `considerRules=False`, only normal RAMs are affected

**Example:**
```python
# Remove a specific sample from training
wsd.leaveOneOut([1, 1, 0], "comfortable", considerRules=True)

# Remove only from normal RAMs (ignore rules)
wsd.leaveOneOut([1, 1, 0], "comfortable", considerRules=False)
```

#### `leaveMoreOut(images, labels, considerRules=False)`

Removes the training effect of multiple samples from the model.

**Parameters:**
- `images` (list): List of lists of integers (samples to remove)
- `labels` (list): List of strings (corresponding classes)
- `considerRules` (bool, optional): If `True`, also removes the effect of rule RAMs. If `False` (default), only normal RAMs are affected.

**Behavior:**
- Iterates over all samples and calls `leaveOneOut` for each one
- Validates that the size of `images` and `labels` is the same
- Shows progress if `verbose=True`

**Example:**
```python
# Remove multiple samples (normal RAMs only)
X_remove = [
    [1, 1, 0],
    [0, 1, 1]
]
y_remove = ["comfortable", "uncomfortable"]

wsd.leaveMoreOut(X_remove, y_remove, considerRules=False)

# Remove multiple samples including rules
wsd.leaveMoreOut(X_remove, y_remove, considerRules=True)
```

**Note:** The default value of `considerRules` is different between the two functions:
- `leaveOneOut`: default is `True` (considers rules)
- `leaveMoreOut`: default is `False` (ignores rules)

---
