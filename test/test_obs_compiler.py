import json

from collections import OrderedDict

import pytest

import tarski
import tarski.evaluators

from tarski.theories import Theory
from tarski.io.fstrips import ParsingError, FstripsReader
from tarski.syntax import *
from tarski.grounding import LPGroundingStrategy
from pypgbr.domain import DomainTheory, ObservationNotMatched

def test_action_index():

    theory = DomainTheory()
    theory.load('test/probBLOCKS-domain.pddl', 'test/probBLOCKS-4-2.pddl')
    assert len(theory.index) == 4

def test_obs_loading_ok():
    theory = DomainTheory()
    theory.load('test/probBLOCKS-domain.pddl', 'test/probBLOCKS-4-2.pddl')

    with open('test/bw_4_2_good_obs.json') as instream:
        in_obs = json.loads(instream.read())
    assert in_obs['type'] == 'actions'

    obs = theory.match_observations(in_obs['observations'])
    assert len(obs) == len(in_obs['observations'])

def test_obs_loading_fails():
    theory = DomainTheory()
    theory.load('test/probBLOCKS-domain.pddl', 'test/probBLOCKS-4-2.pddl')

    with open('test/bw_4_2_bad_obs.json') as instream:
        in_obs = json.loads(instream.read())
    assert in_obs['type'] == 'actions'

    with pytest.raises(ObservationNotMatched):
        obs = theory.match_observations(in_obs['observations'])





