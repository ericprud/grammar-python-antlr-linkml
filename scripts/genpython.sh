#!/usr/bin/env bash
# Regenerate pyshexc/parser from the spec grammar.
#
# ANTLR_VERSION must match the antlr4-python3-runtime pin in pyproject.toml.
# `uvx --from antlr4-tools antlr4 -v $ANTLR_VERSION` fetches the matching
# ANTLR jar automatically (Java required); no manual antlr install needed.
#
# The grammar is taken from a sibling checkout of https://github.com/shexSpec/grammar
set -euo pipefail
ANTLR_VERSION=4.13.2

cd "$(dirname "$0")"
cp ../../grammar/ShExDoc.g4 .
uvx --from antlr4-tools antlr4 -v $ANTLR_VERSION -Dlanguage=Python3 -package parser -o ../pyshexc/parser -no-listener -visitor ShExDoc.g4
rm ShExDoc.g4
