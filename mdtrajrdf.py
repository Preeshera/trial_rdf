import tempfile, os
import argparse
import numpy as np
import mdtraj as md

try:
    import matplotlib

    matplotlib.use('agg')  # no interactive plotting, only save figures
    import pylab

    have_matplotlib = True
except ImportError:
    have_matplotlib = False


parser = argparse.ArgumentParser(description='Generate the RDF g(f) of a lammpstrj file')
parser.add_argument('--trajfile', help='Path to the lammpstrj file',required=True)
parser.add_argument('--pdbfile', help='Path to the pdb file',required=True)
parser.add_argument('--pairselect1', help='Atom selection query for first part of pair',required=True)
parser.add_argument('--pairselect2', help='Atom selection query for first part of pair',required=True)
parser.add_argument('--outdir', help='Directory to output files into', default='./output')
parser.add_argument('--outname', help='Name for Output Files',default='rdf')

args = parser.parse_args()

traj = md.load(args.trajfile,top=args.pdbfile)
print("Trajectory and Topology Loaded")
pairs = traj.top.select_pairs(args.pairselect1, args.pairselect2)
radii, rdf = md.geometry.rdf.compute_rdf(traj, pairs)
print("Computed")

outfile = args.outdir+'/'+args.outname+'.dat'
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
    pylab.savefig(args.outdir+'/'+args.outname+'.pdf')
    pylab.savefig(args.outdir+'/'+args.outname+'.png')