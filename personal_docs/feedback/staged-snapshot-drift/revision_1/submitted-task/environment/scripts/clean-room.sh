#!/bin/bash
root="${1:-/tmp/staged-snapshot-room}"
rm -rf "$root"
mkdir -p "$root"
printf '%s\n' "$root"
