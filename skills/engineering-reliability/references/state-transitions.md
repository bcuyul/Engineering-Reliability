# State transitions / Transiciones de estado

Use when changing persistent data, permissions, lifecycle status, queues, caches, synchronization or recovery. Keep a small state table in tests or notes, not a new architecture unless needed.

1. Identify distinct states, valid/rejected transitions and invariants. Do not equate missing, null, zero, empty, false, expired or deleted unless the contract explicitly does. Test the full lifecycle.
2. Check return value AND resulting state (including related records, audit history or side effects). A rejected operation must preserve state unless the contract specifies otherwise.
3. Test retry after rejection or interruption, duplicate requests, restart/persistence and concurrent transitions when supported. Use fixed seeds and a simple independent oracle for longer sequences if useful.
4. Test the minimum representative transitions, especially boundary states. Confirm the test catches the original bug when feasible. Report untested paths separately; green tests do not imply complete coverage.

| Domain | Representative transition |
| --- | --- |
| Inventory / ledger | Absent → positive → zero → positive; balance conservation on transfer |
| Authorization | Authorized → revoked/denied → reauthorized when supported; cross-tenant rejection preserves state |
| Orders / tickets | Open → closed → reopen; rejected update leaves current state unchanged |
| Files / sync | Missing → empty file → identical copy; partial retry; stale plan rejection |
| Queues / payments | Pending → failed → retry → committed; duplicate must not reapply effects |

## Español

Usa esta referencia al cambiar datos persistentes, permisos, estados, colas, cachés, sincronización o recuperación. Mantén una pequeña tabla de estados en pruebas o notas, sin crear una arquitectura nueva salvo necesidad.

1. Identifica estados distintos, transiciones permitidas/rechazadas e invariantes. No equipares ausencia, nulo, cero, vacío, falso, expirado o eliminado salvo que el contrato lo indique. Prueba el ciclo completo.
2. Verifica respuesta Y estado resultante (registros relacionados, historial o efectos). Una operación rechazada debe conservar el estado salvo indicación expresa del contrato.
3. Prueba reintento tras rechazo/interrupción, duplicados, reinicio/persistencia y concurrencia cuando procedan. Usa semillas fijas y un oráculo independiente sencillo si aportan valor.
4. Selecciona transiciones representativas mínimas, especialmente límites. Comprueba que la prueba detecte el defecto original cuando sea viable. Declara rutas no verificadas; pruebas verdes no implican cobertura completa.

| Dominio | Transición representativa |
| --- | --- |
| Inventario / libro | Ausente → positivo → cero → positivo; conservación de saldo al transferir |
| Autorización | Autorizado → revocado/denegado → reautorizado si se admite; rechazo entre tenants conserva estado |
| Pedidos / tickets | Abierto → cerrado → reabierto; cambio rechazado conserva estado |
| Archivos / sync | Ausente → archivo vacío → copia idéntica; reintento parcial; rechazo de plan obsoleto |
| Colas / pagos | Pendiente → fallo → reintento → confirmado; duplicado no reaplica efectos |
