#!/usr/bin/python
from lxml import etree
from lxml import builder


def main():
    xml = builder.ElementMaker()
    instance = xml.instance
    presentation = xml.presentation
    agents = xml.agents
    agent = xml.agent
    domains = xml.domains
    domain = xml.domain
    variables = xml.variables
    variable = xml.variable
    relations = xml.relations
    relation = xml.relation
    constraints = xml.constraints
    constraint = xml.constraint
    predicates = xml.predicates
    predicate = xml.predicate
    scen = instance(
            presentation(name="sample_problem", maxConstraintArity="2", maximize="false", format="XCSP 2.1_FRODO"),
            agents(
                agent(name="agentX"),
                agent(name="agentY"),
                agent(name="agentZ")
            , nbAgents="3"),
            domains(
                domain("1..3", name="three_colors", nbValues="3")
            , nbDomains="1"),
            variables(
                variable(name="X", domain="three_colors", agent="agentX"),
                variable(name="Y", domain="three_colors", agent="agentY"),
                variable(name="Z", domain="three_colors", agent="agentZ")
            , nbVariables="3"),
            # relations(
            #     relation("\n      infinity: 1 1|2 2|3 3\n    ", name="NEQ", arity="2", nbTuples="3",
            #              semantics="soft", defaultCost="0")
            # , nbRelations="1"),

            constraints(
                constraint(name="X_and_Y_have_different_colors", arity="2", scope="X Y", reference="NEQ"),
                constraint(name="X_and_Z_have_different_colors", arity="2", scope="X Z", reference="NEQ"),
                constraint(name="Y_and_Z_have_different_colors", arity="2", scope="Y Z", reference="NEQ")
            , nbConstraints="3")
    )
    # print(etree.tostring(scen, pretty_print=True).decode("utf-8"))

    root = etree.Element("root")
    child2 = etree.SubElement(root, "child2", name="agentX")
    child2.text = '5'
    root.append(etree.Element("child3"))

    print(etree.tostring(root, pretty_print=True).decode("utf-8"))


if __name__ == "__main__":
    main()