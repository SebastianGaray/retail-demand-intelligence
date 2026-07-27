# Flujo de pronóstico

El flujo compara un promedio reciente, un pronóstico estacional semanal y LightGBM con períodos
cronológicos. Los resultados son evaluaciones sin conexión sobre datos sintéticos. No representan
rendimiento en producción.

```bash
make sample-data
make train
make evaluate
make predictions
```

El horizonte predeterminado es de 28 días. Los últimos 28 días forman el conjunto de prueba y los
28 días anteriores forman validación. Las variables derivadas de demanda e inventario se desplazan
por el horizonte completo para evitar usar información futura.

Se calculan MAE, WAPE y MASE para el total, cada tienda y cada producto. LightGBM se publica como
ganador solo si mejora el WAPE de validación del mejor baseline en al menos 2%.

Los artefactos guardan el modelo, predicciones, métricas, períodos, configuración, versiones de
esquema y checksums. Los archivos de modelo solo deben cargarse desde ejecuciones confiables.

Consulta [Forecasting workflow](../en/forecasting.md) para la definición completa de variables,
métricas y limitaciones.
