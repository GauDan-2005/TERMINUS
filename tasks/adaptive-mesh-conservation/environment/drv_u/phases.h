#ifndef PHASES_H
#define PHASES_H

#include "../include/case_spec.h"
#include "../include/vault_layout.h"

void phase_grow(SimState *st, const ScenarioSpec *spec);
void phase_fold(SimState *st, const ScenarioSpec *spec);
int phase_persist(SimState *st, const char *vault_path, const char *tamper_path,
                  const char *log_path, VaultAudit *resume_aud);

#endif
