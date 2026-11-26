# Benchmarks / Evaluaciones

No measured model results yet. / Sin resultados medidos de modelos todavía.

## Pilot

Five synthetic Python repair tasks, two arms (baseline vs explicit Engineering Reliability context), two repetitions by default. Same model, code, task, permissions, budget and seeded execution order. Inputs and expected outputs stay outside the agent prompt; they are public in this repository, not secret held-out tests. Independent behavioral checks, not LLM grading.

Prerequisites: Python 3.10+, Git. Live runs also require a current Claude Code CLI, a trusted local Linux Python image and Docker in a disposable unmanaged VM. No corporate credentials or data. Use a native Claude executable. The pilot disables tools and customization; it measures guidance under explicit injection, not plugin discovery or full agentic workflows. Managed policy can still affect Claude, so do not use a managed corporate environment. The Docker boundary reduces risk but is not a guarantee; use a disposable VM. No Docker socket or secrets are mounted.

```sh
python benchmarks/pilot/run.py smoke
python benchmarks/pilot/run.py plan
```

Smoke runs only the known broken and reference fixtures locally. It does not call any model. For a live run, obtain and inspect a trusted Python image first, then use an exact model identifier accessible to your account:

```sh
docker pull python:3.12-slim
python benchmarks/pilot/run.py live --model YOUR_EXACT_MODEL_ID --image python:3.12-slim --repetitions 1 --budget 0.25 --confirm-isolated
```

Use two repetitions for the 20-run pilot. The budget is an estimated per-run CLI limit, not a guaranteed billing cap; check your account usage. The runner pins the locally resolved image ID and requires a clean committed checkout. Logs, candidate text and per-run results stay in ignored `benchmarks/local-results/`. The live runner checks reference solutions inside Docker before the first model call. Malformed candidate output counts as failure; infrastructure errors stop the run. Partial results are not a completed comparison. Review raw output before publishing. No telemetry or automated public uploads.

Next: real multi-file agent tasks with native skill activation and isolated environments, Codex adapter, pinned Ponytail/Superpowers configurations, held-out tests and at least five repetitions. Compare correct completion, regressions, security, token usage, time, cost and dependency changes. Report failures and uncertainty.

## Español

Cinco tareas sintéticas Python, dos grupos (base vs contexto explícito de Engineering Reliability), dos repeticiones por defecto. Mismo modelo, código, tarea, permisos, presupuesto y orden reproducible. Las pruebas se mantienen fuera del prompt, pero son públicas en este repositorio; no son pruebas secretas. Verificación conductual independiente.

Requisitos: Python 3.10+, Git. Las ejecuciones reales requieren Claude Code actualizado (ejecutable nativo), Docker e imagen Linux Python confiable, dentro de una VM desechable no administrada, sin datos ni credenciales corporativas. Se desactivan herramientas y personalizaciones; se mide la metodología inyectada, no la activación automática ni un flujo agéntico completo. Políticas administradas pueden alterar el control. Docker reduce riesgo, no lo elimina.

Ejecuta los comandos smoke y plan anteriores. Smoke prueba solo código conocido, sin IA. Para el piloto real descarga e inspecciona la imagen y sustituye YOUR_EXACT_MODEL_ID por un identificador exacto disponible. Una repetición son 10 llamadas; dos son 20. El presupuesto por llamada es aproximado, no un tope de facturación garantizado. El runner fija la imagen local, exige un checkout limpio y guarda evidencias locales ignoradas por Git. El runner verifica las referencias dentro de Docker antes de llamar al modelo. Una respuesta de código inválida cuenta como fallo; los errores de infraestructura detienen la ejecución. Resultados parciales no son una comparación completa. Revisa logs antes de publicar.

Siguiente fase: tareas multiarchivo, activación nativa, Codex, versiones fijadas de Ponytail y Superpowers, pruebas reservadas y cinco o más repeticiones. Publica correctitud, regresiones, seguridad, tokens, tiempo, coste, dependencias, fallos e incertidumbre.

[Claude CLI reference](https://code.claude.com/docs/en/cli-reference) · [Agent Skills evals](https://developers.openai.com/blog/eval-skills) · [Docker run](https://docs.docker.com/reference/cli/docker/container/run/)
