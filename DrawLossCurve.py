import numpy as np
import re
import matplotlib.patches as mpatches
from argparse import ArgumentParser
from matplotlib import pylab as plt
import pdb

#Draw loss curves with many output in a file
#This example has 3 loss curves

def main(files):
    plt.style.use('ggplot')
    fig, ax1 = plt.subplots()
    ax1.set_ylim([0.002,8])
    ax1.set_xlabel('Iteration')
    ax1.set_ylabel('Training Loss')
    temp=[]
    temp.append(files.files1)
    for i, log_file in enumerate(temp):
         loss_iterations, losses, losses2, losses3, losses4 = parse_log(log_file)
         disp_results(fig, ax1, loss_iterations, losses, losses2, losses3, losses4, color_ind=i)
    patch1 = mpatches.Patch(color=colors[0], label=' loss')
    patch2 = mpatches.Patch(color=colors[1], label='2c_4f loss')
    patch3 = mpatches.Patch(color=colors[2], label='2c_5c loss')
    patch4 = mpatches.Patch(color=colors[3], label='3d_5c loss')
    plt.legend(handles=[patch1, patch2, patch3, patch4])
    plt.show()


def parse_log(log_file):
    with open(log_file, 'r') as log_file:
        log = log_file.read()

    
    loss_pattern = r"Iteration (\d+) \(.*\), loss = .*\n.* Train net output #0: prob = ([+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?) .*\n.* Train net output #1: prob_2c_4f = ([+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?) .*\n.* Train net output #2: prob_2c_5c = ([+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?) .*\n.* Train net output #3: prob_3d_5c = ([+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?)"
    losses = []
    losses2 = []
    losses3 = []
    losses4 = []
    loss_iterations = []
    
    for r in re.findall(loss_pattern, log):
        loss_iterations.append(int(r[0]))
        losses.append(float(r[1]))
        losses2.append(float(r[5]))
        losses3.append(float(r[9]))
        losses4.append(float(r[13]))

    loss_iterations = np.array(loss_iterations)
    losses = np.array(losses)
    losses2 = np.array(losses2)
    losses3 = np.array(losses3)
    losses4 = np.array(losses4)

    return loss_iterations, losses, losses2, losses3, losses4


def disp_results(fig, ax1, loss_iterations, losses, losses2, losses3, losses4, color_ind=0):
    modula = len(plt.rcParams['axes.color_cycle'])
    color1=plt.rcParams['axes.color_cycle'][(color_ind * 4 + 0) % modula]
    ax1.plot(loss_iterations, losses,color=color1)
    color2=plt.rcParams['axes.color_cycle'][(color_ind * 4 + 1) % modula]
    ax1.plot(loss_iterations, losses2,color=color2)
    color3=plt.rcParams['axes.color_cycle'][(color_ind * 4 + 2) % modula]
    ax1.plot(loss_iterations, losses3,color=color3)
    color4=plt.rcParams['axes.color_cycle'][(color_ind * 4 + 3) % modula]
    ax1.plot(loss_iterations, losses4,color=color4)
    colors.append(color1)
    colors.append(color2)
    colors.append(color3)
    colors.append(color4)


if __name__ == '__main__':
    global colors
    colors=[]
    parser = ArgumentParser(description="Draw loss curve")
    parser.add_argument('files1')
    args = parser.parse_args()
    main(args)
