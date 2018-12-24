#!/usr/bin/python
from lxml import etree


class Parser():

    def __init__(self, nbScen=1, nbAgents=None, cst='a'):

        # Problem Name
        nbScen = 'scen{0:02}'.format(nbScen)

        # ------------ #
        # Reading Text
        # ------------ #
        # Domains
        dom_file = open('bin/' + nbScen + '/DOM.TXT', 'r')
        dom = []
        for i in dom_file:
            dom.append(list(filter(lambda a: a != '', i[5:-1].split(' '))))
        dom_file.close()
        # Variables
        var_file = open('bin/'+nbScen+'/VAR.TXT', 'r')
        var = []
        for i in var_file:
            var.append(list(filter(lambda a: a != '', i[:-1].split(' '))))
        var_file.close()
        # Constraints
        const_file = open('bin/'+nbScen+'/CTR.TXT', 'r')
        const = []
        operation_gt, operation_eq = False, False
        for i in const_file:
            line = list(filter(lambda a: a != '', i[:-1].split(' ')))
            del line[2]
            if line[2] == '>':
                operation_gt = True
            if line[2] == '=':
                operation_eq = True
            if len(line) == 4:
                const.append(line+['0'])
            elif len(line) == 5:
                const.append(line)
            else:
                raise Exception('CONSTRAINT FILE ERROR')

        const_file.close()
        # Cost
        cost_file = open('bin/'+nbScen+'/cst.txt', 'r')
        cost = []
        for i in cost_file:
            if not '=' in i:
                continue
            line = list(filter(lambda a: a != '', i[:-1].split(' ')))
            if line[0][0] == cst:
                cost.append(line[2])
        cost_file.close()
        if len(cost) > 0:
            cost = cost[::-1]
            cost = [str(int(cost[-1])*1000)] + cost
        else:
            cost = ['0', '0', '0', '0', '0']

        # ------------ #
        # Writing XMLs
        # ------------ #
        # Template
        root = etree.Element("instance")
        etree.SubElement(root, "presentation", name=nbScen,
                                        maxConstraintArity="2", maximize="false"
                                        , format="XCSP 2.1_FRODO")
        # Agents
        if not nbAgents:
            nbAgents = len(var)
            basic_strategy = True # Basic Strategy
        else:
            if nbAgents == 0:
                raise Exception('PLEASE ASSIGN NUMBER OF AGENTS')
            if nbAgents > len(var):
                raise Exception('NUMBER OF AGENTS GREATER THAN NUMBER OF VARIABLES')
            basic_strategy = False # Improve Strategy
        agents = etree.SubElement(root, "agents", nbAgents=str(nbAgents))
        nbDigitsOfnbAgents = len(str(nbAgents))
        str_to_format = 'agent{0:0'+str(nbDigitsOfnbAgents)+'}'
        for i in range(1, nbAgents+1):
            etree.SubElement(agents, "agent", name=str_to_format.format(i))

        # Domains
        domains = etree.SubElement(root, "domains", nbDomains=str(len(dom)))
        for i in range(len(dom)):
            domain = etree.SubElement(domains, "domain", name='dom'+str(i), nbValues=str(len(dom[i])))
            domain.text = ' '.join(dom[i])
        # Variables
        variables = etree.SubElement(root, "variables", nbVariables=str(len(var)))
        if basic_strategy:
            for i in range(len(var)):
                etree.SubElement(variables, "variable", name='var'+var[i][0],
                                            domain='dom'+var[i][1], agent=str_to_format.format(i+1))
        # Predicates
        predicates = etree.SubElement(root, "predicates", nbPredicates=str(operation_eq+operation_gt))
        if operation_gt:
            predicate = etree.SubElement(predicates, "predicate", name="gt")
            parameters = etree.SubElement(predicate, "parameters")
            parameters.text = ' int X1 int X2 int K int C'
            expression = etree.SubElement(predicate, "expression")
            functional = etree.SubElement(expression, "functional")
            functional.text = 'mul(sub(abs(sub(X1, X2)), K), C)'
        if operation_eq:
            predicate = etree.SubElement(predicates, "predicate", name="eq")
            parameters = etree.SubElement(predicate, "parameters")
            parameters.text = ' int X1 int X2 int K int C'
            expression = etree.SubElement(predicate, "expression")
            functional = etree.SubElement(expression, "functional")
            functional.text = 'mul(add(abs(sub(abs(sub(X1, X2)), K)), 1), C)'
        # Relations
        # Constraints
        constraints = etree.SubElement(root, "constraints", nbConstraints=str(len(const)))
        for i in const:
            sign = ''
            if i[-3] == '>':
                sign = 'gt'
            if i[-3] == '=':
                sign = 'eq'
            name = 'var'+i[0]+'_'+'var'+i[1]+'_'+sign+'_'+i[-2]
            constraint = etree.SubElement(constraints, "constraint", name=name,
                                          arity="2", scope='var'+i[0]+" var"+i[1], reference=sign)
            parameters = etree.SubElement(constraint, "parameters")
            parameters.text = ' var'+i[0]+' var'+i[1]+' '+i[-2]+' '+cost[int(i[-1])]

        # Print Output
        # print(etree.tostring(root, pretty_print=True).decode("utf-8"))

        # Write XMLs
        file = open('xml/'+nbScen+'.xml', 'w')
        file.write(etree.tostring(root, pretty_print=True).decode("utf-8"))
        file.close()


def main():
    for i in range(1, 12):
        parser = Parser(nbScen=i)


if __name__ == "__main__":
    main()
