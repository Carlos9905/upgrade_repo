# Uso del script `upgrade_repo.py`

Este documento explica cómo configurar y utilizar el script de Python `upgrade_repo.py` para automatizar la actualización de tu repositorio Git y el reinicio de tu servicio en Ubuntu.

---

## 1. Requisitos previos

- **Python 3.x** instalado en el servidor.
- Acceso de usuario al directorio del repositorio local.
- Archivo **`.env`** con las variables de entorno (ver sección siguiente).
- Ejecución con **permisos de `sudo`** para evitar errores de permiso.

---

## 2. Archivo `.env`

En la misma carpeta donde esté el script, crea un archivo llamado `.env` con el siguiente contenido:

```env
GITHUB_TOKEN=<tu_token_de_github>
REPO_OWNER=<owner_del_repo>
REPO_NAME=<nombre_del_repo>
REPO_BASE_PATH=/opt
SERVICE_NAME=odoo
```

- **GITHUB_TOKEN**: Token de acceso personal de GitHub.
- **REPO_OWNER**: Usuario u organización propietaria del repo.
- **REPO_NAME**: Nombre del repositorio (igual al nombre de la carpeta en `/opt`).
- **REPO_BASE_PATH**: Ruta base donde se encuentran los repositorios (por defecto `/opt`).
- **SERVICE_NAME**: Nombre del servicio a reiniciar (por defecto `odoo`).

---

## 3. Ejecución del script

1. **Concede permisos de ejecución** al script (solo la primera vez):
   ```bash
   chmod +x /ruta/al/script/upgrade_repo.py
   ```

2. **Ejecuta el script con `sudo`:**
   ```bash
   sudo python3 /ruta/al/script/upgrade_repo.py
   ```

### Ejemplo de salida
```text
2025-04-24 20:36:19,055 INFO: === Inicio de actualización de repositorio ===
2025-04-24 20:36:19,056 INFO: Ejecutando: git pull https://<token>@github.com/<owner>/<repo-name>.git (cwd=/opt/<repo-name>)
2025-04-24 20:36:19,063 INFO: Actualización completada con éxito.
```

---

## 4. Solución de problemas comunes

- **`Permission denied: '.git/FETCH_HEAD'`**: asegúrate de ejecutar con `sudo` o cambia la propiedad del directorio con `chown`.
- **Variables de entorno faltantes**: comprueba que `.env` contiene `GITHUB_TOKEN`, `REPO_OWNER` y `REPO_NAME` correctamente.
- **Directorio del repositorio no existe**: verifica que la carpeta `/opt/<REPO_NAME>` exista.

---

> Si tienes dudas o necesitas ampliar funcionalidades (notificaciones, múltiples repos, etc.), ¡avísame!
