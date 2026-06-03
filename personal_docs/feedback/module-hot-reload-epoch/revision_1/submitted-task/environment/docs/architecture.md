# Architecture notes

The runner reads scenario descriptions, asks small core modules to produce rows, invokes the native component for numeric record handling, and writes a report. The core modules are named by package area rather than by business vocabulary so they can be reused in experiments.
