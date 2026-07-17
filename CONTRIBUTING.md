# Contributing

Gracias por tu interés en contribuir a FileHasher.

## Requisitos

- Python 3.13 o superior

## Instalación

```bash
git clone https://github.com/dcobpri/FileHasher.git
cd FileHasher
pip install -e .
```

## Comprobación del código

Antes de realizar un commit ejecuta:

```bash
ruff check .
black .
pyright
pytest -v
```

Todos los comandos deben finalizar sin errores.

## Estilo de desarrollo

- Realizar commits pequeños y descriptivos.
- Mantener la arquitectura del proyecto.
- Añadir pruebas para toda nueva funcionalidad.
- Mantener el código formateado con Black.