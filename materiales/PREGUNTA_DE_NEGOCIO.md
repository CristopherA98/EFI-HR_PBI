# Pregunta de negocio del caso Farmacias Cóndor

## La pregunta

**¿En qué cargos y sucursales de operación de farmacia estamos perdiendo más gente, y cuánto nos cuesta reemplazarla?**

Versión para el aula: *"Cóndor rotó entre 20 % y 31 % de su plantilla cada año. ¿Dónde se concentra esa fuga y qué tan caro y lento es reponerla?"*

## Por qué esta pregunta

- Es de negocio, no de datos: la Gerencia de Operaciones la haría con estas palabras.
- Obliga a usar todo el modelo: plantilla, movimientos, contrataciones, ausencias y las dimensiones cargo, sucursal, área y calendario.
- Se responde con medidas DAX que el curso ya construye (Rotación, Ingresos, Salidas, Costo por contratación, Días de cobertura, Índice de ausentismo).
- Tiene una respuesta con matices (Costa vs. Sierra, picos estacionales), lo que permite storytelling.

## Cadena de seis eslabones

| Eslabón | Contenido |
|---|---|
| Objetivo del negocio | Mantener las farmacias atendidas con personal estable y capacitado |
| OKR | Reducir la rotación de la primera línea de farmacia |
| Resultado clave | Bajar la rotación anualizada de Auxiliares y Cajeros de 35–44 % a menos de 25 % en 12 meses |
| KPI | Rotación; Costo por contratación; Días de cobertura; Índice de ausentismo |
| Fuente del dato | `fact_movimientos`, `fact_contrataciones`, `fact_plantilla`, `fact_ausencias` |
| Umbral y responsable | Rotación mensual > 3 % = alerta; responsable: Gerencia de Operaciones con Talento Humano |

## Subpreguntas (una por bloque del taller)

1. **Dónde:** ¿qué cargos, sucursales y regiones concentran las salidas?
2. **Cuándo y por qué:** ¿hay picos (marzo 2026) y qué motivo domina (renuncia, fin de contrato, desvinculación)? ¿Se van pronto (antes de 90 días)?
3. **Cuánto cuesta y cuánto tarda reponer:** costo por contratación, días de cobertura y canal (agencia vs. portal, universidad, referido).
4. **Qué hacer:** ¿dónde intervenir primero?

## Pistas del dato (ene 2023 – ago 2026, para el expositor)

- 417 salidas: 280 renuncias, 91 fines de contrato, 46 desvinculaciones. Solo 39 ocurren antes de 90 días.
- Rotación anualizada por cargo: Cajero 44,3 %, Auxiliar de farmacia 34,9 % (154 salidas), Asesor de servicio 29,1 %.
- Costa 35,7 % frente a Sierra 23,1 %. Sucursales críticas: Machala Centro 59,0 %, Guayaquil Centro 46,3 %, Manta Norte 45,0 %, Esmeraldas Centro 40,8 %.
- Tendencia a la baja: 30,7 % (2023), 25,4 %, 23,9 %, 20,0 % (2026, ene–ago). Pico en marzo 2026: 20 salidas (9 auxiliares, 13 renuncias).
- El 86 % de las salidas es de Operaciones de farmacia.
- Reponer un Auxiliar cuesta cerca de USD 221 y tarda 22 días; el Químico farmacéutico tarda 37,5 días.
- La agencia cuesta ≈ USD 770 por contratación frente a USD 166–168 de los otros canales (40 de 550 contrataciones).
- El ausentismo sube cada junio–julio; Costa 3,71 % frente a Amazonía 2,88 %.

## Lo que no se debe afirmar

- Que la rotación "baja" sin aclarar que 2026 son solo ocho meses.
- Que la agencia es un problema general: son 40 contrataciones.
- Que hay causa: los datos muestran dónde y cuánto, no por qué.

## Preguntas alternativas

- **Ausentismo:** ¿por qué sube cada junio–julio y qué sucursales costeras lo explican?
- **Atracción:** ¿conviene reducir el uso de agencia y cuánto ahorraría?
