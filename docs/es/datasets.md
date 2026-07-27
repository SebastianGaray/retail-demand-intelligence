# Resumen de datos

El proyecto usa siete conjuntos de datos Parquet: tiendas, productos, ventas diarias, precios
diarios, promociones, inventario diario y calendario.

Cada venta, precio, promoción y registro de inventario referencia una tienda y un producto
existentes. Las fechas deben pertenecer a sus períodos activos y al calendario. Las cantidades no
pueden ser negativas, los precios deben ser mayores que cero y las promociones no pueden
superponerse para la misma tienda y producto.

Los identificadores admiten letras, números, `_` y `-`. Las fechas siguen el formato ISO
`YYYY-MM-DD`.

Ejemplo de venta diaria:

```json
{
  "store_id": "STORE_001",
  "product_id": "SKU_001",
  "date": "2024-01-02",
  "quantity": 10,
  "revenue": 90.00
}
```

Los datos reales o confidenciales no se guardan en el repositorio. Solo se incluyen fixtures
sintéticos pequeños para pruebas. Consulta la [especificación en inglés](../en/datasets.md) para
la definición completa de campos.
