import codecs

from pyshexc.parser_impl.generate_shexj import load_shex_file, parse

# A UTF-8 character after ~300KB of ASCII: chardet only samples the start and reports
# ascii with confidence 1.0 (as it does for FHIR R4's fhir.shex), which used to crash decode()
CAFE_SHEXC = '<http://a.example/S1> { <http://a.example/p1> ["café"] }\n'


def test_utf8_after_long_ascii_prefix(tmp_path):
    shex_file = tmp_path / 'long.shex'
    shex_file.write_bytes(('# padding line for chardet\n' * 12000 + CAFE_SHEXC).encode('utf-8'))
    text = load_shex_file(str(shex_file))
    assert text.endswith(CAFE_SHEXC)
    assert parse(text).shapes[0].expression.valueExpr.values[0].value == 'café'


def test_non_utf8_falls_back(tmp_path):
    """ShExC must be UTF-8, but a Latin-1 file still loads rather than crashing.
    Which 8-bit encoding chardet guesses for so short a sample varies, so only the ASCII is checked."""
    shex_file = tmp_path / 'latin1.shex'
    shex_file.write_bytes(CAFE_SHEXC.encode('latin-1'))
    text = load_shex_file(str(shex_file))
    assert len(text) == len(CAFE_SHEXC)
    e_acute = CAFE_SHEXC.index('é')
    assert text[:e_acute] + 'é' + text[e_acute + 1:] == CAFE_SHEXC


def test_utf8_bom(tmp_path):
    shex_file = tmp_path / 'bom.shex'
    shex_file.write_bytes(codecs.BOM_UTF8 + CAFE_SHEXC.encode('utf-8'))
    assert load_shex_file(str(shex_file)) == CAFE_SHEXC
