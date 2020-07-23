import os
import streamlit.components.v1 as components

_RELEASE = False

if not _RELEASE:
    _component_func = components.declare_component(
        "observable",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("observable", path=build_dir)


def observable(notebook, targets=None, observe=[], redefine={}):
    """Create a new instance of "observable".

    Parameters
    ----------
    name: str
        The name of the thing we're saying hello to. The component will display
        the text "Hello, {name}!"
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.

    Returns
    -------
    int
        The number of times the component's "Click Me" button has been clicked.
        (This is the value passed to `Streamlit.setComponentValue` on the
        frontend.)

    """
    component_value = _component_func(notebook=notebook, targets=targets, observe=observe, redefine=redefine)
    return component_value


if not _RELEASE:
    import streamlit as st

    observable("d/a62482148de72e3f", targets=["video"])
    observable(notebook="@d3/horizontal-bar-chart", 
        targets=["chart"], 
        redefine={
            "data": [
                {"name":"Alex", "value": 100},
                {"name":"Brian", "value": 300},
                {"name":"Craig", "value": 200}
            ],
        }
    )
    d = observable(notebook="@mbostock/form-input", 
        targets=["viewof object"], 
        observe=["object"]
    )
    st.json(d)

    observable(notebook="@d3/disjoint-force-directed-graph", targets=["chart"])

    strokes = observable(notebook="@d3/draw-me", 
        targets=[
            "viewof strokes",
            "viewof lineWidth", 
            "viewof strokeStyle", 
            "undo"
        ], observe=["strokes"])

    st.json(strokes)

    countyCodes = observable(notebook="@awhitty/fips-county-code-brush", targets=["viewof countyCodes"], observe=["countyCodes"])
    st.json(countyCodes)