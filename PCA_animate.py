#! python 

import sys
import getopt
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation


def read_data_fullAPI(INPUT_FILENAME, VARNAME, start_step=None, end_step=None):
    import adios2
    data = []
    n_atoms = 306

    adios = adios2.ADIOS()
    ioReadBP = adios.DeclareIO("pca")
    fh = ioReadBP.Open(INPUT_FILENAME, adios2.Mode.Read)
    var = ioReadBP.InquireVariable(VARNAME)
    if start_step is None:
        start_step = 1
    if end_step is None:
        end_step = fh.Steps()
        print(end_step)
    print(var.Type())
    print(var.Shape())
    var.SetStepSelection([0, 1])
    var.SetSelection([[0, 0, 0], [end_step - start_step, n_atoms, 3]])
    data_var = np.zeros((end_step - start_step, n_atoms, 3), dtype=np.double)
    fh.Get(var, data_var)
    fh.PerformGets()

    data = data_var
    print(type(data))
    print(type(data[0]))
    print(len(data))

    return data


def animate_plot(iteration, data, scatters):
    """
    Update the data held by the scatter plot and therefore animates it.

    Args:
        iteration (int): Current iteration of the animation
        data (list): List of the data positions at each iteration.
        scatters (list): List of all the scatters (One per element)

    Returns:
        list: List of scatters (One per element) with new coordinates
    """
    print("Iteration = {}".format(iteration))

    for i in range(data[0].shape[0]):
        scatters[i]._offsets3d = (data[iteration][i, 0:1], data[iteration][i, 1:2], data[iteration][i, 2:])
    return scatters


def main(data, name=None, save=None):
    """
    Creates the 3D plot and animates it with the input data.

    Args:
        data (list): List of the data positions at each iteration.
        save (bool): Whether to save the recording of the animation. (Default to False).
    """

    # Attaching 3D axis to the figure
    fig = plt.figure()
    ax = p3.Axes3D(fig)

    # Initialize scatters
    scatters = [ax.scatter(data[0][i, 0:1], data[0][i, 1:2], data[0][i, 2:], color="red") for i in
                range(data[0].shape[0])]
    print("Scatters = {}".format(len(scatters)))

    # Number of iterations
    iterations = len(data)

    # Setting the axes properties
    ax.set_xlim3d([-3, 3])
    ax.set_xlabel('X')

    ax.set_ylim3d([-3, 3])
    ax.set_ylabel('Y')

    ax.set_zlim3d([-3, 3])
    ax.set_zlabel('Z')

    ax.set_title(name)

    # Provide starting angle for the view.
    ax.view_init(25, 10)

    ani = animation.FuncAnimation(fig, animate_plot, iterations, fargs=(data, scatters),
                                  interval=1, blit=False, repeat=False)
    if save is not None:
        writer = animation.FFMpegWriter(fps=30, metadata=dict(artist=''), bitrate=1800)
        ani.save(save + '.mp4', writer=writer)

    plt.show()


def printUsage():
    print('PCA_Animante.py -i <inputfile> -v <variable name> -s <first_step-lats_step> -m movie_name')


if __name__ == "__main__":
    INPUT_FILENAME = None
    VARIABLE_NAME = None
    FIRST_STEP = None
    LAST_STEP = None
    MOVIE_NAME = None
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:v:s:m:", ["help", "input", "var", "steps", "movie"])
    except getopt.GetoptError:
        printUsage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            printUsage()
            sys.exit()
        elif opt in ("-i", "--input"):
            INPUT_FILENAME = arg
        elif opt in ("-v", "--var"):
            VARIABLE_NAME = arg
        elif opt in ("-s", "--steps"):
            FIRST_STEP = int(arg.split("-")[0])
            LAST_STEP = int(arg.split("-")[1])
        elif opt in ("-m", "--movie"):
            MOVIE_NAME = arg

    if INPUT_FILENAME is None or VARIABLE_NAME is None:
        printUsage()
        sys.exit(1)

    data = read_data_fullAPI(INPUT_FILENAME, VARIABLE_NAME, FIRST_STEP, LAST_STEP)

    print("Number of steps: {}".format(len(data)))
    main(data, name=VARIABLE_NAME, save=MOVIE_NAME)

    sys.exit(0)
