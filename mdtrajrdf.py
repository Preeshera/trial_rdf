import tempfile, os

import numpy as np

import mdtraj as md

try:
    import matplotlib

    matplotlib.use('agg')  # no interactive plotting, only save figures
    import pylab

    have_matplotlib = True
except ImportError:
    have_matplotlib = False


traj = md.load('../nptpro.lammpstrj',top='../data2.pdb')
print("Loaded")
pairs = traj.top.select_pairs('name NTB', 'name OCS')
radii, rdf = md.geometry.rdf.compute_rdf(traj, pairs)
print("Computed")

outfile = './output/rdf.dat'
with open(outfile, 'w') as output:
    for radius, gofr in zip(radii, rdf):
        output.write("{radius:8.3f} \t {gofr:8.3f}\n".format(**vars()))
print ("g(r) data written to {outfile!r}".format(**vars()))

if have_matplotlib:
    matplotlib.rc('font', size=14)
    matplotlib.rc('figure', figsize=(5, 4))
    pylab.clf()
    pylab.plot(radii, rdf, linewidth=3)
    pylab.xlabel(r"distance $r$ in $\AA$")
    pylab.ylabel(r"radial distribution function $g(r)$")
    pylab.savefig("./figures/rdf.pdf")
    pylab.savefig("./figures/rdf.png")
    print ("Figure written to ./figures/rdf.{pdf,png}")