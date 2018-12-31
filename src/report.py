#!/usr/bin/python
import numpy as np
from src.parser import Parser


class Report():

    def __init__(self, algo, cost_type, var_assignment, optimal_cost, simulation_time, no_messages, info_size, agents):
        self.algo = algo
        self.cost_type = cost_type
        self.vars = var_assignment
        self.cost = optimal_cost
        self.time = simulation_time # in ms
        self.messages = no_messages
        self.info = info_size # in Bytes
        self.agents = np.array(agents) # agent = [messages sent, messages received, info sent, info received]

    def get_sorted_vars(self):
        return self.vars.sort(key=lambda x: x[0])[:, -1]

    def get_sent_messages(self):
        return self.agents[:, 0]

    def get_received_messages(self):
        return self.agents[:, 1]

    def get_sent_info(self):
        return self.agents[:, 2]

    def get_received_info(self):
        return self.agents[:, 3]

    def get_max_var(self):
        return max(self.vars)

    def get_no_vars(self):
        return len(self.vars)


def main():
    print()


if __name__ == "__main__":
    main()