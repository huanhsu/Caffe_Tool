import numpy as np
import re
import matplotlib.patches as mpatches
from argparse import ArgumentParser
from matplotlib import pylab as plt
import pdb

#Draw loss curves with many output in a file
#This example has 4 accuracy curves

#an example on log
#Iteration 10000, Testing net (#0)
#.
#.
#.
#I0728 16:30:05.970779  1057 solver.cpp:398]     Test net output #0: accuracy = 0.824713
#I0728 16:30:05.970815  1057 solver.cpp:398]     Test net output #1: accuracy_2c_4f = 0.782889
#I0728 16:30:05.970824  1057 solver.cpp:398]     Test net output #2: accuracy_2c_5c = 0.876994
#I0728 16:30:05.970832  1057 solver.cpp:398]     Test net output #3: accuracy_3d_5c = 0.876424

#explainition
#Use two patterns but not one due to information losses from Iteration to accuracy when using only a pattern, matching only iteration 0 and the very last accuracy

def main(files):
    plt.style.use('ggplot')
    fig, ax1 = plt.subplots()
    ax1.set_ylim([0,100])
    ax1.set_xlabel('Iteration')
    ax1.set_ylabel('Accuracy (%)')
    temp=[]
    temp.append(files.files1)
    for i, log_file in enumerate(temp):
         accuracy_iterations, accuracies, accuracies2, accuracies3, accuracies4= parse_log(log_file)
         disp_results(fig, ax1, accuracy_iterations, accuracies, accuracies2, accuracies3, accuracies4, color_ind=i)
    patch1 = mpatches.Patch(color=colors[0], label='original')
    patch2 = mpatches.Patch(color=colors[1], label='2c_4f')
    patch3 = mpatches.Patch(color=colors[2], label='2c_5c')
    patch4 = mpatches.Patch(color=colors[3], label='3d_5c')
    plt.legend(handles=[patch1, patch2, patch3, patch4])
    plt.show()


def parse_log(log_file):
    with open(log_file, 'r') as log_file:
        log = log_file.read()
    #two patterns
    iteration_pattern = r"Iteration (\d+), Testing net \(#0\)"
    accuracy_pattern = r"accuracy = (\d+(\.\d*)?)\n.* accuracy_2c_4f = (\d+(\.\d*)?)\n.* accuracy_2c_5c = (\d+(\.\d*)?)\n.* accuracy_3d_5c = (\d+(\.\d*)?)"

    accuracies = []
    accuracies2 = []
    accuracies3 = []
    accuracies4 = []
    accuracy_iterations = []
    
    for r in re.findall(iteration_pattern, log):
        iteration = int(r)
        accuracy_iterations.append(iteration)

    for r in re.findall(accuracy_pattern, log):
        accuracies.append(float(r[0])*100)
        accuracies2.append(float(r[2])*100)
        accuracies3.append(float(r[4])*100)
        accuracies4.append(float(r[6])*100)


    accuracy_iterations = np.array(accuracy_iterations)
    accuracies = np.array(accuracies)
    accuracies2 = np.array(accuracies2)
    accuracies3 = np.array(accuracies3)
    accuracies4 = np.array(accuracies4)

    return accuracy_iterations, accuracies, accuracies2, accuracies3, accuracies4


def disp_results(fig, ax1, accuracy_iterations, accuracies, accuracies2, accuracies3, accuracies4, color_ind=0):
    modula = len(plt.rcParams['axes.color_cycle'])
    #Original accuracy
    color1=plt.rcParams['axes.color_cycle'][(color_ind * 4 + 0) % modula]
    ax1.plot(accuracy_iterations, accuracies,color=color1)
    #
    color2=plt.rcParams['axes.color_cycle'][(color_ind * 4 + 1) % modula]
    ax1.plot(accuracy_iterations, accuracies2,color=color2)
    #
    color3=plt.rcParams['axes.color_cycle'][(color_ind * 4 + 2) % modula]
    ax1.plot(accuracy_iterations, accuracies3,color=color3)
    #
    color4=plt.rcParams['axes.color_cycle'][(color_ind * 4 + 3) % modula]
    ax1.plot(accuracy_iterations, accuracies4,color=color4)
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
