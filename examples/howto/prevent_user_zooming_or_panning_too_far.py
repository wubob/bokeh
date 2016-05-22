from datetime import date, timedelta
import numpy as np
from bokeh.charts import HeatMap
from bokeh.io import output_file, show, vplot, hplot
from bokeh.models import Range1d, LinearAxis
from bokeh.plotting import figure
from bokeh.sampledata.stocks import AAPL, GOOG

output_file('prevent_user_zooming_or_panning_too_far.html',
            title="prevent_user_zooming_or_panning_too_far.py example")

## Plot where bounds are set by auto
N = 4000
x = np.random.random(size=N) * 100
y = np.random.random(size=N) * 100
radii = np.random.random(size=N) * 1.5
colors = ["#%02x%02x%02x" % (int(r), int(g), 150) for r, g in zip(50 + 2 * x, 30 + 2 * y)]
plot_default = figure(tools='pan, box_zoom, wheel_zoom, reset', title="Cannot pan outside data (bounds='auto')")
plot_default.scatter(x, y, radius=radii, fill_color=colors, fill_alpha=0.6, line_color=None)
###### -- ranges set here -- ########
plot_default.x_range.bounds = 'auto'
plot_default.y_range.bounds = 'auto'
###### -- end -- ########


## Plot where ranges are manually set

###### -- ranges set here -- ########
x_range = Range1d(0, 3, bounds=(-1, 3.5), zoom_bounds=(1.5, 3))
y_range = Range1d(0, 3, bounds=(-0.5, 4), zoom_bounds=(1.5, 3))
###### -- end -- ########
plot_range = figure(tools='pan, wheel_zoom, reset', x_range=x_range, y_range=y_range, title="Manual bounds x:(-1, 3.5) y:(-0.5, 4) zoom_bounds: (1.5, 3)")
plot_range.rect(x=[1, 2], y=[1, 1], width=0.9, height=0.9)


## Manually set y_max only

###### -- ranges set here -- ########
x_range = Range1d(0, 3)
y_range = Range1d(0, 3, bounds=(None, 4))
###### -- end -- ########
plot_range_un = figure(tools='pan, wheel_zoom, reset', x_range=x_range, y_range=y_range, title="Unbounded (except for y_max=4)")
plot_range_un.rect(x=[1, 2], y=[1, 1], width=0.9, height=0.9, color='#043A8D')



## Bounded on reversed ranges (except for y_max)

###### -- ranges set here -- ########
x_range = Range1d(3, 0, bounds=(-1, 3.5), zoom_bounds=(1.5, None))
y_range = Range1d(3, 0, bounds=(-0.5, 4), zoom_bounds=(1.5, None))
###### -- end -- ########
plot_range_rev = figure(tools='pan, wheel_zoom, reset', x_range=x_range, y_range=y_range, title="Manual bounds x:(-1, 3.5) y:(-0.5, 4) min_range:1.5 (reverse ranges)")
plot_range_rev.rect(x=[1, 2], y=[1, 1], width=0.9, height=0.9, color='#8CBEDB')



## Chart where limits are set on a categorical range
fruits = {
    'fruit': [
        'apples', 'apples', 'apples', 'apples', 'apples',
        'pears', 'pears', 'pears', 'pears', 'pears',
        'bananas', 'bananas', 'bananas', 'bananas', 'bananas'
    ],
    'fruit_count': [
        4, 5, 8, 12, 4,
        6, 5, 4, 8, 7,
        1, 2, 4, 8, 12
    ],
    'year': [
        '2009', '2010', '2011', '2012', '2013',
        '2009', '2010', '2011', '2012', '2013',
        '2009', '2010', '2011', '2012', '2013']
}

plot_cat_unbounded = HeatMap(fruits, y='year', x='fruit', values='fruit_count', stat=None, title="Heatmap (unbounded)")

plot_cat_autobounded = HeatMap(fruits, y='year', x='fruit', values='fruit_count', stat=None, title="Heatmap (autobounded)")
###### -- ranges set here -- ########
plot_cat_autobounded.x_range.bounds = 'auto'
plot_cat_autobounded.y_range.bounds = 'auto'
###### -- end -- ########

plot_cat_bounded = HeatMap(
    fruits, y='year', x='fruit', values='fruit_count', stat=None,
    title="Heatmap with bounds x:['apples', 'pears'], y:['2009', '2010', '2013']"
)
###### -- ranges set here -- ########
plot_cat_bounded.x_range.bounds = ['apples', 'pears']
plot_cat_bounded.y_range.bounds = ['2009', '2010', '2013']
###### -- end -- ########


## Plot with multiple ranges that are bounded
x = np.array(AAPL['date'], dtype=np.datetime64)
x = x[0:1000]
apple_y = AAPL['adj_close'][0:1000]
google_y = GOOG['adj_close'][0:1000]

###### -- ranges set here -- ########
x_range = Range1d(
    start=date(2000, 1, 1), end=date(2004, 12, 31),
    bounds=(date(2001, 1, 1), date(2006, 12, 31)),
    zoom_bounds=(timedelta(100), timedelta(1000000)),
)
y_range = Range1d(start=00, end=40, bounds=(10, 60))
y_range_extra = Range1d(start=300, end=700, bounds=(200, 1000))
###### -- end -- ########

plot_extra = figure(x_axis_type="datetime", x_range=x_range, y_range=y_range, title="Multiple ranges x:(2001/1/1, 2006/12/31), y1:(10, 60), y2:(200, 1000)")
plot_extra.line(x, apple_y, color='lightblue')
plot_extra.extra_y_ranges = {'goog': y_range_extra}
plot_extra.line(x, google_y, color='pink', y_range_name='goog')
plot_extra.add_layout(LinearAxis(y_range_name="goog", major_label_text_color='pink'), 'left')

# Tweak the formats to make it all readable
plots = [plot_default, plot_range, plot_range_un, plot_range_rev, plot_cat_autobounded, plot_cat_unbounded, plot_cat_bounded, plot_extra]
for plot in plots:
    plot.title_text_font_size = '12pt'

show(vplot(plot_default, hplot(plot_range, plot_range_un, plot_range_rev), hplot(plot_cat_unbounded, plot_cat_autobounded, plot_cat_bounded), plot_extra))
