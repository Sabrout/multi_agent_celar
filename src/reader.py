#!/usr/bin/python
import glob
import re
import numpy as np
import matplotlib.pyplot as plt

from src.report import Report


class Reader():

    def __init__(self, nbScen=2):
        # Problem Name
        self.nbScen = 'scen{0:02}'.format(nbScen)
        # Reports
        self.reports = []
        for path in glob.glob('output/'+self.nbScen+'/*.out'):
            file = open(path, 'r')
            vars = []
            cost = 0
            time = ''
            no_messages = ''
            info_size = ''
            agents = []
            lines = file.readlines()
            for i in range(len(lines)):
                lines[i] = lines[i].replace(',', '')
                if lines[i].startswith("var"):
                    vars.append(list(map(int, re.findall('\d+', lines[i]))))
                if lines[i].startswith("Total optimal cost"):
                    cost = int(re.findall('\d+', lines[i])[0])
                if lines[i].startswith("Algorithm finished in"):
                    time = re.findall('\d+', lines[i])
                    time = int(''.join(time))
                if lines[i].startswith("Number of messages sent (by type)"):
                    no_messages = re.findall('\d+', lines[i+3])
                    no_messages = int(''.join(no_messages))
                if lines[i].startswith("Number of messages sent (by agent)"):
                    j = 1
                    while "agent" in lines[i+j]:
                        agents.append([int(re.findall('\d+', lines[i+j].replace(',', ''))[1])])
                        j += 1
                        if "Number" in lines[i+j]: break
                if lines[i].startswith("Number of messages received (by agent)"):
                    j = 1
                    while "agent" in lines[i+j]:
                        agents[j-1].append(int(re.findall('\d+', lines[i+j].replace(',', ''))[1]))
                        j += 1
                        if "Number" in lines[i+j]: break
                if lines[i].startswith("Amount of information sent (by type"):
                    info_size = re.findall('\d+', lines[i+3])
                    info_size = int(''.join(info_size))
                if lines[i].startswith("Amount of information sent (by agent"):
                    j = 1
                    while "agent" in lines[i+j]:
                        agents[j-1].append(int(re.findall('\d+', lines[i+j].replace(',', ''))[1]))
                        j += 1
                        if "Amount" in lines[i+j]: break
                if lines[i].startswith("Amount of information received (by agent"):
                    j = 1
                    while "agent" in lines[i+j]:
                        agents[j-1].append(int(re.findall('\d+', lines[i+j].replace(',', ''))[1]))
                        j += 1
                        if "Size" in lines[i+j]: break
            vars.sort(key=lambda x: x[0])
            self.reports.append(Report(algo=path.split('_')[-2], cost_type=path.split('_')[-1].replace('.out',''),
                                       var_assignment=vars, optimal_cost=cost, simulation_time=time,
                                       no_messages=no_messages, info_size=info_size, agents=agents))

    def plot(self, y, labels, xlabel, ylabel, plot_name):
        for i in range(0, len(y)):
            plt.plot(y[i], label=labels[i])
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend(loc='upper right')
        plt.savefig("tex/figure/" + plot_name + ".png")
        plt.show()
        plt.close()


def main():
    problems = np.array([2, 5, 6, 9, 11])
    messages = []
    for i in problems:
        print("=================")
        print("Instance No.{}".format(i))
        print("=================")
        reader = Reader(nbScen=i)
        if len(reader.reports) == 1:
            j = reader.reports[0]
        if len(reader.reports) == 2:
            j = reader.reports[1]
        j.print_all()
        messages.append(j.get_sent_messages())
    # reader.plot(messages, ["Instance No.2", "Instance No.5", "Instance No.6", "Instance No.9",
    #      "Instance No.11"], "Agents", "Number of Messages", "messages")


if __name__ == "__main__":
    main()