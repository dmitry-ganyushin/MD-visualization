This is a script to convert molecular trajectories data from the ADIOS2 BP4
format to the crd format used by the VMD visualization program. 

usage: bp2crd  name_of_bp_file name_of_crd_file


The VMD program requires two files to make visualization: a pdb 
(a structure information file) file and a file with trajectories.

The structure file can be obtained using the NWCHEM version 700 
using the following input file
 
echo
start .trypsin
 
analysis
  system trypsin_md
  reference trypsin_md.rst
  file trypsin_md.trj
  write 1 solute trypsin_md.pdb
  frames 1  10 1
  copy solute trypsin_md.crd
end
 
task analysis
