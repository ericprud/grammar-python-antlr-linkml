from pyjsg.jsglib import loads as jsg_loads
from ShExJSG import ShExJ

from pyshexc.ShExC import ShExC


def _tc(cardinality: str) -> str:
    return ('{"type": "Schema", "shapes": [{"type": "Shape", "id": "http://a.example/S1", '
            '"expression": {"type": "TripleConstraint", "predicate": "http://a.example/p1"' + cardinality + '}}]}')


def test_explicit_one_cardinality_is_kept():
    """An explicit min=1, max=1 serializes as {1}, so ShExC -> ShExJ keeps it (shexTest 1card1)"""
    shexc = str(ShExC(jsg_loads(_tc(', "min": 1, "max": 1'), ShExJ)))
    assert '.{1}' in shexc.replace(' ', '')
    tc = ShExC(shexc).schema.shapes[0].expression
    assert (tc.min, tc.max) == (1, 1)


def test_default_cardinality_is_omitted():
    shexc = str(ShExC(jsg_loads(_tc(''), ShExJ)))
    assert '{' not in shexc.split('{', 1)[1]
    tc = ShExC(shexc).schema.shapes[0].expression
    assert (tc.min, tc.max) == (None, None)
