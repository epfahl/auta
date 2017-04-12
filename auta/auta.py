"""Main driver library, including the advance function.
"""

import cytoolz as cz
import copy

import transition
import exceptions
import configuration as cf
import utils
import validation as vl


def init(config, transitions, name=None):
    """Given a list of transitions, return a function that updates the state
    when given new input data and the current state.
    """
    cfg = cf.update(config)
    data_schema = cf.data_schema(cfg)
    state_schema = cf.state_schema(cfg)
    transitions = vl.validate_transitions(config, transitions)

    def _with_initial(initial):
        """Return an iterator over active transition objects with the given
        initial status.
        """
        return cz.map(
            lambda t: transition.activate(t, cfg),
            filter(lambda t: t['initial'] == initial, transitions))

    @vl.validate_inputs(data_schema, state_schema)
    def _advance(data, state):
        """Advance to the next state given input data and current state.
        """
        for tr in _with_initial(state['status']):
            if tr.triggered(data, state):
                return tr.update(data, state)
        else:
            raise exceptions.FSMError(
                "no conditions were satisfied when advancing from "
                "status '{}'".format(state['status']))

    return utils.attrize(
        container_name='fsm',
        name=name,
        config=cfg,
        data_schema=data_schema,
        state_schema=state_schema,
        transitions=transitions,
        advance=_advance)


def run(fsm, series, state_init):
    """Given an initialized state machine, an iterable of data paylaods, and
    an initial state, return a iterator of states that results from
    sequentially processing the data series.
    """
    state = copy.copy(state_init)
    for data in series:
        state_new = fsm.advance(data, state)
        yield state_new
        state = state_new
