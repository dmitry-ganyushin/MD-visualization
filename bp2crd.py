#!/usr/bin/python3
import sys

import adios2

scale_factor = 10

def trajectories_bp_to_crd(bp_file_name, crd_file_name):

    with adios2.open(bp_file_name, "r") as fh:

        with open(crd_file_name, "w") as w:
            w.write("AMBER trajectory file\n")

            for fstep in fh:
                step = fstep.current_step()
                print("processing step: {}".format(step))
                coords_solute = fstep.read("solute/coords")
                coords_solvent = fstep.read("solvent/coords")

                out_string = list();
                for atom_number in range(0, coords_solute.shape[0]):
                    out_string.append(coords_solute[atom_number][0] * scale_factor)
                    out_string.append(coords_solute[atom_number][1] * scale_factor)
                    out_string.append(coords_solute[atom_number][2] * scale_factor)
                last = len(out_string) - len(out_string) % 10
                for pos in range(0, last, 10):
                    w.write(
                        "{:6.3} {:6.3} {:6.3} {:6.3} {:6.3} {:6.3} {:6.3} {:6.3} {:6.3} {:6.3}\n".format(
                            out_string[pos],
                            out_string[
                                pos + 1],
                            out_string[
                                pos + 2],
                            out_string[
                                pos + 3],
                            out_string[
                                pos + 4],
                            out_string[
                                pos + 5],
                            out_string[
                                pos + 6],
                            out_string[
                                pos + 7],
                            out_string[
                                pos + 8],
                            out_string[
                                pos + 9]))

                for pos in range(last, len(out_string)):
                    w.write("%6.3f " % out_string[pos])
                w.write("\n")

    return

def print_usage():
    print("usage: bp2crd  name_of_bp_file name_of_crd_file")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print_usage()
        sys.exit(1)
    bp_file_name = sys.argv[1]
    crd_file_name = sys.argv[2]
    trajectories_bp_to_crd(bp_file_name, crd_file_name)
