import streamlit as st
import pandas as pd
import numpy as np
from enum import Enum
import requests
import json 
import datetime
        
class Section(Enum):
    INTRO = "Introduction"
    
    BAR_CHART = "Static Embed: Bar Chart"
    PENGUINS =  "Static Embed: Scatterplot Matrix Penguins"
    SPIKE = "Static Embed: Spike Map"
    VORONOI = "Static Embed: Trader Joes Voronoi Map"
    WIKI = "Static Embed: Bar Chart Race of Wikipedia Views"

    FORM = "Bi-Directional Embed: HTML Form"
    DRAW = "Bi-Directional Embed: Drawing Canvas"
    COUNTIES = "Bi-Directional Embed: Selecting Counties"
    MATRIX = "Bi-Directional Embed: Matrix Input"
    

def explain_btn(section):
    return st.checkbox("Explain this to me!", key=f"explain_{section}")
        
def showcase(observable):
    sections = list(map(lambda d: d.value, Section))
    section_i = 0
    section_param = st.experimental_get_query_params().get("section")
    if section_param and section_param[0] in sections:
        section_i = sections.index(section_param[0])

    section = st.sidebar.radio(
        "Section",
        sections,
        index=section_i
    )

    if section == Section.INTRO.value:
        st.experimental_set_query_params(section=Section.INTRO.value)

        st.write("""
# Introduction to `streamlit-observable`

👋🏼 Hello! This Streamlit app is an introduction to the `streamlit-observable` 
library - a Streamlit custom component for embeding [Observable notebooks](https://observablehq.com)
into Streamlit apps. You can render, re-use, and recycle any Observable notebook
found on [observablehq.com](https://observablehq.com), 
giving you access to hundreds of data visualizations,
maps, charts, and animations that you can embed into any Streamlit app!

👈🏼Check out the sidebar for a deep-dive into different ways you can use 
`streamlit-observable` in your apps. Each example has a checkbox that looks like this:""")

        explain = explain_btn(Section.INTRO.value)

        st.write("If you click on it, you'll see more details of how the examples were made!")
    
        if explain:
            st.info("wow such hidden detail")

        st.write("""
Or, you can scroll down to get a quick taste of what `streamlit-observable` can do!
         """)
        
        with st.echo():
            observable("The Trusted Line Chart", "@d3/line-chart", ["chart"])

        with st.echo():
            observers = observable("World Tour!", 
                notebook="@d3/world-tour", 
                targets=["canvas"], 
                observe=["name"]
            )
            
            name = observers.get("name")
            
            st.write(f"Current country: ** *{name}* **")
        
        with st.echo():
            observable("Eyes", 
                notebook="@mbostock/eyes",
                targets=["canvas", "mouse"], 
                hide=["mouse"]
            )
        
        with st.echo():
            observable("Intro to Observable", "@observablehq/five-minute-introduction")

    # Bar Chart Section!
    elif section == Section.BAR_CHART.value:
        st.experimental_set_query_params(section=Section.BAR_CHART.value)

        st.write("## Static Embed: Bar Chart")
        explain = explain_btn(Section.INTRO.value)

        if explain:
            st.write("""
Let's start with a humble bar chart!

Let's define 3 different number sliders with 
[`st.slider`](https://docs.streamlit.io/en/stable/api.html#streamlit.slider), 
one for each person: Alex, Brian, and Craig. These sliders are normal Streamlit  widgets, 
defined in Python. With these 3 values, we can make a bar chart, with 1 bar per person. 
We could use the standard [D3 Bar Chart](https://observablehq.com/@d3/bar-chart) 
Observable notebook, but let's instead use Julien Barnier's 
[Updatable Bar Chart](https://observablehq.com/@juba/updatable-bar-chart) 
notebook, which gives nice transitions whenever the bar values change.

So we have our 3 Streamlit sliders, and we know what Observable notebook we want to use. How can we embed it?

        """)

        with st.echo():
            a = st.slider("Alex", value=30)
            b = st.slider("Brian", value=20)
            c = st.slider("Craig", value=50)

            observable("Example Updatable Bar Chart", 
                notebook="@juba/updatable-bar-chart", 
                targets=["chart", "draw"], 
                redefine={
                    "data": [
                        {"name": "Alex", "value": a},
                        {"name": "Brian", "value": b},
                        {"name": "Craig", "value": c}
                    ],
                },
                hide=["draw"]
            )
        if explain:
            st.write(""" 
And that's it! Try changing the `a`, `b`, or `c` sliders above, and watch how the new values automatically 
get propogated down into the notebook.

Let's quickly explain the parameters to the `observable()` function. You can find the full API Reference for 
`streamlit-observable` [here](TODO).

The first parameter, `"Example Updatable Bar Chart"`, is the `key` parameter, used to uniquely identify every `streamlit-observable` embed. 

`notebook` is the id of the notebook at observablehq.com. You can find this at the end of the notebook's URL: 
https://observablehq.com/@juba/updatable-bar-chart

`targets` are the cells of the notebook we want to be render in the embed. In this case, we just want to 
render the SVG chart found in the `chart` cell, as well as the `draw` cell that contains the logic that 
dynmically updates the chart with new data.

`redefine` is a dict with key/values of the cells of the notebook we want to redefine, or "inject" into. 
In this case, we want to redefine the `"data"` cell, which in the original notebook is an array of JS objects,
each with `"name"` and `"value"` keys. So, we can simply hardcode the 3 names we have, pass in the `a`, `b`, and `c` 
variables we defined with `st.slider` calls, and we're good to go!

`hide` is a list of cells that we want to be ran in the embed, but not displayed. In this case, since the `"draw"` 
cell only performs logic for updating the `"chart"` SVG (and does not embed anything of interest in itself), we can 
just hide it to make our embed cleaner. Normally, unless you are dealing with animations or transitions, you don't need 
to work with the `hide` parameter much! 
        """)


    # Penguins
    elif section == Section.PENGUINS.value:
        st.experimental_set_query_params(section=Section.PENGUINS.value)
        
        st.write("## Static Embed: Scatterplot Matrix with Penguins")
        explain = explain_btn(Section.PENGUINS.value)

        if explain:
            st.write("""
Allison Horst cleaned [published a dataset](https://github.com/allisonhorst/palmerpenguins)
 about penguins in Antartica, originally collected by Kristen Gorman! 
Using Streamlit, we can use `pd.read_csv` to read in the dataset into a pandas 
DataFrame, which looks like this:
        """)
        
        with st.echo():
            @st.cache
            def get_penguins():
                return pd.read_csv("https://raw.githubusercontent.com/allisonhorst/palmerpenguins/master/inst/extdata/penguins.csv")

            penguins = get_penguins()

            st.dataframe(penguins)

        if explain:
            st.write("""

Now, what if we want to visualize this data in a really cool way - say, with a 
[Brushable Scatterplot Matrix](https://observablehq.com/@d3/brushable-scatterplot-matrix)? 
It's possible! However, instead of using that D3 notebook directly, we're going to 
[fork the notebook](https://observablehq.com/@observablehq/fork-share-merge), in order to make 
these two changes:

1. In the D3 notebook, a color legend gets rendered in a cell, but the cell doesn't have a name,
making embeding hard. So, we'll just add a `legend =` to that cell to give it a name.
2. We want to be able to inject our own CSV string using a new cell, so we'll add a `rawData` 
cell that we can redefine to pass in our own CSV.

Now, we'll enable link sharing to that fork, and pass in the notebook's id into `observable()`!
""")

        with st.echo():
            observable("Palmer Penguin Scatterplot Matrix", 
                notebook="d/1bba1cb4219a9df5",
                targets=["chart", "legend"], 
                redefine={
                    "rawData":penguins.to_csv(),
                    "columns": ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]
                }
            )
        
        if explain:
            st.write("Try dragging a box around some of the points!")
    # Spike Map!
    elif section == Section.SPIKE.value:
        st.experimental_set_query_params(section=Section.SPIKE.value)

        st.write("## Static Embed: U.S. Spike Map of Births in 2010")
        explain = explain_btn(Section.SPIKE.value)

        if explain:
            st.write("""
Here, we re-use the [Spike Map](https://observablehq.com/@d3/spike-map) Observable notebook, 
with on own data on births per month in each county. [The dataset](https://github.com/the-pudding/data/tree/master/births) 
was cleaned and offered  by the folks over at [The Pudding](https://pudding.cool/2017/05/births/),
with the original dataset compiled by the US National Vital Statistics System.

Just like with penguin scatterplot matrix, we need to 
[fork the original D3 notebook](https://observablehq.com/d/1f434ef3b0569a00), 
for three reasons:

1. We want to choose the color of the spikes based off of 
[`st.color_picker`](https://docs.streamlit.io/en/stable/api.html#streamlit.beta_color_picker), 
but the color of the spikes weren't exposed in a separate cell in the original notebook. 
2. We want to pass in a JSON serializable list into the notebook, and re-use the data processing 
logic found in the original `"data"` cell.

Let's take a look at what the data looks like, and make a 
[`st.slider`](https://docs.streamlit.io/en/stable/api.html#streamlit.slider) 
widget to select a specific month in 2010 to look at:
""")

        with st.echo():
            @st.cache
            def get_birth_csv():
                df = pd.read_csv("https://raw.githubusercontent.com/the-pudding/data/master/births/allBirthData.csv",
                    dtype={
                        "State": str, 
                        "County": str
                    }
                )
                df["State"] = df["State"].str.zfill(2)
                df["County"] = df["County"].str[-3:]
                return df
            
            df = get_birth_csv()

            year = 2010
            month = st.slider("Month", min(df["Month"]), max(df["Month"]))
            
            df_map = df[(df["Year"] == year) & (df["Month"] == month)]

            st.dataframe(df_map)
        
        if explain:
            st.write("""
Now, let's make a color_picker widget, to choose what color the spikes should be.
We will pass that into the `redefine` param of `observable()`, as well as the value 
of `df_map` (which we will filter + tranform before passing it in, to match the schema
the underlying notebook is expecting).
""")

        with st.echo():
            color = st.beta_color_picker("Spike Color", "#ff0000")
        
            observable("Spike Chart of Births by County", 
                notebook="d/1f434ef3b0569a00", 
                targets=["chart"], 
                redefine={
                    "rawData": df_map[["countyBirths", "State", "County"]].to_numpy().tolist(),
                    "color": color
                }
            )
        
        if explain:
            st.write('Now try changing the "Month" slider and the "Spike Color" color picker, and see how the map responds!')

    # Voronoi!
    if section == Section.VORONOI.value:
        st.experimental_set_query_params(section=Section.VORONOI.value)

        st.write("## Static Embed: Voronoi Map of Trader Joe's")
        explain = explain_btn(Section.VORONOI.value)
        
        if explain:
            st.write("""
A [voronoi diagram](https://en.wikipedia.org/wiki/Voronoi_diagram) can partition 
points on plane into regions based on how close they are to each other. In map-making, 
we can use this technique to roughly see how clustered points are on a certain geography. 
To try this out, let's make a voronoi map of all Trader Joe's locations in the United States!

First off, let's get data on all the Trader Joe's stores in the United States. They 
have an unprotected internal API on their website, which we can borrow like so. We 
will convert the raw JSON that the API returns into a nicer pandas DataFrame 
with the columns `"latitude"`, `"longitude"`, and `"name"`.
""")

        with st.echo():
            @st.cache
            def get_trader_joes():
                req_data = {
                    "request":{
                        "appkey":"8559C922-54E3-11E7-8321-40B4F48ECC77",
                        "formdata":{
                            "geoip":True,
                            "dataview":"store_default",
                            "limit":30000,
                            "geolocs":{
                                "geoloc":[{"addressline":"","country":"","latitude":"","longitude":""}]
                            },
                            "searchradius":"3000",
                            "where":{"or":{"wine":{"eq":""},"beer":{"eq":""},"liquor":{"eq":""},"comingsoon":{"eq":""}},"warehouse":{"distinctfrom":"1"}},
                            "true":"1"
                        },
                    "geoip":1
                    }
                }
                response = requests.post('https://hosted.where2getit.com/traderjoes/rest/locatorsearch?like=0.07986455552168592&lang=en_US', data=json.dumps(req_data))
                data = response.json()
                df = pd.DataFrame(data.get("response").get("collection"))
                df["longitude"] = df["longitude"].astype('float')
                df["latitude"] = df["latitude"].astype('float')
                df["name"] = ""
                return df
            
            df_tjs = get_trader_joes()

        if explain:
            st.write(df_tjs)

            st.write("""
The reason why we overwrite the `"name"` column with an empty string is purely for aesthetics.
If we were to put labels on every store, the map would become a giant 
mess of 100's of labels everywhere, so we'll just skip it for this.

Now, let's embed this data into an Observable notebook! Thankfully, Mike Bostock wrote 
[U.S. Voronoi Map-o-Matic](https://observablehq.com/@mbostock/u-s-voronoi-map-o-matic) 
that we can plug into. The notebook expects the `data` cell to be an array of JS objects, 
so we'll convert the DataFrame into a list of dicts before redefining:
""")
        with st.echo():
            observable("Trader Joes Voronoi Map", 
                notebook="@mbostock/u-s-voronoi-map-o-matic", 
                targets=["map"],
                redefine={
                    "data": df_tjs[["longitude", "latitude", "name"]].to_dict(orient="records")
                }
            )
        
        if explain:
            st.write("Voila!")

    # Wikipedia bar chart race!
    elif section == Section.WIKI.value:
        st.experimental_set_query_params(section=Section.WIKI.value)

        st.write("## Static Component: Bar Chart Race with Wikipedia Pageviews")
        explain = explain_btn(Section.WIKI.value)
        
        if explain:
            st.write(""" 
Let's make a bar chart race with Wikipedia pageview data! If you don't know what a bar chart
race is, check out the D3 [Bar Chart Race](https://observablehq.com/@d3/bar-chart-race) 
notebook, that we will work on top of for this.

First up, let's use the Wikipedia REST API to get the data. I won't go super in-depth into 
this, but if you want to learn more about all the different APIs to access Wikipedia pageview 
numbers, check out [this wiki](https://wikitech.wikimedia.org/wiki/Analytics/AQS/Pageviews). 

The endpoint we'll use will give us the top viewed Wikipedia articles for a given day (on desktop).
We'll grab the data starting on March 1st 2020 and ending 50 days later. The code is a little 
verbose, which you don't need to understand fully. In essence, for every day in the range we want,
we make an API request to get that day's data, we transform the schema of the data to match what 
we expect, filter out pages we don't want to see (e.g. "Main_Page"), and stuff all the day's data 
into one large pandas DataFrame.

The schema we want to match depends on the `"data"` cell in the Observable notebook. That cell
is an array of JS objects, where each object has `"date"`, `"name"`, `"category"`, and `"value"` 
keys. For this pageviews data, `"date"` will be the date that we requested, `"name"` will be 
the name of the article, `"category"` we'll just ignore (it determines the color of each bar,
which we don't need to worry about), and `"value"` will be the number of desktop views that 
page got in the given day.
""")
        with st.echo():
            @st.cache
            def get_wiki_data():
                df = pd.DataFrame(columns=["date", "article", "views", "rank"])
                dates = pd.date_range(datetime.date(2020, 3, 1), periods=50).tolist()
                for d in dates:
                    response = requests.get(
                        "https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/desktop/{year}/{month}/{day}"
                            .format(year=d.year, month=d.strftime("%m"), day=d.strftime("%d"))
                    )
                    day_data = response.json()
                    articles = day_data.get("items")[0].get("articles")
                    articles = list(map(lambda a: {
                        "article": a.get("article"),
                        "views": a.get("views"),
                        "rank": a.get("rank"),
                        "date": d.strftime("%Y-%m-%d")
                    }, articles))

                    def filter_articles(d):
                        if d.get("article") == "Main_Page":
                            return False
                        if "Special:" in d.get("article"):
                            return False
                        return d.get("rank") < 50

                    articles = list(filter(filter_articles, articles))
                    df = df.append(articles, ignore_index=True)
                return df.rename(columns={
                    "article": "name",
                    "views": "value"
                })
            df_wiki = get_wiki_data()

        st.write(df_wiki)

        if explain:
            st.write("""
Now, we're also going to [fork](https://observablehq.com/d/9bbcce8f2f6834d7) 
the original D3 notebook to make a couple of cosmetic changes. You can view the exact changes 
[in this comparison view](https://observablehq.com/compare/3ff9fa2c6593d814@3046...9bbcce8f2f6834d7@3073),
but here's a quick overview of what we had to change:

1. We add a new `"rawData"` cell that we can use to inject our own CSV string to change the 
data in the bar chart race.
2. We use a [Scrubber](https://observablehq.com/@mbostock/scrubber) 
to control the animation, so people can pause and control the pace of the animation.
3. We change the `"formatDate"` cell to include the month and day when rendering the date in 
the animation.
""")

        with st.echo():
            observable("Wiki Bar Chart Race", 
                notebook="d/9bbcce8f2f6834d7", 
                redefine={
                    "rawData": df_wiki.to_csv(),
                    "duration": 200,
                    "n": 10
                }, 
                targets=["chart", "viewof keyframe", "update"],
                hide=["update"]
            )
        st.write("Dope! I don't know why the Laptop Wikipedia page was so popular in early March...")

    # Form!
    elif section == Section.FORM.value:
        st.experimental_set_query_params(section=Section.FORM.value)
        
        st.write("## Bi-Directional Component: HTML Form")
        explain = explain_btn(Section.FORM.value)
        
        if explain:
            st.write(""" 
`streamlit-observable` can not only embed an Observable notebook from Python -> JavaScript, but
we can also pass values back from an Observable notebook, from Javascript -> Python!

Let's use Mike Bostock's [Form Input](https://observablehq.com/@mbostock/form-input) notebook as an example.
The notebook offers a cool utility in the `"form"` cell, which can be used to turn any HTML form into an 
Observable "view" (See ["Introduction to Views"](https://observablehq.com/@observablehq/introduction-to-views) 
for an explanation). It also has an example, found in the `"viewof object"` cell. 
Let's embed that example cell into Streamlit, then pass that cell's value back into Python!
        """)
        with st.echo():
            observers = observable("Example form", 
                notebook="@mbostock/form-input",
                targets=["viewof object"],
                observe=["object"]
            )

            o = observers.get("object")

            if o is not None:
                st.write("message: **'{message}'**, hue: '{hue}', size: '{size}', emojis: '{emojis}'".format(
                    message=o.get("message"),
                    hue=o.get("hue"),
                    size=o.get("size"),
                    emojis=str(o.get("emojis"))
                ))
        
        if explain:
            st.write(""" 
Let's take a closer look to see how this example is working:

First part, rendering the actual notebook. We pass in the key, `"Example form"`. 
The `notebook` param passes in the observablehq.com notebook ID for the notebook, `"@mbostock/form-input"`.
In `targets`, we only want to render the `"viewof object"` cell, which is the cell that is the HTML form 
that we want to interact with. The `observe` parameter is a list of cells that we want to observe.
Meaning, whenever the value of the `"object"` cell changes, we want to pass that new value 
back into the Streamlit app/Python-land. """)
        
            if st.button('❓Whats the difference between the "viewof object" cell and the `"object"` cell?'):
                st.info("""The `"viewof object"` cell and the `"object"` cell are two different cells, 
even though they are defined on the same line in the Observable notebook. The `"viewof object"` cell is
the HTML form that we want to embed and see in the browser, and the `"object"` cell is underlying 
*value* of that HTML form. See 
["A Brief Introduction to Viewof"](https://observablehq.com/@observablehq/a-brief-introduction-to-viewof)
for details.
""")
            st.write(""" 
Now, when you pass in any cell name into `observe`, then the `observable()` call will return a dict,
where the keys are the names of the cells, and the values are the value of those cells as they 
exist in the notebook. In this case, the entire `"observers"` object looks like this:
""")

            with st.echo():
                st.json(observers)
            
            st.write("""
So, to access the value of the `"object"` cell, we can just call `observers.get("object")`, and we'll 
have the Python-serialized value of that cell from Observable!
""")


    # Draw me!
    elif section == Section.DRAW.value:
        st.experimental_set_query_params(section=Section.DRAW.value)

        st.write("## Bi-Directional Component: Drawing Canvas")
        explain = explain_btn(Section.DRAW.value)

        if explain:
            st.write("""
Let's play with the D3 [Draw Me](https://observablehq.com/@d3/draw-me) notebook! 
If we embed it and observe the `"strokes"` cell, then users of our Streamlit app 
could draw images, and we can receive the points of those strokes back in Python!
""")
        with st.echo():
            observers = observable("Example Drawing Canvas", 
                notebook="@d3/draw-me", 
                targets=["viewof lineWidth", "viewof strokeStyle", "undo", "viewof strokes"], 
                observe=["strokes"]
            )
        
        if explain:
            st.write("""
Try drawing on the white canvas above! We embed 4 different cells  to make this work: 

1. `"viewof lineWidth"`, the slider that determines the width of the line the user draws.
2. `"viewof strokeStyle"`, a color picker that chooses the color of the line the user draws.
3. `"undo"`, a form that allows to removing/adding back the last change the user made.
4. `"viewof strokes"`, the canvas that the user can draw on. 

Then, we can observe the value of the `"strokes"`, cell, which will update on every stroke. 
It comes back as a list of strokes, where every stroke is a list of x-y coordinates of 
the user's drawing. 
            """)

        with st.echo():
            strokes = observers.get("strokes")
            st.json(strokes)

        if explain:
            st.write("""
You can use in conjunction with 
[Google's "Quick, Draw!" dataset](https://github.com/googlecreativelab/quickdraw-dataset) 
to test out a drawing classifier on the fly!
""")

    # Counties!
    elif section == Section.COUNTIES.value:
        st.experimental_set_query_params(section=Section.COUNTIES.value)
        
        st.write("## Bi-Directional Component - Selecting U.S. Counties")
        explain = explain_btn(Section.COUNTIES.value)

        if explain:
            st.write("""
Here, we embed the [FIPS County Code Brush](https://observablehq.com/@awhitty/fips-county-code-brush) 
Observable notebook, which gives us a U.S. County map where we can "brush" 
to select specific U.S. counties Then, in Streamlit, we fetch data from the 
U.S. Census Bureau using their [REST API](https://www.census.gov/data/developers/data-sets/acs-1year.html) 
to calculate how many people live inside and outside the brushed area!

First, we'll use the Census API to get data from the 
[American Community Survey](https://www.census.gov/programs-surveys/acs) in 2018, which compiles 
estimates of how many people live in the US (not to be confused with the *actual* census, which actually 
counts the number of people). The 
[`B01001_001E`](https://api.census.gov/data/2018/acs/acs1/variables/B01001_001E.html) 
variable is the total estimated people for a given geography, and we will request that variable 
for every county in the United States. We'll then transform that API resonse to create a 
`"county_fips"` column, which will be the county 
[FIPS Code](https://www.census.gov/geographies/reference-files/2017/demo/popest/2017-fips.html) 
that the notebook is expecting.

""")    
        with st.echo():
            @st.cache
            # Pls dont roast my pandas code
            def get_county_pop():
                df = pd.read_json(
                    "https://api.census.gov/data/2018/acs/acs5?get=B01001_001E&for=county:*", 
                    orient="records",
                    dtype=False
                )
                df.drop(df.head(1).index, inplace=True)
                df = df.rename(columns={0:"population", 1:"state", 2:"county"})
                df.population = df.population.astype('int')
                df["county_fips"] = df["state"] + df["county"]
                
                return df

            df = get_county_pop()
        
        st.write(df)

        if explain:
            st.write("""
Now, we do have to [fork](https://observablehq.com/d/4f9aa5feff9761c9) the original notebook, because 
the original notebook only returns a cell called `"countyCodes"` that is a 
[JavaScript Set](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set) 
of the counties that are selected. However, a Set isn't JSON-serializable, which we need to 
return back to Streamlit. So, the fork adds a new cell, `"selectedCounties"`, which simply wraps 
the `"countyCodes"` cell with `Array.from()` to convert to a JSON-serializable array. You can 
[compare the original notebook and the fork here](https://observablehq.com/compare/681a742a4888d182@700...4f9aa5feff9761c9@703).
""")

        with st.echo():
            observers = observable("County Brush", 
                notebook="d/4f9aa5feff9761c9",
                targets=["viewof countyCodes"], 
                observe=["selectedCounties"]
            )

            selectedCounties = observers.get("selectedCounties")
        
        st.write(selectedCounties)
        
        if explain:
            st.write("""
So we have `selectedCounties`, a list of counties that are selected in the map above, and 
`df`, a dataframe of all counties in the United States with the size of the population. 
Now, we can do a little pandas magic 🔮 to find out how many people live inside and 
outside the selected counties:
""")

        with st.echo():
            df_selected = df[df["county_fips"].isin(selectedCounties)]
            df_not_selected = df[~df["county_fips"].isin(selectedCounties)]

            sel_sum = df_selected.population.sum()
            not_sel_sum = df_not_selected.population.sum()

            st.write("""
**{:,}** people live in the **{:,}** counties that are selected above. 
That's **{:.2%}** of the total US population.""".format(
                sel_sum, len(df_selected), sel_sum / not_sel_sum
            ))
    
    elif section == Section.MATRIX.value:
        st.experimental_set_query_params(section=Section.MATRIX.value)
            
        st.write("## Bi-Directional Embed: Matrix Input")
        explain = explain_btn(Section.MATRIX.value)
        
        if not explain:
            st.write("""
Try clicking on the the first two matrices, and see the multiplication result at the bottom!
""")
        else:
            st.write("""
    Let's play with some matrices! Bryan Gin-ge Chen write a neat notebook called 
    [Grid inputs](https://observablehq.com/@bryangingechen/grid-inputs), which 
    gives some utility functions in Observable to render matricies in an aesthetic 
    way, and allows people to change the values of a matrix very easily. Let's use 
    these utilities to define a matrix in an Observable notebook embed, then read 
    that matrix into Streamlit, then perform some operations on it in Python and 
    pass it *back into* an Observable notebook for nice rendering!

    Here's the plan: we embed 2 matricies: `a`, with 10 columns and 5 rows (10x5), 
    and `b`, with 5 columns and 10 rows (5x10). Then, we read those values into 
    Python numpy arrays, and use 
    [`np.matmul`](https://numpy.org/doc/stable/reference/generated/numpy.matmul.html)
    to multiply `a` and `b` together. Finally, we'll embed that resulting matrix 
    into *another* Observable notebook using 
    [`pt()`](https://observablehq.com/d/43b57dd558b3d1ee#pt), 
    a function that renders matrices into a nice $LaTeX$ format.

    Let's try it out!

    [Here's the notebook](https://observablehq.com/d/9e0aa2504039dbcd) we'll be embeding.
    Notice how  we are importing the `"grid"` and `"pt"` cells from Bryan's 
    `grid-inputs` notebook. We define 2 cells, `"viewof a"` and `"viewof b"`, which 
    both use `grid()` to create matrices of different sizes (10x5 and 5x10, respectfully).
    We also create a `"prettyExample"` cell, which just pretty-prints the matrix 
    that's defined in the `"example"` cell. Now let's embed these into Streamlit! 


    """)

        with st.echo():
            observers_a = observable("Matrix Input A", 
                notebook="d/9e0aa2504039dbcd",
                targets=["viewof a"],
                observe=["a"]
            )
            observers_b = observable("Matrix Input B", 
                notebook="d/9e0aa2504039dbcd",
                targets=["viewof b"],
                observe=["b"]
            )
        if explain:
            st.write("""
    Note: we could've just embed both cells in the same component by passing 
    in both cells into `targets` (which would look like `targets=["viewof a", "viewof b"]`).
    But it looked better when they were separated into their own components.

    Now, let's read in the values of the `a` and `b` cells:
            """)

        with st.echo():
            a = observers_a.get("a")
            b = observers_b.get("b")

        if explain:
            st.write("Then let's multiply these two matricies together:")

        with st.echo():
            result = np.matmul(a, b)

        if explain:
            st.write("""Finally, let's use that `"prettyExample"` cell
to render the multiplication result out!""")

        with st.echo():
            observable("np.matmul result", 
                notebook="d/9e0aa2504039dbcd",
                targets=["prettyExample"],
                redefine={
                    "example": result.tolist()
                }
            )

        if explain:
            st.write("""
Nice! Try clicking on the `a` and `b` matrices above, and see how the 
multiplication results changes.
""")
