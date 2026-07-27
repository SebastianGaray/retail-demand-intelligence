# Datos sintéticos de demostración

El generador crea archivos Parquet relacionados para tiendas, productos, precios, promociones,
ventas, inventario y calendario. Todos los nombres y valores son sintéticos.

```bash
make sample-data
```

La demanda combina diferencias por producto y tienda, estacionalidad semanal, tendencia, precio,
promociones y ruido reproducible. Las ventas no pueden superar el inventario disponible. Algunas
reposiciones se omiten para producir quiebres de stock ocasionales.

Los archivos se validan antes de publicarse y permanecen fuera de Git. `manifest.json` registra
la versión del generador, la semilla, los parámetros, la fecha de ejecución y los checksums.

Consulta [Synthetic demo data](../en/demo-data.md) para los supuestos y simplificaciones
completos.
