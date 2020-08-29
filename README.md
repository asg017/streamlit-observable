# streamlit-observable

Embed Observable notebooks into Streamlit apps!

## Why tho 

There are hundreds of Observable notebooks at observablehq.com that create 
beautiful data visualizations, graphs, charts, maps, and animations. Using the Observable runtime, you can inject your own data configuration into these notebooks, 

## Install

```bash
pip install streamlit-observable
```

## Usage

Check out the 

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
## Caveats

### Redefining or Observing Cells need to be JSON-serializable

In order to pass data from Python into an Observable notebook (with `redefine`), it needs to be JSON serializable, usually a `list`, `dict`, string or number. So if you're working with a pandas DataFrame or numpy array, you may need to wrangle it before redefining (usually with something like panda's [`.to_dict()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_dict.html) or numpy's [`.tolist()`](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.tolist.html)).

Similarly, when passing data from an Observable notebook back into Streamlit/Python (with `observe`), that data also needs to be JSON serializable. So when passing back [Date objects](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date), [Sets](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set), or other custon objects, you'll first need to represent it in some JSON serializable way, then wrangle it in Python-land to match what you expect. For example, with a Date object, you could convert to to the JSON-friendly Unix Epoch (number) with [.getTime()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/getTime), then read it as a datetime object in Python with [`datetime.fromtimestamp(time / 1000)`](https://docs.python.org/3/library/datetime.html).

### Accessing webcam and microphone doesn't work

Not entirely sure why this is the case, but if someone figures it out, I'd love to see a PR!

### Large Data is Hard

I haven't tried this, but I expect that if you try loading 1GB+ of data into a bar chart, something will break. All the data that you `redefine` will be read in memory in your browser when embeding into the chart, so something might break along the way. If you ever come across this, feel free to open an issue about it!

### You'll need to fork a lot

Most Observable notebooks are built with only other Observable users in mind. Meaning, a lot of cells are exposed as custom Objects, Dates, functions, or classes, all of which you can't control very well in Python land. So, you may need to fork the notebook you want in Observable, make changes to make it a little friendlier, then publish/enable link-sharing to access in Streamlit. Thankfully, this is pretty quick to do on Observable once you get the hang of it, but it does take extra time.