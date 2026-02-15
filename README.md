# 🧭 Pokedex Desktop App

Aplicación de escritorio desarrollada en **Python + PySide6** que permite buscar Pokémon y movimientos utilizando la **PokeAPI**.

Incluye navegación por teclado, autocompletado y visualización detallada de información.

---

## 🚀 Características

### 🔎 Búsqueda de Pokémon
- Barra de búsqueda con filtrado en tiempo real.
- Navegación con teclado:
  - ⬆ Flecha arriba
  - ⬇ Flecha abajo
  - ⏎ Enter para seleccionar
- Autocompletado automático al seleccionar un Pokémon.
- Lista que se oculta sin romper el layout.
- Obtención de datos por nombre o ID.

---

### 🧬 Información del Pokémon
Se muestran los siguientes datos:

- Nombre
- Tipos
- Habilidades (incluye hidden abilities)
- HP
- ATK
- DEF
- Sp. Atk
- Sp. Def
- Speed
- Sprite oficial

Datos obtenidos desde:
https://pokeapi.co/api/v2/pokemon/{id}

---

### ⚔ Búsqueda de Movimientos
- Barra de búsqueda independiente.
- Filtrado dinámico.
- Navegación con flechas.
- Enter para seleccionar.
- Autocompletado al seleccionar.

---

### 📖 Información del Movimiento
Actualmente muestra:
- Nombre
- Tipo

Estructura preparada para extender con:
- Poder
- Precisión
- PP
- Clase de daño
- Descripción

Datos obtenidos desde:
https://pokeapi.co/api/v2/move/{id}

---

## 🎮 Navegación por Teclado

| Tecla | Acción |
|-------|--------|
| ⬆ | Mover selección hacia arriba |
| ⬇ | Mover selección hacia abajo |
| ⏎ | Seleccionar elemento |
| Escribir | Filtrar resultados |

---

## 🛠 Tecnologías

- Python 3
- PySide6 (Qt for Python)
- Requests
- PokeAPI

---

## 📦 Instalación

```bash
pip install PySide6 requests
