#!/usr/bin/python
import glob
import re

from src.report import Report


class Reader():

    def __init__(self, nbScen=1):
        # Problem Name
        nbScen = 'scen{0:02}'.format(nbScen)
        # Reports
        self.reports = []
        for path in glob.glob('output/'+nbScen+'/*.out'):
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

def main():
    reader = Reader(nbScen=6)


if __name__ == "__main__":
    main()