# Interfaces locales

FastAPI y Streamlit leen la misma ejecución de artefactos. Ninguna interfaz entrena modelos.

```bash
make app
make api
```

El dashboard funciona sin el proceso de FastAPI. Si faltan artefactos, muestra instrucciones para
prepararlos. El selector de idioma permanece disponible en todas las páginas.

`make demo` genera datos sintéticos, entrena, evalúa, guarda predicciones e inicia Streamlit. Los
datos y artefactos generados permanecen fuera de Git.

Consulta [Local interfaces](../en/interfaces.md) para los endpoints y la lista completa de
verificación manual.
