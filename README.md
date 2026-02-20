# 🗂️ MyOptimizer

**MyOptimizer** es una aplicación de escritorio para Windows desarrollada con [Flet](https://flet.dev/) que automatiza la **organización y optimización de archivos** en tus carpetas. Clasifica tus ficheros en categorías configurables, elimina duplicados de forma inteligente y te permite gestionar múltiples perfiles de configuración sin tocar ningún archivo JSON a mano.

---

## ✨ Características principales

### 📁 Organización de archivos
- Selecciona una o varias **carpetas de origen** para organizar.
- Define una **carpeta de destino** donde se copiará o moverá el resultado.
- Los archivos se clasifican automáticamente en subcarpetas según su extensión y el perfil activo.
- **Detección de duplicados** en dos pasadas:
  1. Hash parcial de los primeros 64 KB (elimina el 99 % de falsos positivos).
  2. Hash SHA-256 completo para confirmación definitiva.
- Procesamiento paralelo con `ThreadPoolExecutor` para máxima velocidad.

### 👤 Gestión de perfiles
Cada perfil es un fichero `config_<nombre>.json` almacenado en el directorio de datos del usuario (`%APPDATA%\MarcRoviraP\MyOptimizer\config\`).

| Acción | Descripción |
|---|---|
| **Nuevo perfil** | Escribe un nombre → clic `+`. El perfil se crea vacío (sin categorías). |
| **Clonar perfil** | Icono 📋 en la tarjeta → introduce un nombre único → se copia el JSON íntegro. |
| **Editar perfil** | Icono ✏️ en la tarjeta → abre el editor de árbol. |
| **Renombrar perfil** | Dentro del editor, botón "Renombrar perfil" bajo el nombre → introduce el nuevo nombre. |
| **Eliminar perfil** | Icono 🗑️ en la tarjeta → dialog de confirmación. |

### 🛠️ Editor de perfil
El editor muestra un **árbol jerárquico** de categorías con sus extensiones:
- **Añadir/eliminar extensiones** por categoría (campo de texto + botón).
- **Drag & drop**: arrastra una extensión de una categoría a otra.
- **Crear/eliminar categorías** al vuelo.
- **Guardar** cambios con el botón 💾; indicador de estado en tiempo real.
- **Restaurar** el estado guardado con el botón ↺.

### 👁️ Vista previa antes de aplicar
Antes de mover o copiar cualquier archivo, la vista previa muestra:
- Qué archivos serán procesados, agrupados por categoría.
- Barra de progreso por categoría durante la operación.
- Elección de modo: **Copiar** o **Mover**.

---

## 🎨 Perfil por defecto (`config_Optimizador`)

El perfil predeterminado incluye **21 categorías** listas para usar:

| Categoría | Extensiones (ejemplos) |
|---|---|
| Fotos | jpg, jpeg, png, gif, heic, raw, cr2… |
| Imágenes Vectoriales | svg, ai, eps, cdr |
| Documentos PDF | pdf |
| Documentos Word | doc, docx, odt, rtf… |
| Hojas de Cálculo | xls, xlsx, ods, csv… |
| Presentaciones | ppt, pptx, odp, key… |
| Documentos Texto Plano | txt, md, markdown, tex |
| Ebooks | epub, mobi, azw, fb2 |
| Formularios y Datos | xml, json, yaml, yml, xsd |
| Programas | exe, msi, bat, apk, jar… |
| Comprimidos | zip, rar, 7z, tar, iso… |
| Videos | mp4, mkv, avi, mov, webm… |
| Audio | mp3, wav, flac, ogg… |
| Código | py, js, ts, html, css, java, go, rs… |
| Bases de Datos | db, sqlite, mdb, accdb |
| Configuración | ini, cfg, conf, env |
| Fuentes | ttf, otf, woff, woff2 |
| Logs | log |
| Temporales | tmp, temp, bak, old |
| Accesos Directos | lnk, url, desktop |
| Otros | *(vacía — archivos no clasificados)* |

---

## 🏗️ Arquitectura

```
MyOptimizer/
├── src/
│   ├── main.py               # UI completa en Flet (todas las vistas)
│   ├── utils.py              # Lógica de negocio: Configuracion, deduplicación, organización
│   ├── config_Optimizador.json  # Perfil por defecto (copiado al instalar)
│   └── assets/
│       └── myOptimizer.ico   # Icono de la aplicación
├── pyproject.toml            # Metadatos del proyecto y configuración flet build
└── README.md
```

### Clases y módulos clave

#### `Configuracion` (`utils.py`)
| Método | Descripción |
|---|---|
| `getProfiles()` | Lista todos los `config_*.json` del directorio de configuración. |
| `viewProfile(perfil)` | Carga y devuelve el JSON del perfil como dict. |
| `setPerfil(perfil)` | Establece el perfil activo. |
| `setDestinyPath(path)` | Define la carpeta de destino. |
| `addFolderToStructure(path)` | Añade una carpeta de origen. |
| `removeFolderFromStructure(path)` | Elimina una carpeta de origen. |
| `getStructureFolder()` | Escanea las carpetas de origen y devuelve `{categoría: [Path, ...]}` sin duplicados. |
| `applyOrganization(modo, on_progress)` | Ejecuta la copia/movimiento con callback de progreso. |

#### Vistas principales (`main.py`)
| Función | Descripción |
|---|---|
| `systemUI()` | Panel de carpeta de destino. |
| `folderOrganizerUI()` | Grid de carpetas de origen. |
| `profilesUI()` | Panel lateral de perfiles. |
| `createProfileUI(perfil)` | Tarjeta individual de perfil con acciones. |
| `viewEditarPerfil(perfil)` | Editor de árbol de categorías/extensiones. |
| `viewPreviewPerfil(perfil)` | Vista previa + aplicar organización. |
| `tooglePreviewView(...)` | Alterna entre vista previa y editor. |
| `dialogClonarPerfil(perfil)` | Dialog para clonar un perfil. |
| `dialogRenombrarPerfil(perfil, ref)` | Dialog para renombrar un perfil. |
| `dialogSeguroEliminarPerfil(perfil)` | Dialog de confirmación para eliminar. |

---

## 🚀 Instalación y ejecución

### Requisitos previos
- Python **3.10+**
- [Flet](https://flet.dev/) >= 0.80.5

### Modo desarrollo

```bash
# Clonar el repositorio
git clone https://github.com/MarcRoviraP/MyOptimizer.git
cd MyOptimizer

# Crear entorno virtual e instalar dependencias
python -m venv .venv
.venv\Scripts\activate
pip install -e .

# Ejecutar
python src/main.py
```

### Compilar el ejecutable de Windows

```bash
flet build windows
```

El ejecutable quedará en `build/windows/MyOptimizer.exe`.

---

## 💡 Cómo usar

1. **Añade carpetas de origen** en el panel "Carpetas a organizar" (botón `Agregar carpeta`).
2. **Selecciona la carpeta de destino** en el panel superior.
3. **Elige o crea un perfil** en el panel de configuración (derecha).
4. Si quieres personalizar las categorías, haz clic en ✏️ → edita el árbol → 💾 Guardar.
5. Haz clic en el perfil para ver la **vista previa** de los archivos que se organizarán.
6. Elige **Copiar** o **Mover** y pulsa **Aplicar**.

---

## 🔒 Almacenamiento de datos

Los perfiles se almacenan en el directorio estándar de datos de usuario de Windows:

```
%APPDATA%\MarcRoviraP\MyOptimizer\config\
```

Esto garantiza que los datos persisten entre versiones y no se pierden al desinstalar la aplicación.

---

## 📄 Licencia

Copyright © 2026 MarcRoviraP. Todos los derechos reservados.