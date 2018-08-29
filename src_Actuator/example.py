'''
tester for topology compliant optimization code
'''
import time
import math

from loads import Inverter
from constraints import DensityConstraint
from fesolvers import CvxFEA, SciPyFEA
from topopt import Topopt
from plotting import Plot

if __name__ == "__main__":
    t = time.time()
    # material properties
    young = 1
    poisson = 0.3
    ext_stiff = 0.1

    # constraints
    Emin = 1e-9
    volfrac = 0.3
    move = 1

    # mesh dimensions
    nelx = 40
    nely = 20

    # optimization settings
    penal = 3.0
    rmin = 1.5
    loopy = 10  # math.inf
    delta = 0.001

    # loading/problem
    load = Inverter(nelx, nely, ext_stiff)

    # constraints5
    den_con = DensityConstraint(load, move, volume_frac=volfrac, Emin=Emin)

    # optimizer
    verbose = True
    fesolver = SciPyFEA(verbose=verbose)
    optimizer = Topopt(fesolver, young, poisson, verbose=verbose)

    # compute
    filt = 'density'
    history = False
    x = optimizer.init(load, den_con)
    x, x_more = optimizer.layout(load, den_con, x, penal, rmin, delta, loopy, filt, history)

    print('Elapsed time is: ', time.time() - t, 'seconds.')

    if history:
        x_history = x_more
        loop = len(x_history)
    else:
        loop = x_more
        x_history = None

    # save
    if x_history:
        import imageio
        imageio.mimsave('topopt.gif', x_history)

    # plot
    pl = Plot(x, load, nelx, nely)
    pl.figure()
    pl.loading()
    pl.boundary()
    pl.show()
