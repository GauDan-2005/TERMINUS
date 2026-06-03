# Architecture

The command layer prepares a profile, captures source-side observations, materializes a restored tree, and emits a compact audit document. Internal packages are deliberately small: one package tracks active objects, one folds durable rows, one carries accounting attributes, and one binds filesystem observations to emitted files.

Native probes are kept separate so operator builds can compare platform-level observations with the records carried by the service.
