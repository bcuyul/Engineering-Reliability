# Installation

[Español](#español)

Universal installer (Node.js and pnpm required):
```sh
pnpm dlx skills add bcuyul/Engineering-Reliability
```
Add `-g` for user scope or `--skill engineering-reliability` for the core only. Review the external [installer](https://github.com/vercel-labs/skills), version and privacy settings. Select target agents interactively.

**Claude Code:** enter separately:
```
/plugin marketplace add bcuyul/Engineering-Reliability
/plugin install engineering-reliability@engineering-reliability
```
**Codex:** `codex plugin marketplace add bcuyul/Engineering-Reliability`; select the plugin in the host. Native manifests are preview, not runtime-tested.

**Other hosts:** use the universal installer for supported agents, or copy the desired skill directory into the host's documented skills location. Merge AGENTS.md into existing persistent instructions (CLAUDE.md, AGENTS.md, GEMINI.md or host-specific rules). Do not overwrite existing rules. Restart, check discovery, invoke the skill and test on a disposable project. Uninstall through the same host or installer.

## Español

Instalador universal (requiere Node.js y pnpm):
```sh
pnpm dlx skills add bcuyul/Engineering-Reliability
```
Añade `-g` para alcance de usuario o `--skill engineering-reliability` para instalar solo el núcleo. Revisa el [instalador externo](https://github.com/vercel-labs/skills), su versión y privacidad. Selecciona los agentes interactivamente.

**Claude Code:** ejecuta por separado los dos comandos anteriores de marketplace e instalación. **Codex:** añade el marketplace con el comando anterior y selecciona el plugin. Manifiestos preliminares, sin pruebas reales en el agente.

**Otros agentes:** usa el instalador universal o copia la carpeta de la skill al destino documentado. Integra AGENTS.md en las instrucciones persistentes existentes sin reemplazarlas. Reinicia, comprueba la detección, invoca la skill y prueba en un proyecto desechable. Desinstala mediante el mismo mecanismo. La activación automática depende del agente.
