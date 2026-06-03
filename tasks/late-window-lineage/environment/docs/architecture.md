# Architecture notes

The binary loads case rows, normalizes them into internal rows, combines stored rows with fresh rows, and writes a structured audit. The direct and restart-shaped paths share most code but enter it with different state surfaces. Display helpers live outside the processing path and exist for operator inspection.

The input files are plain comma-separated rows. They are operational data, not answers. The audit output is produced from those rows at runtime.
