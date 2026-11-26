<p align="center"><img src="assets/mark.svg" width="104" alt="Engineering Reliability"></p>
<h1 align="center">Engineering Reliability</h1>
<p align="center"><em>Cambios pequeños. Evidencia sólida. Versiones más seguras.</em></p>
<p align="center"><a href="README.md">English</a> · <a href="INSTALL.md#español">Instalación</a> · <a href="benchmarks/README.md">Benchmarks</a></p>

Los agentes de IA escriben código rápidamente. La fiabilidad exige entender qué cambia, qué puede fallar y qué se ha comprobado realmente.

Engineering Reliability reúne [Agent Skills](https://agentskills.io/) para desarrollar software según su riesgo, sin imponer un stack.

## Instalar

```sh
pnpm dlx skills add bcuyul/Engineering-Reliability
```

Añade `-g` para todos los proyectos. Selecciona los agentes deseados. Consulta [instalación](INSTALL.md#español).

## Método

**Comprender → Reutilizar → Simplificar → Verificar → Liberar**

| Riesgo | Enfoque |
| --- | --- |
| R0 · Investigación | Evidencia, sin cambios |
| R1 · Corrección menor | Diff acotado y verificación |
| R2 · Funcionalidad | Contratos, alternativas, regresión y revisión |
| R3 · Crítico | Autorización, aislamiento, recuperación y revisión independiente |

Nunca sacrificar seguridad, integridad de datos, accesibilidad ni recuperación. Los cambios con estado deben verificar [transiciones e invariantes](skills/engineering-reliability/references/state-transitions.md), no solo operaciones aisladas.

## Skills

| Skill | Propósito |
| --- | --- |
| [engineering-reliability](skills/engineering-reliability/SKILL.md) | Método principal |
| [engineering-review](skills/engineering-review/SKILL.md) | Revisar cambios y consumidores afectados |
| [engineering-audit](skills/engineering-audit/SKILL.md) | Priorizar riesgos del repositorio |
| [engineering-dependencies](skills/engineering-dependencies/SKILL.md) | Evaluar librerías, licencias y versiones |
| [engineering-release](skills/engineering-release/SKILL.md) | Comprobar preparación de una versión |

Para reforzar la activación, integra [AGENTS.md](AGENTS.md#español) en las instrucciones existentes. Las instrucciones orientan; CI impone controles.

## Antes / después

**Tarea:** importar CSV. En vez de instalar una librería inmediatamente, inspeccionar el parser existente, la biblioteca estándar, las filas inválidas y los límites de recursos. Reutilizar y probar. Ejemplo ilustrativo, no resultado medido.

## Evidencia

El [protocolo de benchmark](benchmarks/README.md) mide correctitud, regresiones, dependencias, coste y tiempo. No hay resultados medidos publicados todavía.

Las skills no requieren scripts ejecutables, telemetría ni conexiones propias. El comportamiento del instalador y del agente es independiente.

Inspirado en [Ponytail](https://github.com/DietrichGebert/ponytail) y [Superpowers](https://github.com/obra/superpowers).
