"""Library for creating transition objects.
"""

import toolz as tz

import utils
import exceptions


def update_fn(trans, config):
    """Consume an update declaration of the form

    {
        'episode_start': <name of update rule>,
        'episode_end': <name of update rule>
    }

    and return a function that updates the episode start and end times.
    An update rule is one of

    'advance': set to the data time
    'copy': set to the value in the current state
    'initialize': set to the initial value (e.g., None)
    """
    update_dec = trans['update']
    time_key = config['time_key']
    state_initial = config['state_initial']

    def _update(data, state):

        def _rulemap(rule, key):
            if rule == 'advance':
                if key in ('episode_start', 'episode_end'):
                    return data[time_key]
                elif key == 'episode_status_max':
                    return trans['final']
            elif rule == 'copy':
                return state[key]
            elif rule == 'initialize':
                return state_initial[key]
            else:
                raise exceptions.FSMError(
                    "rule ('{}') not recognized".format(rule))

        return {k: _rulemap(r, k) for k, r in update_dec.iteritems()}

    return _update


def activate(trans, config):
    """Return an active transition object given a transition declaration and
    configuration data.
    """
    time_key = config['time_key']
    params = config['params']

    def _triggered(data, state):
        return trans['trigger'](data, state, **params)

    def _update(data, state):
        upd = tz.merge(
            {
                time_key: data[time_key],
                'status': trans['final']},
            update_fn(trans, config)(data, state))
        return tz.merge(state, upd)

    return utils.attrize(
        name='transition',
        initial=trans['initial'],
        final=trans['final'],
        triggered=_triggered,
        update=_update)
