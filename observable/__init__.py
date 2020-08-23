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
    _component_func = components.declare_component(
        "observable", path=build_dir)


def observable(key, notebook, targets=None, redefine={}, observe=[]):
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
        key=key
    )
    return component_value


if not _RELEASE:
    import streamlit as st
    import pandas as pd

    @st.cache
    def get_birth_csv():
        df = pd.read_csv("https://raw.githubusercontent.com/the-pudding/data/master/births/allBirthData.csv",
                         dtype={"State": str, "County": str})
        df["State"] = df["State"].str.zfill(2)
        df["County"] = df["County"].str[-3:]
        return df

    section = st.sidebar.selectbox(
        "Example",
        ("spike", "bar-chart", "form", "force-graph", "draw", "counties")
    )

    if section == 'spike':
        df = get_birth_csv()

        year = st.slider("Year", min(df["Year"]), max(df['Year']), value=2010)
        month = st.slider("Month", min(df["Month"]), max(df["Month"]))
        color = st.selectbox("yeet", ("red", "blue", "green"))

        df_map = df[(df["Year"] == year) & (df["Month"] == month)]

        st.write(year, month, color, df_map.shape, df_map.columns)
        st.dataframe(df_map)
        observable("Spike Chart of Births by County", "d/1f434ef3b0569a00", targets=["chart"], redefine={
            "rawData": df_map[["countyBirths", "State", "County"]].to_numpy().tolist(),
            "color": color
        })
    elif section == 'bar-chart':
        a = st.slider("Alex", value=30)
        b = st.slider("Brian", value=20)
        c = st.slider("Craig", value=50)

        observable("Example Updatable Bar Chart", "@juba/updatable-bar-chart", ["chart", "draw"], {
            "data": [
                {"name": "Alex", "value": a},
                {"name": "Brian", "value": b},
                {"name": "Craig", "value": c}
            ],
        }
        )
    elif section == 'form':
        d = observable("Example form", "@mbostock/form-input",
                       targets=["viewof object"],
                       observe=["object"]
                       )
        o = d.get("object")
        st.write("message: **'{message}'**, hue: '{hue}', size: '{size}', emojis: '{emojis}'".format(
            message=o.get("message"),
            hue=o.get("hue"),
            size=o.get("size"),
            emojis=str(o.get("emojis"))
        ))

    elif section == 'force-graph':
        @st.cache
        def get_force():
            df_characters = pd.read_json(
                'https://raw.githubusercontent.com/sxywu/hamilton/master/src/data/char_list.json')
            df_links = pd.read_csv(
                'https://raw.githubusercontent.com/sxywu/hamilton/master/data/meta/characters.csv')
            return (df_characters, df_links)
        df_characters, df_links = get_force()
        characters = df_characters.transpose().rename(
            columns={0: "id", 1: "group"}).to_dict('records')

        character_index_to_name = {}
        for index, character in enumerate(characters):
            character_index_to_name[index] = character.get("id")

        df_links_directed = df_links[~df_links["directed_to"].isna()]
        df_links_directed = df_links_directed[
            (df_links_directed["characters"].str.isnumeric())
            & (df_links_directed["directed_to"].str.isnumeric())]
        d = df_links_directed.groupby(
            ["characters", "directed_to"])["lines"].count().rename_axis(["from", "to"]).reset_index(level=[0, 1])
        st.write(character_index_to_name)
        d["from"] = d["from"].apply(lambda x: character_index_to_name[(x)])
        d["to"] = d["to"].apply(lambda x: character_index_to_name[(x)])
        st.write(d)

        observable("Example Force Directed Graph", notebook="@d3/disjoint-force-directed-graph", targets=["chart"],
                   redefine={
            "data": {
                "nodes": characters,
                "links": [],
            }
        })

    elif section == 'draw':
        strokes = observable("Example Drawing Canvas", notebook="@d3/draw-me", targets=[
                             "viewof strokes", "viewof lineWidth", "viewof strokeStyle", "undo"], observe=["strokes"])

        st.json(strokes)

    elif section == 'counties':
        countyCodes = observable("County Brush", notebook="@awhitty/fips-county-code-brush",
                                 targets=["viewof countyCodes"], observe=["countyCodes"])
        st.json(countyCodes)
    observable("Eyes", notebook="@mbostock/eyes",
               targets=["canvas", "mouse"])
