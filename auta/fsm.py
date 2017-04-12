"""Declaratively specify the FSM(s).
"""

bias = [
    (
        'watching', 'watching',
        dict(op='le', value=1),
        dict(start='initialize', end='initialize')),
    (
        'watching', 'warning',
        dict(op='eq', value=2),
        dict(start='advance', end='advance')),
    (
        'watching', 'alerting',
        dict(op='eq', value=3),
        dict(start='advance', end='advance')),
    (
        'warning', 'watching',
        dict(op='le', value=1),
        dict(start='initialize', end='initialize')),
    (
        'warning', 'alerting',
        dict(op='ge', value=2),
        dict(start='copy', end='advance')),
    (
        'alerting', 'alerting',
        dict(op='ge', value=2),
        dict(start='copy', end='advance')),
    (
        'alerting', 'warning',
        dict(op='eq', value=1),
        dict(start='copy', end='copy')),
    (
        'alerting', 'watching',
        dict(op='le', value=-1),
        dict(start='initialize', end='initialize'))]
