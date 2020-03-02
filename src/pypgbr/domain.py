"""
    Planning Domain Theory

    Miquel Ramirez
    miquel.ramirez@unimelb.edu.au
    (c) 2020
"""
from collections import OrderedDict

from tarski.errors import UndefinedElement
from tarski.io.fstrips import ParsingError, FstripsReader
from tarski.grounding import LPGroundingStrategy
from tarski.syntax.transform.action_grounding import ground_schema

class ObservationNotMatched(Exception):
    pass

class DomainTheory(object):

    def __init__(self):
        self.problem = None
        self.grounding = None
        self.action_index = OrderedDict()

    def load(self, domain_file, instance_file):
        reader = FstripsReader(raise_on_error=True)
        reader.parse_domain(domain_file)
        reader.parse_instance(instance_file)
        self.problem = reader.problem
        self.ground_problem()
        self.setup_index()

    def ground_problem(self):
        if self.problem is None:
            raise RuntimeError('DomainTheory.ground_problem(): no problem has been set!')
        self.grounding = LPGroundingStrategy(self.problem)

    def setup_index(self):
        self.index = OrderedDict()
        actions = self.grounding.ground_actions()
        for name, bindings in actions.items():
            schema = self.problem.get_action(name)
            self.index[name] = OrderedDict()
            for b in bindings:
                op = ground_schema(schema, b)
                #print(name, b)
                self.index[name][b] = op

    def match_observations(self, events):
        """
        Matches input observation sequence to indexed ground actions
        :param events: sequence of observations (pairs of action schema name and list of objects)
        :return: list of tuples (schema, object tuple, ground action)
        """
        O = []
        for name, b in events:
            schema = self.problem.get_action(name)
            try:
                b_constants = tuple([self.problem.language.get(bi) for bi in b])
            except UndefinedElement as e:
                raise ObservationNotMatched("Constant not defined in binding. {}.  schema: {} objects: {}".format(str(e), name, b))
            schema_entry = self.index[name]
            try:
                op = schema_entry[tuple(b)]
                O += [(schema, b_constants, op)]
            except KeyError as e:
                raise ObservationNotMatched("schema: {} objects: {}".format(name, b))
        return O