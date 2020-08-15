# streamlit-observable

Embed Observable notebooks into Streamlit Apps!

## Installation

```bash
pip install streamlit-observable
```

## Usage

```python
from streamlit_observable import observable
```

### Embed an Entire Notebook

```python
import streamlit as st
from streamlit_observable import observable

st.write("# Notebook Explainer")
observable("Noteo", ...)
```

## API Reference

### observable(key, notebook, _targets_=None, _redefine_={}, _observe_=[])

```
Create a new instance of "observable".

    Parameters
    ----------
    key: str
        A unique string used to avoid constant re-renders to the iframe.
    notebook: str
        The observablehq.com notebook id to embed. Ex. "@"d3/bar-chart"
        or "d/1f434ef3b0569a00"
    targets: list or None
        An optional list of strings that are the name of the cells to embed.
        By default, the entire notebook, including unnamed cells, will be embeded.
    observe: list or None
        An optional list of strings that are the name of cells to observe.
        Whenever these cells change value or become fulfilled, the value will
        be passed back into Streamlit as part of the return value.
    redefine: dict or None
        An optional dict containing the cells you wish to redefine and the values
        you wish to redefine them as. The keys are the cell names you want to
        redefine, the values are what they will be redefined as. Keep in mind,
        there is a serialization process from Streamlit Python -> frontend JavaScript.
    Returns
    -------
    dict
        An object containing the live observed values. If the observe parameter is
        empty, then the dict will be empty. The keys are the name of the cell that
        is observe, the values are the values of the cells.
```
