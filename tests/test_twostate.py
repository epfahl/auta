import toolz as tz
import auta


# Define a two-status state machine with status values 'a' and 'b'.
twostate = dict(
    config=dict(
        time_key='time',
        time_type='integer',
        data_values=[0, 1],
        status_values=['a', 'b'],
        state_initial=dict(
            status='a')),
    transitions=[
        dict(
            initial='a', final='a',
            trigger=lambda d, s: d['value'] == 0,
            update=dict(
                episode_start='initialize',
                episode_end='initialize')),
        dict(
            initial='a', final='b',
            trigger=lambda d, s: d['value'] == 1,
            update=dict(
                episode_start='advance',
                episode_end='advance')),
        dict(
            initial='b', final='b',
            trigger=lambda d, s: d['value'] == 1,
            update=dict(
                episode_start='copy',
                episode_end='advance')),
        dict(
            initial='b', final='a',
            trigger=lambda d, s: d['value'] == 0,
            update=dict(
                episode_start='initialize',
                episode_end='initialize'))])


def _series(values, time_key):
    """Return a series of data payloads for the given sequence of values.
    """
    return map(
        lambda (t, v): {time_key: t, 'value': v},
        zip(range(len(values)), values))


def test_status_sequence():
    fsm = auta.init(twostate['config'], twostate['transitions'])
    values = [0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0]
    series = _series(values, fsm.config['time_key'])
    states = auta.run(fsm, series, fsm.config['state_initial'])
    seq = list(tz.pluck('status', states))
    assert seq == [
        'a', 'a', 'a', 'b', 'b', 'b',
        'b', 'a', 'b', 'a', 'b', 'b', 'a']
