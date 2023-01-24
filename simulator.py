import datetime
import numpy as np
from bokeh.plotting import figure, curdoc, show
from bokeh.models import Slider, ColumnDataSource  # type: ignore
from bokeh.layouts import column, row
# eyam plague / covid spread modelling

# init_pop = 249.5  # N_0
# susceptibles = [235.0]  # S_0
# infectives = [14.5]  # I_0
# deaths = [0.0]
# TRANS_rate = 0.01776  # beta const
# DEATH_rate = 2.9  # alpha const
# timestep = .1  # dt in months
# t = 0
# lim = 12  # how many months to simulate


def smoothen(data, dates):
    # new_times = np.arange(np.datetime64(datetime.date(1066, 6, 3)),
    #                       np.timedelta64(
    #                           datetime.timedelta(days=(4+.1)*30)),
    #                       np.timedelta64(datetime.timedelta(days=.5*30)))
    dates = list(map(np.int64, dates))
    coefficients = np.polyfit(dates, data, deg=4)
    y_ = np.polyval(coefficients, dates)
    return y_


def simulate(init_pop, s_0, i_0, trans_rate, death_rate, dt, lim, epsilon=.1):
    """
    Simulates spread of disease using equations from https://www.youtube.com/watch?v=Qlfv77GPS5Y
    time is in months (365/12 days)
    Tries to fit Mompesson data from 1666
    No natural immunity is assumed
    """

    time_count = int(lim/dt)
    real_times = np.arange(np.datetime64(datetime.date(1066, 6, 3)),
                           datetime.timedelta(days=(lim+dt)*30), datetime.timedelta(days=dt*30))

    susceptibles = [s_0]
    infectives = [i_0]
    deaths = [0.0]
    for i in range(time_count):
        curr_susceptibles = susceptibles[-1]
        curr_infectives = infectives[-1]
        curr_deaths = deaths[-1]
        susceptibles.append(curr_susceptibles-(trans_rate *
                            curr_susceptibles*curr_infectives*dt))
        infectives.append((curr_infectives+dt*(trans_rate *
                                               curr_susceptibles *
                                               curr_infectives-death_rate*curr_infectives)))
        deaths.append(curr_deaths+death_rate*curr_infectives*dt)
        assert curr_susceptibles+curr_infectives+curr_deaths - init_pop < .01

        if abs(susceptibles[-2] - susceptibles[-1]) < epsilon and abs(infectives[-2] - infectives[-1]) < epsilon:
            real_times = real_times[:i+2]
            break

    return real_times, susceptibles, infectives, deaths


def callback(_attr, _old, _new):
    times, susceptibles, infectives, deaths = simulate(
        249.5, 235., 14.5, beta.value, alpha.value, dt=.01, lim=12, epsilon=epsilon.value)
    source.data = dict(
        times=times, susceptibles=susceptibles, infectives=infectives, deaths=deaths)


# TODO: use bokeh server to make it interactive
# TODO: import and best fit real data(covid/eyam)
# using scipy.optimise().curve_fit() or numpy(?)
# TODO: add more details, e.g. make alpha, beta, variable
# based on season, evolution, lockdowns, etc.
# human intervention could be in 3 levels,
# e.g. 1)symptomatic isolation/masking,
# 2) contact tracing, animal culling
# 3) Full lockdowns, vaccine rollouts
#
# TODO: stochastic model with probability map
# TODO: tell bokeh datetimes, not floats
server_mode = True
times, susceptibles, infectives, deaths = simulate(
    249.5, 235., 14.5, .01776, 2.9, dt=.1, lim=12)

months = ["Jan", "Feb", "Mar", "Apr", "May", "June",
          "July", "Aug", "Sept", "Oct", "Nov", "Dec"]
# Year, month, day, S, I, D, ln( S0 / S ), I0+S0 – I - S
data = [(datetime.date(1066, months.index("July"), 3),
        0.00, 235, 14.5, 0, 0.00, 0.00),
        (datetime.date(1066, months.index("July"), 19),
        0.51, 201, 22, 26.5, 0.16, 26.50),
        (datetime.date(1066, months.index("Aug"), 3),
        1.02, 153.5, 29, 67, 0.43, 67.00),
        (datetime.date(1066, months.index("Aug"), 19),
        1.53, 121, 21, 107.5, 0.66, 107.50),
        (datetime.date(1066, months.index("Sept"), 3),
        2.04, 108, 8, 133.5, 0.78, 133.50),
        (datetime.date(1066, months.index("Sept"), 19),
        2.55, 97, 8, 144.5, 0.88, 144.50),
        (datetime.date(1066, months.index("Oct"), 20),
        3.57, 83, 0, 166.5, 1.04, 166.50)]

dates = [np.datetime64(datum[0]) for datum in data]

source = ColumnDataSource(data=dict(
    times=times, susceptibles=susceptibles, infectives=infectives, deaths=deaths))
other_tools = "pan, box_zoom, save, reset, help,"
p = figure(title="Simulated Eyam population",
           x_axis_label='date', x_axis_type="datetime",
           y_axis_label='people', tools="wheel_zoom, "+other_tools)

p.line("times", "susceptibles", source=source, color="blue",
       legend_label="susceptibles", line_width=2)
p.line("times", "infectives", source=source, color="green",
       legend_label="infectives", line_width=2)
p.line("times", "deaths", source=source, color="orange",
       legend_label="deaths", line_width=2)


p.x(dates, [datum[2] for datum in data], color="blue", size=15)
p.x(dates, [datum[3] for datum in data], color="green", size=15)
p.x(dates, [datum[4] for datum in data], color="orange", size=15)

other_tools = "pan, box_zoom, save, reset, help,"
scatter = figure(title="Real Eyam population",
                 x_axis_type="datetime", x_axis_label='time',
                 y_axis_label='people', tools="wheel_zoom, "+other_tools)

scatter.circle(dates, [datum[2] for datum in data], color="blue")
scatter.circle(dates, [datum[3] for datum in data], color="green")
scatter.circle(dates, [datum[4] for datum in data], color="orange")
scatter.line(dates, smoothen([datum[2]
                              for datum in data], dates), color="blue")
scatter.line(dates, smoothen([datum[3]
                              for datum in data], dates), color="green")
scatter.line(dates, smoothen([datum[4]
                              for datum in data], dates), color="orange")


if server_mode:
    alpha = Slider(start=0, end=6.0, value=3, step=.05, title="death rate")
    beta = Slider(start=0, end=.1, value=.01776,
                  step=.001, title="infection rate")
    epsilon = Slider(start=0, end=0.2, value=.05,
                     step=.005, title="limit of graph")

    alpha.on_change('value', callback)
    beta.on_change('value', callback)
    epsilon.on_change('value', callback)

    # put the button and plot in a layout and add to the document
    curdoc().add_root(column(alpha, beta, epsilon, row(p, scatter)))  # type: ignore
else:
    # can use scatter plot and line of best fit
    # (https://stackoverflow.com/questions/54603873/bokeh-plot-regression-lines-on-scatter-plot)
    # https://docs.bokeh.org/en/latest/docs/user_guide/basic/scatters.html#scatter-plots

    show(column(p, scatter))

# use stochastic model
# np.random.poisson()
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.lsq_linear.html
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.least_squares.html
# then render to heatmap:
# https://docs.bokeh.org/en/latest/docs/user_guide/plotting.html#color-mapped-images
