#!/usr/bin/python
from lxml import etree


class Parser():

    def __init__(self, nbScen=1, nbAgents=None):

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
        const_hard = []
        const_soft = []
        for i in const_file:
            line = list(filter(lambda a: a != '', i[:-1].split(' ')))
            del line[2]
            if len(line) == 4:
                const_hard.append(line)
            elif len(line) == 5:
                if line[-1] == '0':
                    const_hard.append(line[:-1])
                else:
                    const_soft.append(line)
            else:
                raise Exception('CONSTRAINT FILE ERROR')
        const_file.close()

        # Process Hard Constraints
        const_hard_set = set()
        for i in range(len(const_hard)):
            const_hard_set.add((const_hard[i][-2], const_hard[i][-1]))

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
            domain = etree.SubElement(domains, "domain", name=str(i), nbValues=str(len(dom[i])))
            domain.text = ' '.join(dom[i])
        # Variables
        variables = etree.SubElement(root, "variables", nbVariables=str(len(var)))
        if basic_strategy:
            for i in range(len(var)):
                etree.SubElement(variables, "variable", name=var[i][0],
                                            domain=var[i][1], agent=str_to_format.format(i+1))
        # Predicates
        predicates = etree.SubElement(root, "predicates", nbPredicates=str(len(const_hard_set)))
        for i in const_hard_set:
            sign, constant = i
            if sign == '>':
                sign = 'gt'
            if sign == '=':
                sign = 'eq'
            predicate = etree.SubElement(predicates, "predicate", name=sign+constant)
            parameters = etree.SubElement(predicate, "parameters")
            parameters.text = ' int X1 int X2 '
            expression = etree.SubElement(predicate, "expression")
            functional = etree.SubElement(expression, "functional")
            functional.text = sign+'(abs(sub(X1, X2)), '+constant+')'
        # Relations
        # Constraints
        constraints = etree.SubElement(root, "constraints", nbConstraints=str(len(const_hard)+len(const_soft)))
        for i in const_hard:
            sign = ''
            if i[-2] == '>':
                sign = 'gt'
            if i[-2] == '=':
                sign = 'eq'
            name = i[0]+'_'+i[1]+'_'+sign+'_'+i[-1]
            constraint = etree.SubElement(constraints, "constraint", name=name, arity="2", scope=i[0]+" "+i[1],
                                          reference=sign+i[-1])
            parameters = etree.SubElement(constraint, "parameters")
            parameters.text = ' '+i[0]+' '+i[1]+' '




        # Print Output
        print(etree.tostring(root, pretty_print=True).decode("utf-8"))


def main():
    parser = Parser(nbScen=1)


if __name__ == "__main__":
    main()