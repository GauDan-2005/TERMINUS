#!/bin/bash
case_name="${1:-alpha}"
work="${2:-/tmp/staged-snapshot-$case_name}"
mkdir -p "$work/source" "$work/restored"
printf '%s\n' "$work"
