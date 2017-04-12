"""Utilities for validating data.
"""

import datetime
import cerberus
from dateutil import parser as dtparser
import decorator
import toolz as tz

import exceptions


class AutaValidator(cerberus.Validator):
    """Custom Cerberus Validator.
    """

    def _validate_type_asdatetime(self, value):
        """Validate values that are or could parsed as datetimes.
        """
        if isinstance(value, (datetime.datetime, datetime.date)):
            return True
        else:
            try:
                dtparser.parse(value)
                return True
            except Exception:
                return False


def validation_errors(record, schema):
    """Return a dict of errors upon validating the record against the schema.
    """
    v = AutaValidator(schema, allow_unknown=True)
    v.validate(record)
    return v.errors


def validate_inputs(*schemas):

    @decorator.decorator
    def _validate(fn, *recs):
        """Validate multiple function input records against their corresponding
        schemas.  Return the dictionary of all errors.
        """
        if len(recs) != len(schemas):
            raise ValueError("number of schemas does match number of records")
        else:
            errors = tz.merge(*[
                validation_errors(r, s)
                for r, s in zip(recs, schemas) if s is not None])
            if len(errors) > 0:
                raise exceptions.ValidationError(
                    "validation failed with errors:\n{}".format(errors))
            else:
                return fn(*recs)

    return _validate


def validate_output(schema):

    @decorator.decorator
    def _validate(fn, *args):
        """Validate the function output records against its schema and return a
        dict of errors.
        """
        rec = fn(*args)
        errors = validation_errors(rec, schema)
        if len(errors) > 0:
            raise exceptions.ValidationError(
                "validation failed with errors:\n{}".format(errors))
        else:
            return rec

    return _validate


def validate_transitions(config, transitions):
    """Validate the data in the list of transitions against the config.
    """

    def _statuses(trans):
        """Return unique status values among transitions.
        """
        return set(tz.concat(tz.pluck(['initial', 'final'], trans)))

    diff = _statuses(transitions) - set(config['status_values'])
    if len(diff) > 0:
        raise exceptions.ValidationError(
            "invalid status values in transitions: {}".format(diff))
    else:
        return transitions
