#!/usr/bin/env bash
REALPATH="$(realpath "$0")"
BASEDIR="$(dirname "$REALPATH")"
BASENAME="$(basename "$REALPATH")"

cd "$BASEDIR"

# https://stackoverflow.com/a/8597411
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    o=xdg-open
elif [[ "$OSTYPE" == "darwin"* ]]; then
    o=open
else
    >&2 echo "Only Linux and MacOS are supported by $BASENAME"
    exit 1
fi

tests/basic/test_VRE_RUNNER.sh  && ($o /Users/struckmanns/git/gitlab/dataquierVRE/tests/basic/run000/report.html ; less tests/basic/run000/tool.log)
