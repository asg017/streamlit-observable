import os
import streamlit.components.v1 as components

_RELEASE = True

if not _RELEASE:
    _component_func = components.declare_component(
        "observable",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend", "build")
    _component_func = components.declare_component("observable", path=build_dir)


def observable(key, notebook, targets=None, redefine={}, observe=[], hide=[]):
    """Create a new instance of "observable".

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
    hide: list or None
        An option list of strings that are the names of cells that will be embeded,
        but won't be rendered to the DOM.
    Returns
    -------
    dict
        An object containing the live observed values. If the observe parameter is
        empty, then the dict will be empty. The keys are the name of the cell that
        is observe, the values are the values of the cells.

    """
    component_value = _component_func(
        notebook=notebook,
        targets=targets,
        observe=observe,
        redefine=redefine,
        hide=hide,
        key=key,
        name=key
    )
    return component_value


if not _RELEASE:
    observers = observable("World Tour!", 
        notebook="@d3/world-tour", 
        targets=["canvas"], 
        observe=["name"]
    )
    
    name = observers.get("name")
    
    st.write(f"Current country: ** *{name}* **")
    