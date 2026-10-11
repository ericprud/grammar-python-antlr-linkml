from pyshexc.parser_impl.generate_shexj import parse


def test_iriref_with_query_string():
    """IRIREF allows '=' (only #x00-#x20 and <>"{}|^`\\ are excluded), so query strings lex"""
    schema = parse('<http://a.example/S1> { <http://a.example/p1?q=v&r=w> . }')
    assert schema is not None
    assert schema.shapes[0].expression.predicate == 'http://a.example/p1?q=v&r=w'
