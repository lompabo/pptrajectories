#!/usr/bin/env python
# -*- coding: utf-8 -*-

from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
## for Palatino and other serif fonts use:
# rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)

import numpy as np
import itertools
from numpy import random
from scipy import stats
from matplotlib import pyplot as plt
from scipy.stats import gaussian_kde
import sys

if __name__ == '__main__':
    # radius of the red circle
    r = 1
    # (twin) parameters for the beta distribution
    a = 2
    bdist = stats.beta(a, a, loc=-r, scale=2*r)
    # intervals for the discretization of each dimension
    n = 51
    # Number of samples
    ns = 200 * n**2
    # base plot size
    pscale = 5

    # ========================================================================
    # Versatility of the Beta distribution
    # ========================================================================

    # Parametrization 1
    plt.figure(figsize=(2*pscale, pscale))
    plt.subplot(121)
    plt.title(r'Probability Density Function $f_{\alpha = \beta = 2}(x)$')
    d = np.linspace(0, 1)
    plt.plot(d, stats.beta.pdf(d, a=2, b=2))
    # q1, q3 = stats.beta.ppf([0.25, 0.75], a=3, b=3)
    # plt.vlines([q1, q3], 0, 3, 'y')
    plt.ylim((0, 3))
    plt.grid()
    # Parametrization 2
    plt.subplot(122)
    plt.title(r'Probability Density Function $f_{\alpha = b = 6}(x)$')
    d = np.linspace(0, 1)
    plt.plot(d, stats.beta.pdf(d, a=6, b=6))
    # q1, q3 = stats.beta.ppf([0.25, 0.75], a=6, b=6)
    # plt.vlines([q1, q3], 0, 3, 'y')
    plt.ylim((0, 3))
    plt.grid()
    plt.savefig('beta.png')

    # ========================================================================
    # Goal: highest probabilities in the _center_
    # ========================================================================

    # Compute distance from the center in the discretized target 2-D space
    # NOTE the initial computations will be done on a linearized vectors
    xvals = np.linspace(-r, r, n)
    yvals = np.linspace(-r, r, n)
    dmap = np.array([(x**2 + y**2)
        for x, y in itertools.product(xvals, yvals)])
    dmap = np.sqrt(dmap)
    # Compute probability density function on the target 2-D space
    pdf = np.zeros((n**2, ))
    mask = dmap < abs(r) # NOTE the probability is zero when the distance
                         # is outside the bounds of the beta distribution
    pdf[mask] = bdist.pdf(dmap[mask])
    # Normalize the Probability Density Function (this is _very_ important)
    pdf = pdf / pdf.sum()
    # Put the pdf in 2-D form
    pdf = pdf.reshape((n, n))
    # Print maximum probability for and individual cell
    # NOTE this will be very small
    pmax = pdf.max()
    print('Max cell prob: ', pmax)
    
    # Show the probability density function
    plt.close('all')
    plt.figure(figsize=(2*pscale, pscale))
    plt.subplot(121)
    plt.title(r'Joint PDF $f(d, \phi)$')
    plt.pcolor(pdf, cmap='gray', vmin=0, vmax=pmax)
    plt.gca().set_xticks([0, n/2, n-1])
    plt.gca().set_xticklabels(['-r', '0', 'r'])
    plt.gca().set_yticks([0, n/2, n-1])
    plt.gca().set_yticklabels(['r', '0', '-r'])
    phi = np.linspace(0, 2*np.pi, 360)
    plt.plot(n/2 + (n/2-1) * np.cos(phi), n/2 + (n/2-1) * np.sin(phi), 'r', linewidth=1)
    # ry = abs(bdist.ppf(0.25))
    # plt.plot(n/2 + ry * (n/2-1) * np.cos(phi), n/2 + ry * (n/2-1) * np.sin(phi), 'y', linewidth=1)
    plt.axis('equal')
    plt.xlim(0, n)
    plt.ylim(0, n)
    # Plot conditional probability
    plt.subplot(122)
    d = np.linspace(-r, r)
    plt.title(r'Conditional PDF of d: $f(d \mid \phi = 0)$')
    plt.plot(d, bdist.pdf(d), 'r')
    # plt.vlines(bdist.ppf([0.25, 0.75]), plt.ylim()[0], plt.ylim()[1], 'y')
    plt.gca().set_xticks([-r, 0, r])
    plt.gca().set_xticklabels(['-r', '0', 'r'])
    plt.grid()
    plt.savefig('fig1.png')
    # plt.show()

    # ========================================================================
    # Wrong Sampling (conditional d, then phi)
    # ========================================================================

    # Wrong sampling
    d = np.linspace(-r, r, 101)
    prob1 = bdist.pdf(d)
    prob1 /= prob1.sum()
    dvals1 = np.random.choice(d, ns, p=prob1)
    # dvals1 = bdist.rvs(ns)
    phi = np.pi * np.random.rand(ns)
    xvals1 = dvals1 * np.cos(phi)
    yvals1 = dvals1 * np.sin(phi)

    plt.close('all')
    plt.figure(figsize=(2*pscale, pscale))
    # Show the probability along a section
    plt.subplot(121)
    plt.title(r'Discretized Conditional Distribution of $d$')
    plt.step(d, prob1, where='mid')
    plt.gca().set_xticks([-r, 0, r])
    plt.gca().set_xticklabels(['-r', '0', 'r'])
    plt.grid()
    # plt.ylim(0,1)
    # Plot 2-D histogram
    plt.subplot(122)
    plt.title(r'2D Histogram (conditional $d$, then $\phi$)')
    plt.hist2d(xvals1, yvals1,
            bins=[np.linspace(-r,r,n), np.linspace(-r,r,n)], cmap='gray')
    plt.gca().set_xticks([-1, 0, 1])
    plt.gca().set_xticklabels(['-r', '0', 'r'])
    plt.gca().set_yticks([-1, 0, 1])
    plt.gca().set_yticklabels(['r', '0', '-r'])
    phi = np.linspace(0, 2*np.pi, 360)
    plt.plot(r * np.cos(phi), r * np.sin(phi), 'r', linewidth=1)
    plt.xlim(-1, 1)
    plt.ylim(-1, 1)
    plt.savefig('fig2.png')
    # plt.show()

    # ========================================================================
    # Correct Sampling (sample d with marginalized phi, then phi)
    # ========================================================================

    # Correct sampling
    d = np.linspace(-r, r, 101)
    prob2 = bdist.pdf(d) * np.pi * np.abs(d)
    prob2 /= prob2.sum()
    dvals2 = np.random.choice(d, ns, p=prob2)
    phi = np.pi * np.random.rand(ns)
    xvals1 = dvals2 * np.cos(phi)
    yvals1 = dvals2 * np.sin(phi)
    # Compute the (approximate) first quartile
    q1 = d[np.where(prob2.cumsum() > 0.25)[0][0]]

    plt.close('all')
    plt.figure(figsize=(2*pscale, pscale))
    # Show the probability along a section
    plt.subplot(121)
    plt.title(r'Discretized Distribution of $d$ (marginalized $\phi$)')
    plt.step(d, prob2, where='mid')
    # plt.vlines([q1, q3], plt.ylim()[0], plt.ylim()[1], 'y')
    plt.vlines([q1, abs(q1)], plt.ylim()[0], plt.ylim()[1], 'y')
    plt.gca().set_xticks([-r, 0, r])
    plt.gca().set_xticklabels(['-r', '0', 'r'])
    plt.grid()
    # plt.ylim(0,1)
    # Plot 2-D histogram
    plt.subplot(122)
    plt.title(r'2D Histogram ($d$, then $\phi$)')
    plt.hist2d(xvals1, yvals1,
            bins=[np.linspace(-r,r,n), np.linspace(-r,r,n)], cmap='gray')
    plt.gca().set_xticks([-1, 0, 1])
    plt.gca().set_xticklabels(['-r', '0', 'r'])
    plt.gca().set_yticks([-1, 0, 1])
    plt.gca().set_yticklabels(['r', '0', '-r'])
    phi = np.linspace(0, 2*np.pi, 360)
    plt.plot(r * np.cos(phi), r * np.sin(phi), 'r', linewidth=1)
    ry = abs(q1)
    plt.plot(ry * np.cos(phi), ry * np.sin(phi), 'y', linewidth=1)
    plt.xlim(-1, 1)
    plt.ylim(-1, 1)
    plt.savefig('fig3.png')
    # plt.show()
    sys.exit()

