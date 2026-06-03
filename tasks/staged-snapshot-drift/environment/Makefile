.PHONY: build audit clean

build:
	mkdir -p /app/bin
	gcc -std=c11 -O2 -Wall -Wextra -o /app/bin/fsmeasure /app/probe/measure.c /app/probe/fswalk.c
	go build -o /app/bin/snapctl ./cmd/ctl

audit:
	$(MAKE) -s build
	bash /app/scripts/run-matrix.sh

clean:
	rm -rf /app/output /app/bin /tmp/staged-snapshot-* /tmp/ssd-*
