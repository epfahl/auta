"""Configuration utilities.
"""

import toolz as tz

DEFAULT_CONFIG = {
    'time_key': 'time',
    'time_type': 'asdatetime',
    'data_values': [],
    'status_values': [],
    'params': {},
    'state_initial': {
        'status': None,
        'episode_start': None,
        'episode_end': None,
        'episode_status_max': None}}

REQUIRED_CONFIG_KEYS = [
    'time_key',
    'time_type',
    'data_values',
    'status_values',
    'state_initial']


def _merge_with_default(updates, default=DEFAULT_CONFIG):
    """Merge config updates with the default config.

    Note
    ----
    toolz.merge does not recursively merge nested dicts, hence the
    multiple merge steps.
    """
    cfg = tz.merge(default, updates)
    cfg['state_initial'] = tz.merge(
        DEFAULT_CONFIG['state_initial'], cfg['state_initial'])
    cfg['state_initial'][cfg['time_key']] = None
    return cfg


def _validate(config):
    """Validate the configuation.
    """
    diff = set(REQUIRED_CONFIG_KEYS) - set(config.keys())
    if len(diff) > 0:
        raise ValueError(
            "config is missing required keys".format(diff))
    elif config['state_initial']['status'] not in config['status_values']:
        raise ValueError(
            "initial status '{}' is not among the allowed status values"
            .format(config['state_initial']['status']))
    else:
        return config


def update(updates):
    """Merge config updates with a default and validate the results.
    """
    return _validate(_merge_with_default(updates))


def data_schema(cfg):
    """Given config data, return the Cerberus schema for the input data.
    """
    return {
        cfg['time_key']: {
            'type': cfg['time_type'],
            'required': True},
        'value': {
            'allowed': cfg['data_values'],
            'required': True}}


def state_schema(cfg):
    """Given config data, return the Cerberus schema for the state.
    """
    return {
        cfg['time_key']: {
            'type': cfg['time_type'],
            'required': True,
            'nullable': True},
        'status': {
            'allowed': cfg['status_values'],
            'required': True},
        'episode_start': {
            'type': cfg['time_type'],
            'required': True,
            'nullable': True},
        'episode_end': {
            'type': cfg['time_type'],
            'required': True,
            'nullable': True},
        'episode_status_max': {
            'allowed': cfg['status_values'],
            'required': False,
            'nullable': True}}
