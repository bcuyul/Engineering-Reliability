---
name: engineering-release
description: Evaluate stable release readiness, CI, packaging, regressions and rollback. Evalúa preparación de versiones sin publicar.
metadata:
  version: "2.2.0-rc.1"
---
# engineering-release

Identify candidate SHA, target platforms, baseline and scope. Check acceptance, data integrity, security, review, tests, performance where relevant, dependencies, artifacts and recovery. Record PASS, FAIL, NOT RUN or N/A with evidence. Verify CI for this candidate. Missing required gates block readiness. Critical changes need independent review and authorization. Never publish or deploy without permission.

For changed stateful behavior, require evidence for relevant lifecycle transitions, invariants and failure postconditions before a stable verdict.

## Español

Identifica SHA candidato, plataformas, línea base y alcance. Comprueba aceptación, integridad, seguridad, revisión, pruebas, rendimiento pertinente, dependencias, artefactos y recuperación. Registra PASS, FAIL, NOT RUN o N/A con evidencia. Verifica CI del candidato. Los controles obligatorios pendientes bloquean la liberación. Cambios críticos requieren revisión independiente y autorización. No publiques ni despliegues sin permiso.

Para cambios con estado, exige evidencia de transiciones relevantes, invariantes y condiciones posteriores a fallos antes de declarar estabilidad.

Apply the core skill if installed / Aplica la skill principal si está instalada.
