The heap stress harness under `/app` looks fine on tiny sequences but its combined audit drifts once fragmentation, neighbor merge, and growth scripts run together. Repair it so `bash /app/scripts/run-matrix.sh` completes and writes `/app/output/alloc-audit.json` for cedar, jade, slate, coral, onyx, and pearl from the shipped inputs.

The JSON has a top-level cases array. Each case reports name, ok, steps, heap_sig, fl_count, fl_sig, byte_total, and ledger. Steps record each operation with matching signature and tally fields. The ledger path points to JSONL rows in the same order as steps. A case is clean when ok is true and those surfaces stay consistent through the scripted sequence.

`bash /app/scripts/run-one.sh <name>` must write `/app/output/<name>-audit.json` under the same rules. Two matrix runs from unchanged inputs must produce equivalent JSON.
