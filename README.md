# 🏹 Windranger Classic Mod para Deadlock (Grey Talon)

Mod completo y optimizado para **Deadlock** que reemplaza el modelo, armas, accesorios, habilidades y voces de **Grey Talon** por la apariencia clásica de **Windranger (Windrunner)** de **Dota 2**.

---

## ⚡ Guía de Instalación Express (En 1 Minuto)

Para instalar el mod en **cualquier computadora** no necesitas Blender ni herramientas de desarrollo. Sigue estos 2 sencillos pasos:

### 1. Copiar el archivo del mod
* **Opción A (Automática):** Ejecuta con doble clic el archivo [`install.bat`](./install.bat). Detectará automáticamente tu instalación de Steam y Deadlock y copiará el mod a la carpeta de addons.
* **Opción B (Manual):** Copia el archivo [`build/pak02_dir.vpk`](./build/pak02_dir.vpk) y pégalo en la carpeta de addons de Deadlock:
  ```text
  <Tu_Ruta_De_Steam>\steamapps\common\Deadlock\game\citadel\addons\pak02_dir.vpk
  ```
  *(Si la carpeta `addons` no existe dentro de `citadel`, créala).*

### 2. Activar la carga de mods en Deadlock (Solo la primera vez)
1. Ve a la carpeta `...\Deadlock\game\citadel\` y abre el archivo **`gameinfo.gi`** con el **Bloc de notas**.
2. Presiona `Ctrl + B` (o `Ctrl + F`) y busca el bloque **`SearchPaths`**.
3. Añade la línea `Game				citadel/addons` justo arriba de `Mod					citadel`, de modo que quede así:

```text
		SearchPaths
		{
			// These are optional low-violence paths. They will only get mounted if you're in a low-violence mode.
			Game_LowViolence	citadel_lv

			Game				citadel/addons
			Mod					citadel
			Game				citadel
		}
```
4. Guarda los cambios (`Ctrl + G` o Archivo > Guardar) y ciérralo.

¡Listo! Al iniciar Deadlock, Grey Talon aparecerá automáticamente con la apariencia y voces de Windranger.

---

## 🗑️ Desinstalación Rápida
* Ejecuta [`uninstall.bat`](./uninstall.bat) o simplemente borra el archivo `pak02_dir.vpk` de la carpeta `addons`. El juego volverá a su estado original sin afectar ningún archivo base.

---

## ✨ Características del Mod

1. **Modelo y Armadura Clásica:**
   * Apariencia fiel de Windrunner en Dota 2: túnica de cuero verde, cabellera naranja característica, carcaj superior con flechas de plumas verdes y hombrera de cuero.
   * Orientación anatómica corregida al 100% (alineación frontal y rotación del esqueleto sincronizada con Deadlock).

2. **Rigging y Animaciones Pulidas:**
   * **Mano del arco perfecta:** Influencia de deformación consolidada en `hand_L` para preservar la solidez del puño cerrado que sostiene el mango del arco, eliminando estiramientos o pellizcos en los dedos al apuntar y disparar.
   * **Flexión de codos y hombros natural:** Transición suave de pesos entre antebrazo (`arm_lower_L`) y torso.

3. **Accesorios y Habilidades:**
   * **Arco clásico:** Arco de madera recurva tradicional de Windrunner con cuerda tensada.
   * **Halcón / Lechuza de la Ultimate:** Reemplazo en alta definición (4K) para la habilidad definitiva de Grey Talon.

4. **Paquete Completo de Audio (200+ Voces):**
   * Más de 200 líneas de voz originales en inglés de Windranger adaptadas a todas las acciones de juego: ataques básicos, saltos, recargas, habilidades, emotes, asesinatos y selección en el menú.

5. **Interfaz de Usuario (UI):**
   * Prefab 3D para el menú de inspección y pedestal de selección de héroes (`maps/ui/hero_prefabs/archer.vpk`).

6. **Compatibilidad:**
   * Diseñado como paquete aislado **`pak02_dir.vpk`**, lo que permite convivir limpiamente con otros mods instalados (como el mod de Dynamo en `pak01_dir.vpk`) sin sobreescribirse ni causar colisiones.

---

## 📁 Estructura del Repositorio

```text
├── build/
│   └── pak02_dir.vpk          # Mod compilado listo para usar (~39.5 MB)
├── custom_mod_source/         # Recursos fuente del mod listos para empaquetado
│   ├── models/                # Modelos Source 2 compilados (.vmdl_c)
│   ├── materials/             # Shaders y materiales PBR (.vmat_c, .vtex_c)
│   ├── sounds/                # Banco de voces de Windranger (.vsnd_c)
│   └── maps/                  # Prefabs 3D de UI para el menú principal
├── dota2_extracted/           # Mallas base originales extraídas de Dota 2
├── extracted/                 # Plantillas DMX y mallas de referencia
├── tools/                     # Pipeline automatizado en Python y scripts de Blender
│   ├── build_restored_perfect_windrunner.py  # Script de Blender para pesado y exportación DMX
│   ├── compile_clean_vmdl.py                 # Compilador con resourcecompiler de Source 2
│   ├── repack_and_install.py                 # Empaquetador VPK e instalador directo
│   └── build_mod.py                          # Constructor rápido de paquetes VPK
├── install.bat                # Instalador express de 1 clic
├── uninstall.bat              # Desinstalador express
├── build.bat                  # Script de recompilación rápida
└── README.md
```

---

## 🛠️ Herramientas para Desarrolladores

Si deseas modificar o reconstruir el mod desde cero:
* **Blender:** Se utilizó Blender 4.x / 5.x junto con la librería `dmx` para transferir pesos y mapeo de vértices entre los esqueletos de Dota 2 y Deadlock.
* **Source 2 Resource Compiler:** Para compilar archivos `.vmdl` a `.vmdl_c`.
* **Python VPK:** Para empaquetar la estructura de archivos en un archivo VPK estándar de Valve.
