# 🏹 Windranger Classic Mod para Deadlock (Grey Talon)

Mod completo y pulido para **Deadlock** que reemplaza a **Grey Talon** por la apariencia clásica de **Windranger (Windrunner)** de **Dota 2**, incluyendo modelo 3D corregido, armas, habilidades, todas las pantallas de interfaz (UI/Cards) y más de 200 líneas de voz.

---

## ⚡ Tutorial Express de Instalación (Solo 2 Pasos)

Instalar el mod en cualquier computadora toma menos de 1 minuto:

### Paso 1: Copiar el mod a Deadlock
Elige **una** de las siguientes dos opciones:
* **Opción Automática (Recomendada):** Haz doble clic en [`install.bat`](./install.bat). Detectará automáticamente tu juego y copiará el archivo por ti.
* **Opción Manual:** Copia el archivo [`build/pak02_dir.vpk`](./build/pak02_dir.vpk) y pégalo dentro de:
  ```text
  ...\Steam\steamapps\common\Deadlock\game\citadel\addons\
  ```
  *(Si la carpeta `addons` no existe, simplemente créala dentro de `citadel`).*

---

### Paso 2: Activar la carga de mods (Solo se hace 1 vez)
1. Abre tu carpeta del juego: `...\Deadlock\game\citadel\`.
2. Abre el archivo **`gameinfo.gi`** con el **Bloc de notas**.
3. Presiona `Ctrl + B` y busca: `SearchPaths`.
4. Agrega la línea `Game				citadel/addons` justo arriba de `Mod					citadel`:

```text
		SearchPaths
		{
			Game_LowViolence	citadel_lv

			Game				citadel/addons
			Mod					citadel
			Game				citadel
		}
```
5. Guarda el archivo (`Ctrl + G`) y ciérralo.

**¡Listo! Ya puedes abrir Deadlock.** En el menú principal, selección de héroes y en partida verás y escucharás a Windranger clásica.

---

## 🗑️ ¿Cómo desinstalar el mod?
* Haz doble clic en [`uninstall.bat`](./uninstall.bat) o borra el archivo `pak02_dir.vpk` de la carpeta `addons`. El juego volverá a su estado original sin alterar ningún archivo base.

---

## ✨ Contenido y Mejoras Incluidas

1. **Pantallas e Interfaz de Usuario (UI) 100% Clásica:**
   * **Tarjetas de selección de héroe (`archer_card_psd`):** Tarjeta principal de la galería de héroes con el arte clásico de Windrunner.
   * **Tarjetas de estado:** Versiones para baja salud (`critical`) y victoria (`gloat`).
   * **Ranura vertical de lobby (`archer_vertical_psd`):** Busto vertical de Windranger para la cola de emparejamiento.
   * **Avatar e icono HUD (`archer_sm_psd`):** Retrato para la tabla de puntuación, barra superior y registro de bajas.
   * **Icono de minimapa (`archer_mm_psd`):** Icono circular clásico nítido para el minimapa en partida.
   * **Pedestal 3D del menú:** Eliminada la estatua estática del Arcano; ahora la selección y vista previa del héroe carga directamente nuestro modelo 3D animado de Windranger clásica.

2. **Modelo 3D y Armadura Clásica:**
   * Túnica de cuero verde, cabellera naranja icónica, hombrera de cuero verde y carcaj de flechas en la espalda alta.
   * Orientación anatómica y escala 1:1 sincronizada con Deadlock.

3. **Rigging Pulido y Mano del Arco Sólida:**
   * Pesos consolidados en `hand_L` para mantener el puño cerrado firme y sin desgarros ni pellizcos al tensar la cuerda y disparar el arco.
   * Flexión natural del codo (`arm_lower_L`) y hombros.

4. **Arco y Flechas Clásicas:**
   * Arco de madera recurva tradicional con cuerda tensada y flechas con plumas verdes.

5. **Halcón / Búho 4K de la Ultimate:**
   * Modelo y textura en alta resolución para la habilidad definitiva de Grey Talon.

6. **Más de 200 Líneas de Voz Clásicas:**
   * Banco de sonido original de Windranger adaptado a todas las acciones de Grey Talon (ataques, saltos, recargas, habilidades, emotes y selección).

7. **Compatibilidad:**
   * Configurado como `pak02_dir.vpk`, convive a la perfección con otros mods (como Dynamo en `pak01_dir.vpk`).

---

## 📁 Estructura del Repositorio

```text
├── build/
│   └── pak02_dir.vpk          # Paquete completo compilado (~33.7 MB)
├── custom_mod_source/         # Recursos fuente del mod
│   ├── models/                # Modelos 3D (.vmdl_c) de Windranger y el Halcón
│   ├── materials/             # Shaders y texturas (.vmat_c, .vtex_c)
│   ├── panorama/              # Tarjetas, iconos y avatares de interfaz
│   └── sounds/                # Banco de voces completo (.vsnd_c)
├── tools/                     # Scripts de compilación, pipeline y automatización
├── install.bat                # Instalador automático en 1 clic
├── uninstall.bat              # Desinstalador automático
└── README.md                  # Este documento
```
