#! /bin/bash

mkdir -p htmldoc/qrgen
uv run pytest
uv run pdoc --html --force --config latex_math=True -o htmldoc qrgen
uv run coverage html -d htmldoc/coverage --rcfile tests/coverage.conf
uv run coverage xml -o htmldoc/coverage/coverage.xml --rcfile tests/coverage.conf
uv run docstr-coverage src/qrgen -miP -sp -is -idel --skip-file-doc --badge=htmldoc/qrgen/doc_badge.svg
uv run genbadge coverage -l -i htmldoc/coverage/coverage.xml -o htmldoc/qrgen/cov_badge.svg
