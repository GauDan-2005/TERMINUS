# Policy Revocation Shadow — Reviewer Appendix

Post-build discovery confirmation only. Do not use as Step 2b drafting input.

## Expected fix surface

Five Rust modules under `k0` through `k5` with opaque symbols. Revoke handling, cache keying, batch evaluation, delegation resolution, and audit classification must be coordinated.

## Empirical target

Hard: frontier accuracy at or below 20% on the best or worst reference model with a deterministic oracle.

## Docker checklist

Confirm tmux, asciinema, digest-pinned FROM, narrow COPY, `.dockerignore`, OCI labels, pytest preinstalled, no runtime installs in `tests/test.sh`.
