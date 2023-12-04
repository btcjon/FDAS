[Open this notebook in Jupyterlite](https://panelite.holoviz.org/?path=/reference/widgets/Tabulator.ipynb) | [Download this notebook from GitHub (right-click to download).](https://raw.githubusercontent.com/holoviz/panel/main/examples/reference/widgets/Tabulator.ipynb)

___

```
import datetime as dt
import numpy as np
import pandas as pd
import panel as pn

np.random.seed(7)
pn.extension('tabulator')

```

The `Tabulator` widget allows displaying and editing a pandas DataFrame. The `Tabulator` is a largely backward compatible replacement for the [`DataFrame`](https://panel.holoviz.org/reference/widgets/DataFrame.html) widget and will eventually replace it. It is built on the **version 5.5** of the [Tabulator](http://tabulator.info/) library, which provides for a wide range of features.

Discover more on using widgets to add interactivity to your applications in the how-to guides on interactivity. Alternatively, learn [how to set up callbacks and (JS-)links between parameters](https://panel.holoviz.org/how_to/links/index.html) or how to use them as part of declarative UIs with Param.

## Parameters:[#](https://panel.holoviz.org/reference/widgets/Tabulator.html#parameters "Permalink to this heading")

For details on other options for customizing the component see the [layout](https://panel.holoviz.org/how_to/layout/index.html) and [styling](https://panel.holoviz.org/how_to/styling/index.html) how-to guides.

### Core[#](https://panel.holoviz.org/reference/widgets/Tabulator.html#core "Permalink to this heading")

-   **`aggregators`** (`dict`): A dictionary mapping from index name to an aggregator to be used for `hierarchical` multi-indexes (valid aggregators include ‘min’, ‘max’, ‘mean’ and ‘sum’). If separate aggregators for different columns are required the dictionary may be nested as `{index_name: {column_name: aggregator}}`
    
-   **`buttons`** (`dict`): A dictionary of buttons to add to the table mapping from column name to the HTML contents of the button cell, e.g. `{'print': '<i class="fa fa-print"></i>'}`. Buttons are added after all data columns.
    
-   **`configuration`** (`dict`): A dictionary mapping used to specify _Tabulator_ options not explicitly exposed by Panel.
    
-   **`editors`** (`dict`): A dictionary mapping from column name to a bokeh `CellEditor` instance or _Tabulator_ editor specification.
    
-   **`embed_content`** (`boolean`): Whether to embed the `row_content` or to dynamically fetch it when a row is expanded.
    
-   **`expanded`** (`list`): The currently expanded rows as a list of integer indexes.
    
-   **`filters`** (`list`): A list of client-side filter definitions that are applied to the table.
    
-   **`formatters`** (`dict`): A dictionary mapping from column name to a bokeh `CellFormatter` instance or _Tabulator_ formatter specification.
    
-   **`frozen_columns`** (`list`): List of columns to freeze, preventing them from scrolling out of frame. Column can be specified by name or index.
    
-   **`frozen_rows`**: (`list`): List of rows to freeze, preventing them from scrolling out of frame. Rows can be specified by positive or negative index.
    
-   **`groupby`** (`list`): Groups rows in the table by one or more columns.
    
-   **`header_align`** (`dict` or `str`): A mapping from column name to header alignment or a fixed header alignment, which should be one of `'left'`, `'center'`, `'right'`.
    
-   **`header_filters`** (`boolean`/`dict`): A boolean enabling filters in the column headers or a dictionary providing filter definitions for specific columns.
    
-   **`hidden_columns`** (`list`): List of columns to hide.
    
-   **`hierarchical`** (boolean, default=False): Whether to render multi-indexes as hierarchical index (note hierarchical must be enabled during instantiation and cannot be modified later)
    
-   **`layout`** (`str`, `default='fit_data_table'`): Describes the column layout mode with one of the following options `'fit_columns'`, `'fit_data'`, `'fit_data_stretch'`, `'fit_data_fill'`, `'fit_data_table'`.
    
-   **`page`** (`int`, `default=1`): Current page, if pagination is enabled.
    
-   **`page_size`** (`int`, `default=20`): Number of rows on each page, if pagination is enabled.
    
-   **`pagination`** (`str`, `default=None`): Set to `'local` or `'remote'` to enable pagination; by default pagination is disabled with the value set to `None`.
    
-   **`row_content`** (`callable`): A function that receives the expanded row (`pandas.Series`) as input and should return a Panel object to render into the expanded region below the row.
    
-   **`selection`** (`list`): The currently selected rows as a list of integer indexes.
    
-   **`selectable`** (`boolean` or `str` or `int`, `default=True`): Defines the selection mode:
    
    -   `True` Selects rows on click. To select multiple use Ctrl-select, to select a range use Shift-select
        
    -   `False` Disables selection
        
    -   `'checkbox'` Adds a column of checkboxes to toggle selections
        
    -   `'checkbox-single'` Same as ‘checkbox’ but header does not allow select/deselect all
        
    -   `'toggle'` Selection toggles when clicked
        
    -   `int` The maximum number of selectable rows.
        
-   **`selectable_rows`** (`callable`): A function that should return a list of integer indexes given a DataFrame indicating which rows may be selected.
    
-   **`show_index`** (`boolean`, `default=True`): Whether to show the index column.
    
-   **`sortable`** (`bool | dict[str, bool]`, `default=True`): Whether the table is sortable or whether individual columns are sortable. If specified as a bool applies globally otherwise sorting can be enabled/disabled per column.
    
-   **`sorters`** (`list`): A list of sorter definitions mapping where each item should declare the column to sort on and the direction to sort, e.g. `[{'field': 'column_name', 'dir': 'asc'}, {'field': 'another_column', 'dir': 'desc'}]`.
    
-   **`text_align`** (`dict` or `str`): A mapping from column name to alignment or a fixed column alignment, which should be one of `'left'`, `'center'`, `'right'`.
    
-   **`theme`** (`str`, `default='simple'`): The CSS theme to apply (note that changing the theme will restyle all tables on the page), which should be one of `'default'`, `'site'`, `'simple'`, `'midnight'`, `'modern'`, `'bootstrap'`, `'bootstrap4'`, `'materialize'`, `'bulma'`, `'semantic-ui'`, or `'fast'`.
    
-   **`theme_classes`** (`list[str]`): List of extra CSS classes to apply to the Tabulator element to customize the theme.
    
-   **`title_formatters`** (`dict`): A dictionary mapping from column name to a _Tabulator_ formatter specification.
    
-   **`titles`** (`dict`): A mapping from column name to a title to override the name with.
    
-   **`value`** (`pd.DataFrame`): The pandas DataFrame to display and edit
    
-   **`widths`** (`dict`): A dictionary mapping from column name to column width in the rendered table.
    

### Display[#](https://panel.holoviz.org/reference/widgets/Tabulator.html#display "Permalink to this heading")

-   **`disabled`** (`boolean`): Whether the cells are editable
    

### Properties[#](https://panel.holoviz.org/reference/widgets/Tabulator.html#properties "Permalink to this heading")

-   **`current_view`** (`DataFrame`): The current view of the table that is displayed, i.e. after sorting and filtering are applied. `current_view` isn’t guaranteed to be in sync with the displayed current view when sorters are applied and values are edited, in which case `current_view` is sorted while the displayed table isn’t.
    
-   **`selected_dataframe`** (`DataFrame`): A DataFrame reflecting the currently selected rows.
    

### Callbacks[#](https://panel.holoviz.org/reference/widgets/Tabulator.html#callbacks "Permalink to this heading")

-   **`on_click`**: Allows registering callbacks which are given `CellClickEvent` objects containing the `column`, `row` and `value` of the clicked cell.
    
-   **`on_edit`**: Allows registering callbacks which are given `TableEditEvent` objects containing the `column`, `row`, `value` and `old` value of the edited cell.
    

In both these callbacks `row` is the index of the `value` DataFrame.

___

The `Tabulator` widget renders a DataFrame using an interactive grid, which allows directly editing the contents of the DataFrame in place, with any changes being synced with Python. The `Tabulator` will usually determine the appropriate formatter appropriately based on the type of the data:

```
df = pd.DataFrame({
    'int': [1, 2, 3],
    'float': [3.14, 6.28, 9.42],
    'str': ['A', 'B', 'C'],
    'bool': [True, False, True],
    'date': [dt.date(2019, 1, 1), dt.date(2020, 1, 1), dt.date(2020, 1, 10)],
    'datetime': [dt.datetime(2019, 1, 1, 10), dt.datetime(2020, 1, 1, 12), dt.datetime(2020, 1, 10, 13)]
}, index=[1, 2, 3])

df_widget = pn.widgets.Tabulator(df, buttons={'Print': "<i class='fa fa-print'></i>"})
df_widget

```

## Formatters[#](https://panel.holoviz.org/reference/widgets/Tabulator.html#formatters "Permalink to this heading")

By default the widget will pick Bokeh `CellFormatter` and `CellEditor` types appropriate to the dtype of the column. These may be overridden by explicit dictionaries mapping from the column name to the editor or formatter instance. For example below we create a `NumberFormatter` to customize the formatting of the numbers in the `float` column and a `BooleanFormatter` instance to display the values in the `bool` column with tick crosses:

```
from bokeh.models.widgets.tables import NumberFormatter, BooleanFormatter

bokeh_formatters = {
    'float': NumberFormatter(format='0.00000'),
    'bool': BooleanFormatter(),
}

pn.widgets.Tabulator(df, formatters=bokeh_formatters)

```

The list of valid Bokeh formatters includes:

-   [BooleanFormatter](https://docs.bokeh.org/en/latest/docs/reference/models/widgets/tables.html#bokeh.models.BooleanFormatter)
    
-   [DateFormatter](https://docs.bokeh.org/en/latest/docs/reference/models/widgets/tables.html#bokeh.models.DateFormatter)
    
-   [NumberFormatter](https://docs.bokeh.org/en/latest/docs/reference/models/widgets/tables.html#bokeh.models.NumberFormatter)
    
-   [HTMLTemplateFormatter](https://docs.bokeh.org/en/latest/docs/reference/models/widgets/tables.html#bokeh.models.HTMLTemplateFormatter)
    
-   [StringFormatter](https://docs.bokeh.org/en/latest/docs/reference/models/widgets/tables.html#bokeh.models.StringFormatter)
    
-   [ScientificFormatter](https://docs.bokeh.org/en/latest/docs/reference/models/widgets/tables.html#bokeh.models.ScientificFormatter)
    

However in addition to the formatters exposed by Bokeh it is also possible to provide valid formatters built into the _Tabulator_ library. These may be defined either as a string or as a dictionary declaring the `type` and other arguments, which are passed to _Tabulator_ as the `formatterParams`:

```
tabulator_formatters = {
    'float': {'type': 'progress', 'max': 10},
    'bool': {'type': 'tickCross'}
}

pn.widgets.Tabulator(df, formatters=tabulator_formatters)

```

The list of valid _Tabulator_ formatters can be found in the [Tabulator documentation](https://tabulator.info/docs/5.5/format#format-builtin).

Note that the equivalent specification may also be applied for column titles using the `title_formatters` parameter (but does not support Bokeh `CellFormatter` types).

## Editors/Editing[#](https://panel.holoviz.org/reference/widgets/Tabulator.html#editors-editing "Permalink to this heading")

Just like the formatters, the `Tabulator` will natively understand the Bokeh `Editor` types. However, in the background it will replace most of them with equivalent editors natively supported by the _Tabulator_ library:

```
from bokeh.models.widgets.tables import CheckboxEditor, NumberEditor, SelectEditor

bokeh_editors = {
    'float': NumberEditor(),
    'bool': CheckboxEditor(),
    'str': SelectEditor(options=['A', 'B', 'C', 'D']),
}

pn.widgets.Tabulator(df[['float', 'bool', 'str']], editors=bokeh_editors)

```

Therefore it is often preferable to use one of the [_Tabulator_ editors](https://tabulator.info/docs/5.5/edit#edit) directly. Setting the editor of a column to `None` makes that column non-editable. Note that in addition to the standard _Tabulator_ editors the `Tabulator` widget also supports `'date'` and `'datetime'` editors:

```
tabulator_editors = {
    'int': None,
    'float': {'type': 'number', 'max': 10, 'step': 0.1},
    'bool': {'type': 'tickCross', 'tristate': True, 'indeterminateValue': None},
    'str': {'type': 'list', 'valuesLookup': True},
    'date': 'date',
    'datetime': 'datetime'
}

edit_table = pn.widgets.Tabulator(df, editors=tabulator_editors)

edit_table

```

When editing a cell the data stored on the `Tabulator.value` is updated and you can listen to any changes using the usual `.param.watch(callback, 'value')` mechanism. However if you need to know precisely which cell was changed you may also attach an `on_edit` callback which will be passed a `TableEditEvent` containing the:

-   `column`: Name of the edited column
    
-   `row`: Integer index of the edited row of the `value` DataFrame
    
-   `old`: Old cell value
    
-   `value`: New cell value
    

```
edit_table.on_edit(lambda e: print(e.column, e.row, e.old, e.value))

```

## Column layouts[#](https://panel.holoviz.org/reference/widgets/Tabulator.html#column-layouts "Permalink to this heading")

By default the DataFrame widget will adjust the sizes of both the columns and the table based on the contents, reflecting the default value of the parameter: `layout="fit_data_table"`. Alternative modes allow manually specifying the widths of the columns, giving each column equal widths, or adjusting just the size of the columns.

### Manual column widths[#](https://panel.holoviz.org/reference/widgets/Tabulator.html#manual-column-widths "Permalink to this heading")

To manually adjust column widths provide explicit `widths` for each of the columns:

```
custom_df = pd._testing.makeMixedDataFrame().iloc[:3, :]

pn.widgets.Tabulator(custom_df, widths={'index': 70, 'A': 50, 'B': 50, 'C': 70, 'D': 130})

```

You can also declare a single width for all columns this way:

```
pn.widgets.Tabulator(custom_df, widths=130)

```

or even use percentage widths:

```
pn.widgets.Tabulator(custom_df, widths={'index': '5%', 'A': '15%', 'B': '15%', 'C': '25%', 'D': '40%'}, sizing_mode='stretch_width')

```

### Autosize columns[#](https://panel.holoviz.org/reference/widgets/Tabulator.html#autosize-columns "Permalink to this heading")

To automatically adjust the columns depending on their content set `layout='fit_data'`:

```
pn.widgets.Tabulator(custom_df, layout='fit_data', width=400)

```

To ensure that the table fits all the data but also stretches to fill all the available space, set `layout='fit_data_stretch'`:

```
pn.widgets.Tabulator(custom_df, layout='fit_data_stretch', width=400)

```

The `'fit_data_fill'` option on the other hand won’t stretch the last column but still fill the space:

```
pn.widgets.Tabulator(custom_df, layout='fit_data_fill', width=400)

```

Perhaps the most useful of these options is `layout='fit_data_table'` (and therefore the default) since this will automatically size both the columns and the table:

```
pn.widgets.Tabulator(custom_df, layout='fit_data_table')

```

### Equal size[#](https://panel.holoviz.org/reference/widgets/Tabulator.html#equal-size "Permalink to this heading")

The simplest option is simply to allocate each column equal amount of size:

```
pn.widgets.Tabulator(custom_df, layout='fit_columns', width=650)

```

## Alignment[#](https://panel.holoviz.org/reference/widgets/Tabulator.html#alignment "Permalink to this heading")

The content of a column or its header can be horizontally aligned with `text_align` and `header_align`. These two parameters accept either a string that globally defines the alignment or a dictionary that declares which particular columns are meant to be aligned and how.

```
pn.widgets.Tabulator(df.iloc[:, :2], header_align='center', text_align={'int': 'center', 'float': 'left'}, widths=150)

```

## Styling[#](https://panel.holoviz.org/reference/widgets/Tabulator.html#styling "Permalink to this heading")

The ability to style the contents of a table based on its content and other considerations is very important. Thankfully `pandas` provides a powerful [styling API](https://pandas.pydata.org/pandas-docs/stable/user_guide/style.html), which can be used in conjunction with the `Tabulator` widget. Specifically the `Tabulator` widget exposes a `.style` attribute just like a `pandas.DataFrame` which lets the user apply custom styling using methods like `.apply` and `.applymap`. For a detailed guide to styling see the [Pandas documentation](https://pandas.pydata.org/pandas-docs/stable/user_guide/style.html).

Here we will demonstrate with a simple example, starting with a basic table:

```
style_df = pd.DataFrame(np.random.randn(4, 5), columns=list('ABCDE'))
styled = pn.widgets.Tabulator(style_df)

```

Next we define two functions which apply styling cell-wise (`color_negative_red`) and column-wise (`highlight_max`), which we then apply to the `Tabulator` using the `.style` API and then display the `styled` table:

```
def color_negative_red(val):
    """
    Takes a scalar and returns a string with
    the css property `'color: red'` for negative
    strings, black otherwise.
    """
    color = 'red' if val < 0 else 'black'
    return 'color: %s' % color

def highlight_max(s):
    '''
    highlight the maximum in a Series yellow.
    '''
    is_max = s == s.max()
    return ['background-color: yellow' if v else '' for v in is_max]

styled.style.applymap(color_negative_red).apply(highlight_max)

styled

```

## Theming[#](https://panel.holoviz.org/reference/widgets/Tabulator.html#theming "Permalink to this heading")

The Tabulator library ships with a number of themes, which are defined as CSS stylesheets. For that reason changing the theme on one table will affect all tables on the page and it will usually be preferable to see the theme once at the class level like this:

```
pn.widgets.Tabulator.theme = 'default'

```

For a full list of themes see the [Tabulator documentation](http://tabulator.info/docs/4.9/theme), however the default themes include:

-   `'simple'`
    
-   `'default'`
    
-   `'midnight'`
    
-   `'site'`
    
-   `'modern'`
    
-   `'bootstrap'`
    
-   `'bootstrap4'`
    
-   `'materialize'`
    
-   `'semantic-ui'`
    
-   `'bulma'`
    

Additionally, you may provide additional theming classes [as described here](https://tabulator.info/docs/5.5/theme#framework).

```
pn.widgets.Tabulator(df, theme='bootstrap5', theme_classes=['thead-dark', 'table-sm'])

```

## Selection/Click[#](https://panel.holoviz.org/reference/widgets/Tabulator.html#selection-click "Permalink to this heading")

The `selection` parameter controls which rows in the table are selected and can be set from Python and updated by selecting rows on the frontend:

```
sel_df = pd.DataFrame(np.random.randn(3, 5), columns=list('ABCDE'))

select_table = pn.widgets.Tabulator(sel_df, selection=[0, 2])
select_table

```

Once initialized, the `selection` parameter will return the integer indexes of the selected rows, while the `selected_dataframe` property will return a new DataFrame containing just the selected rows:

```
select_table.selection = [1]

select_table.selected_dataframe

```

|  | A | B | C | D | E |
| --- | --- | --- | --- | --- | --- |
| 1 | \-1.450679 | \-0.405228 | \-2.288315 | 1.049397 | \-0.416474 |

The `selectable` parameter declares how the selections work.

-   `True`: Selects rows on click. To select multiple use Ctrl-select, to select a range use Shift-select
    
-   `False`: Disables selection
    
-   `'checkbox'`: Adds a column of checkboxes to toggle selections
    
-   `'checkbox-single'`: Same as `'checkbox'` but disables (de)select-all in the header
    
-   `'toggle'`: Selection toggles when clicked
    
-   Any positive `int`: A number that sets the maximum number of selectable rows
    

```
pn.widgets.Tabulator(sel_df, selection=[0, 2], selectable='checkbox')

```

Additionally we can also disable selection for specific rows by providing a `selectable_rows` function. The function must accept a `DataFrame` and return a list of integer indexes indicating which rows are selectable, e.g. here we disable selection for every second row:

```
select_table = pn.widgets.Tabulator(sel_df, selectable_rows=lambda df: list(range(0, len(df), 2)))
select_table

```

To trigger events based on an exact cell that was clicked you may also register an `on_click` callback which is called whenever a cell is clicked.

```
def click(event):
    print(f'Clicked cell in {event.column!r} column, row {event.row!r} with value {event.value!r}')

select_table.on_click(click) 
# Optionally we can also limit the callback to a specific column
# select_table.on_click(click, column='A') 

```

### Freezing rows and columns[#](https://panel.holoviz.org/reference/widgets/Tabulator.html#freezing-rows-and-columns "Permalink to this heading")

Sometimes your table will be larger than can be displayed in a single viewport, in which case scroll bars will be enabled. In such cases, you might want to make sure that certain information is always visible. This is where the `frozen_columns` and `frozen_rows` options come in.

#### Frozen columns[#](https://panel.holoviz.org/reference/widgets/Tabulator.html#frozen-columns "Permalink to this heading")

When you have a large number of columns and can’t fit them all on the screen you might still want to make sure that certain columns do not scroll out of view. The `frozen_columns` option makes this possible by specifying a list of columns that should be frozen, e.g. `frozen_columns=['index']` will freeze the index column:

```
wide_df = pd._testing.makeCustomDataframe(3, 10, r_idx_names=['index'])

pn.widgets.Tabulator(wide_df, frozen_columns=['index'], width=400)

```

#### Frozen rows[#](https://panel.holoviz.org/reference/widgets/Tabulator.html#frozen-rows "Permalink to this heading")

Another common scenario is when you have certain rows with special meaning, e.g. aggregates that summarize the information in the rest of the table. In this case you may want to freeze those rows so they do not scroll out of view. You can achieve this by setting a list of `frozen_rows` by integer index (which can be positive or negative, where negative values are relative to the end of the table):

```
date_df = pd._testing.makeTimeDataFrame().iloc[:5, :2]
agg_df = pd.concat([date_df, date_df.median().to_frame('Median').T, date_df.mean().to_frame('Mean').T])
agg_df.index= agg_df.index.map(str)

pn.widgets.Tabulator(agg_df, frozen_rows=[-2, -1], height=200)

```

## Row contents[#](https://panel.holoviz.org/reference/widgets/Tabulator.html#row-contents "Permalink to this heading")

A table can only display so much information without becoming difficult to scan. We may want to render additional information to a table row to provide additional context. To make this possible you can provide a `row_content` function which is given the table row as an argument (a `pandas.Series` object) and should return a panel object that will be rendered into an expanding region below the row. By default the contents are fetched dynamically whenever a row is expanded, however using the `embed_content` parameter we can embed all the content.

Below we create a periodic table of elements where the Wikipedia page for each element will be rendered into the expanded region:

```
from bokeh.sampledata.periodic_table import elements

periodic_df = elements[['atomic number', 'name', 'atomic mass', 'metal', 'year discovered']].set_index('atomic number')

content_fn = lambda row: pn.pane.HTML(
    f'<iframe src="https://en.wikipedia.org/wiki/{row["name"]}?printable=yes" width="100%" height="200px"></iframe>',
    sizing_mode='stretch_width'
)

periodic_table = pn.widgets.Tabulator(
    periodic_df, height=350, layout='fit_columns', sizing_mode='stretch_width',
    row_content=content_fn, embed_content=True
)

periodic_table

```

The currently expanded rows can be accessed and set on the `expanded` parameter:

## Grouping[#](https://panel.holoviz.org/reference/widgets/Tabulator.html#grouping "Permalink to this heading")

Another useful option is the ability to group specific rows together, which can be achieved using `groups` parameter. The `groups` parameter should be composed of a dictionary mapping from the group titles to the column names:

```
pn.widgets.Tabulator(date_df.iloc[:3], groups={'Group 1': ['A', 'B'], 'Group 2': ['C', 'D']})

```

## Groupby[#](https://panel.holoviz.org/reference/widgets/Tabulator.html#groupby "Permalink to this heading")

In addition to grouping columns we can also group rows by the values along one or more columns:

```
from bokeh.sampledata.autompg import autompg

pn.widgets.Tabulator(autompg, groupby=['yr', 'origin'], height=240)

```

### Hierarchical Multi-index[#](https://panel.holoviz.org/reference/widgets/Tabulator.html#hierarchical-multi-index "Permalink to this heading")

The `Tabulator` widget can also render a hierarchical multi-index and aggregate over specific categories. If a DataFrame with a hierarchical multi-index is supplied and the `hierarchical` is enabled the widget will group data by the categories in the order they are defined in. Additionally for each group in the multi-index an aggregator may be provided which will aggregate over the values in that category.

For example we may load population data for locations around the world broken down by sex and age-group. If we specify aggregators over the ‘AgeGrp’ and ‘Sex’ indexes we can see the aggregated values for each of those groups (note that we do not have to specify an aggregator for the outer index since we specify the aggregators over the subgroups in this case the ‘Sex’):

```
from bokeh.sampledata.population import data as population_data 

pop_df = population_data[population_data.Year == 2020].set_index(['Location', 'AgeGrp', 'Sex'])[['Value']]

pn.widgets.Tabulator(value=pop_df, hierarchical=True, aggregators={'Sex': 'sum', 'AgeGrp': 'sum'}, height=200)

```

## Filtering[#](https://panel.holoviz.org/reference/widgets/Tabulator.html#filtering "Permalink to this heading")

A very common scenario is that you want to attach a number of filters to a table in order to view just a subset of the data. You can achieve this through callbacks or other reactive approaches but the `.add_filter` method makes it much easier.

### Constant and Widget filters[#](https://panel.holoviz.org/reference/widgets/Tabulator.html#constant-and-widget-filters "Permalink to this heading")

The simplest approach to filtering is to select along a column with a constant or dynamic value. The `.add_filter` method allows passing in constant values, widgets and Param `Parameter`s. If a widget or `Parameter` is provided the table will watch the object for changes in the value and update the data in response. The filtering will depend on the type of the constant or dynamic value:

-   scalar: Filters by checking for equality
    
-   `tuple`: A tuple will be interpreted as range, the _start_ and _end_ bounds being both included in the range. Setting one of the bounds to `None` create an open-ended bound.
    
-   `list`/`set`: A list or set will be interpreted as a set of discrete scalars and the filter will check if the values in the column match any of the items in the list.
    

As an example we will create a DataFrame with some data of mixed types:

```
filter_table = pn.widgets.Tabulator(pd._testing.makeMixedDataFrame())
filter_table

```

Now we will start adding filters one-by-one, e.g. to start with we add a filter for the `'A'` column, selecting a range from 0 to 3:

```
filter_table.add_filter((0, 3), 'A')

```

Next we add dynamic widget based filter, a `RangeSlider` which allows us to further narrow down the data along the `'A'` column:

```
slider = pn.widgets.RangeSlider(start=0, end=3, name='A Filter')
filter_table.add_filter(slider, 'A')

```

Lastly we will add a `MultiSelect` filter along the `'C'` column:

```
select = pn.widgets.MultiSelect(options=['foo1', 'foo2', 'foo3', 'foo4', 'foo5'], name='C Filter')
filter_table.add_filter(select, 'C')

```

Now let’s display the table alongside the widget based filters:

```
pn.Row(
    pn.Column(slider, select),
    filter_table
)

```

After filtering (and sorting) you can inspect the current view with the `current_view` property:

```
select.value = ['foo1', 'foo2']
filter_table.current_view

```

|  | A | B | C | D |
| --- | --- | --- | --- | --- |
| 0 | 0.0 | 0.0 | foo1 | 2009-01-01 |
| 1 | 1.0 | 1.0 | foo2 | 2009-01-02 |

### Function based filtering[#](https://panel.holoviz.org/reference/widgets/Tabulator.html#function-based-filtering "Permalink to this heading")

For more complex filtering tasks you can supply a function that should accept the DataFrame to be filtered as the first argument and must return a filtered copy of the data. Let’s start by loading some data.

```
import sqlite3

from bokeh.sampledata.movies_data import movie_path

con = sqlite3.Connection(movie_path)
movies_df = pd.read_sql('SELECT Title, Year, Genre, Director, Writer, Rating, imdbRating from omdb', con)
movies_df = movies_df[~movies_df.Director.isna()]

movies_table = pn.widgets.Tabulator(movies_df, pagination='remote', page_size=4)

```

By using the `pn.bind` function, which binds widget and `Parameter` values to a function, complex filtering can be achieved. E.g. here we will add a filter function that tests whether the string or regex is contained in the ‘Director’ column of a listing of thousands of movies:

```
director_filter = pn.widgets.TextInput(name='Director filter', value='Chaplin')

def contains_filter(df, pattern, column):
    if not pattern:
        return df
    return df[df[column].str.contains(pattern)]
    
movies_table.add_filter(pn.bind(contains_filter, pattern=director_filter, column='Director'))    

pn.Row(director_filter, movies_table)

```

### Client-side filtering[#](https://panel.holoviz.org/reference/widgets/Tabulator.html#client-side-filtering "Permalink to this heading")

In addition to the Python API the `Tabulator` widget also offers a client-side filtering API, which can be exposed through `header_filters` or by manually setting filters in the rendered table. The API for declaring header filters is almost identical to the API for defining Editors. The `header_filters` can either be enabled by setting it to `True` or by manually supplying filter types for each column. The types of filters supports all the same options as the editors, in fact if you do not declare explicit `header_filters` the `Tabulator` widget will simply use the defined `editors` to determine the correct filter type:

```
tabulator_editors = {
    'float': {'type': 'number', 'max': 10, 'step': 0.1},
    'bool': {'type': 'tickCross', 'tristate': True, 'indeterminateValue': None},
    'str': {'type': 'list', 'valuesLookup': True},
}

header_filter_table = pn.widgets.Tabulator(
    df[['float', 'bool', 'str']], height=140, width=400, layout='fit_columns',
    editors=tabulator_editors, header_filters=True
)
header_filter_table

```

When a filter is applied client-side the `filters` parameter is synced with Python. The definition of `filters` looks something like this:

```
[{'field': 'Director', 'type': '=', 'value': 'Steven Spielberg'}]

```

Try applying a filter and then inspect the `filters` parameter:

For all supported filtering types see the [_Tabulator_ Filtering documentation](http://tabulator.info/docs/4.9/filter).

If we want to change the filter type for the `header_filters` we can do so in the definition by supplying a dictionary indexed by the column names and then either providing a dictionary which may define the `'type'`, a comparison `'func'`, a `'placeholder'` and any additional keywords supported by the particular filter type.

```
movie_filters = {
    'Title': {'type': 'input', 'func': 'like', 'placeholder': 'Enter title'},
    'Year': {'placeholder': 'Enter year'},
    'Genre': {'type': 'input', 'func': 'like', 'placeholder': 'Enter genre'},
    'Director': {'type': 'input', 'func': 'like', 'placeholder': 'Enter director'},
    'Writer': {'type': 'input', 'func': 'like', 'placeholder': 'Enter writer'},
    'Rating': {'type': 'list', 'func': 'in', 'valuesLookup': True, 'sort': 'asc', 'multiselect': True},
    'imdbRating': {'type': 'number', 'func': '>=', 'placeholder': 'Enter minimum rating'},
}

filter_table = pn.widgets.Tabulator(
    movies_df.iloc[:200], pagination='local', layout='fit_columns', page_size=4, sizing_mode='stretch_width',
    header_filters=movie_filters
)
filter_table

```

## Downloading[#](https://panel.holoviz.org/reference/widgets/Tabulator.html#downloading "Permalink to this heading")

The `Tabulator` widget also supports triggering a download of the data as a CSV or JSON file depending on the filename. The download can be triggered with the `.download()` method, which optionally accepts the filename as the first argument.

To trigger the download client-side (i.e. without involving the server) you can use the `.download_menu` method which creates a `TextInput` and `Button` widget, which allow setting the filename and triggering the download respectively:

```
download_df = pd.DataFrame(np.random.randn(4, 5), columns=list('ABCDE'))

download_table = pn.widgets.Tabulator(download_df)

filename, button = download_table.download_menu(
    text_kwargs={'name': 'Enter filename', 'value': 'default.csv'},
    button_kwargs={'name': 'Download table'}
)

pn.Row(
    pn.Column(filename, button),
    download_table
)

```

Note that when `pagination='remote'` is enabled the download feature will only include the current page for technical reasons. If you want to support downloading all the data use the [`FileDownload` widget](https://panel.holoviz.org/reference/widgets/FileDownload.html).

## Buttons[#](https://panel.holoviz.org/reference/widgets/Tabulator.html#buttons "Permalink to this heading")

If you want to trigger custom actions by clicking on a table cell you may declare a set of `buttons` that are rendered in columns after all the data columns. To respond to button clicks you can register a callback using the general `on_click` method:

```
button_table = pn.widgets.Tabulator(df, buttons={
    'print': '<i class="fa fa-print"></i>',
    'check': '<i class="fa fa-check"></i>'
})

string = pn.widgets.StaticText()

button_table.on_click(
    lambda e: string.param.update(value=f'Clicked {e.column!r} on row {e.row}')
)

pn.Row(button_table, string)

```

Please note, that in a server context you will have to include the _font awesome_ css file to get the button icons rendered, i.e. use

```
pn.extension("tabulator", ..., css_files=["https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css"])

```

## Streaming[#](https://panel.holoviz.org/reference/widgets/Tabulator.html#streaming "Permalink to this heading")

When we are monitoring some source of data that updates over time, we may want to update the table with the newly arriving data. However, we do not want to transmit the entire dataset each time. To handle efficient transfer of just the latest data, we can use the `.stream` method on the `Tabulator` object:

```
stream_df = pd.DataFrame(np.random.randn(5, 5), columns=list('ABCDE'))

stream_table = pn.widgets.Tabulator(stream_df, layout='fit_columns', width=450, height=400)
stream_table

```

As example, we will schedule a periodic callback that streams new data every 1000ms (i.e. 1s) five times in a row:

```
def stream_data(follow=True):
    stream_df = pd.DataFrame(np.random.randn(5, 5), columns=list('ABCDE'))
    stream_table.stream(stream_df, follow=follow)

pn.state.add_periodic_callback(stream_data, period=1000, count=5);

```

If you are viewing this example with a live Python kernel you will be able to watch the table update and scroll along. If we want to disable the scrolling behavior, we can set `follow=False`:

```
stream_data(follow=False)

```

## Patching[#](https://panel.holoviz.org/reference/widgets/Tabulator.html#patching "Permalink to this heading")

In certain cases we don’t want to update the table with new data but just patch existing data.

```
patch_table = pn.widgets.Tabulator(df[['int', 'float', 'str', 'bool']].copy())
patch_table

```

The easiest way to patch the data is by supplying a dictionary as the patch value. The dictionary should have the following structure:

```
{
    column: [
        (index: int or slice, value),
        ...
    ],
    ...
}

```

As an example, below we will patch the `'bool'` and `'int'` columns. On the `'bool'` column we will replace the 0th and 2nd row and on the `'int'` column we replace the first two rows:

```
patch_table.patch({
    'bool': [
        (0, False),
        (2, False)
    ],
    'int': [
        (slice(0, 2), [3, 2])
    ]
}, as_index=False)

```

## Static Configuration[#](https://panel.holoviz.org/reference/widgets/Tabulator.html#static-configuration "Permalink to this heading")

Panel does not expose all options available from Tabulator, if a desired option is not natively supported, it can be set via the `configuration` argument.  
This dictionary can be seen as a base dictionary which the tabulator object fills and passes to the Tabulator javascript-library.

As an example, we can enable `clipboard` functionality and set the `rowHeight` options. `columnDefaults` takes a dictionary used to configure the columns specifically, in this example we disable header sorting with `headerSort`.

```
df = pd.DataFrame({
    'int': [1, 2, 3],
    'float': [3.14, 6.28, 9.42],
    'str': ['A', 'B', 'C'],
    'bool': [True, False, True],
    'date': [dt.date(2019, 1, 1), dt.date(2020, 1, 1), dt.date(2020, 1, 10)]
}, index=[1, 2, 3])

pn.widgets.Tabulator(df, configuration={
    'clipboard': True,
    'rowHeight': 50,
    'columnDefaults': {
        'headerSort': False,
    },
})

```

These and other available _Tabulator_ options are listed at http://tabulator.info/docs/5.4/options.

Obviously not all options will work though, especially any settable callbacks and options which are set by the internal Panel tabulator module (for example the `columns` option). Additionally it should be noted that the configuration parameter is not responsive so it can only be set at instantiation time.

___

[Open this notebook in Jupyterlite](https://panelite.holoviz.org/?path=/reference/widgets/Tabulator.ipynb) | [Download this notebook from GitHub (right-click to download).](https://raw.githubusercontent.com/holoviz/panel/main/examples/reference/widgets/Tabulator.ipynb)