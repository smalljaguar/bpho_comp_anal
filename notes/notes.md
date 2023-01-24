# Week 1

# The Eyam Equations

Variables are:
Susceptibles, Recovered, Infected, Dead
$[S,R,I,D] \in \N$
&nbsp;
### $ S+I+D+R = P_0 $
&nbsp;
### $ \frac{d(R+D)}{dt} = \alpha I $
### $ \frac {dS} {dt} = - \beta SI $
### $ \frac {dI} {dt} = \beta SI - \alpha I = I(\beta S - \alpha) $

# Susceptible threshold
### $ \rho = \frac {\alpha}{\beta}$
If $ S > \rho$ epidemic grows
If $ S < \rho$ epidemic shrinks

# Iterative solution via Euler numeric method

approximate equations by making $\Delta t$ finitely small
e.g. $\alpha = 2.894, \beta = \frac {\alpha} {163.3}$
$t=0, S_0=235, I_0 = 14.5, D_0 = 0$
$t_{n+1} = t_n + \Delta t$
$S_{n+1} = S_n -\beta S_n I_n \Delta t$
$I_{n+1} = I_n + (\beta S_n I_n - \alpha I_n) \Delta t$ 
$D_{n+1} = D_n + \alpha I_n \Delta T$

Stochastic Eyam model
Obviously the changes to $S, I, D$ are **discrete**, *not* continuous values. Also,
one expects the spread of infection to be a **random** process. Returning to
Brauer's model, we can use the **expected** values of $S,I$ and $D$ changes within
time interval $\Delta t$ to be the mean (and variance ) of a **Poisson distribution**. If
we can sample this distribution, then *between each time step* we should
have a *representative discrete change* of $S,I,D$ that incorporates both the
model and the idea of randomness.

$\Delta S = -x, \Delta I_1 = x$
$x ~ Po(\beta S I \Delta T)$
$\Delta D = y$
$y ~ Po(\alpha I \Delta t)$
$\Delta I_2 = -y \therefore \Delta I = \Delta I_1 + \Delta I_2 $

# Covid-19
One can estimate the number of Covid-19
infectives from the cumulative deaths:

## $ I_n = \frac{1}{ka} \frac {dD}{dt} \approx \frac{1}{ka} \frac {D_{n+1}-D_{n-1}}{t_{n+1}-t_{n-1}}$
Numpy can do this for us with `np.gradient(np.cumsum(data))`
Can get data from **Our World in Data**, or direct from **John Hopkins**

Maybe copy some ideas from Plague Inc with modelling spread? E.g. variable transmission/death rate as disease evolves, superspreader events, multiple methods of transmission, government policy etc.

An analysis from 2016: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4874723/

# Week 2