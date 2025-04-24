#!/usr/bin/env python3
import os
import subprocess
import logging
import sys
from pathlib import Path

def load_env_file(env_path):
    """
    Carga variables de un .env en os.environ sin librerías externas.
    Formato por línea: KEY=VALUE, ignora comentarios (#) y líneas vacías.
    """
    if not env_path.is_file():
        logging.warning(f"No se encontró .env en {env_path}")
        return

    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, val = line.split('=', 1)
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        os.environ.setdefault(key, val)

def run_command(cmd, cwd=None):
    logging.info(f"Ejecutando...")
    try:
        r = subprocess.run(
            cmd,
            cwd=cwd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if r.stdout:
            logging.info(r.stdout.strip())
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Error en {' '.join(cmd)}:\n{e.stderr.strip()}")
        return False

def main():
    # 1) Cargar .env desde la carpeta del script
    script_dir = Path(__file__).parent
    load_env_file(script_dir / ".env")

    # 2) Leer variables necesarias
    token     = os.getenv("GITHUB_TOKEN")
    owner     = os.getenv("REPO_OWNER")
    repo      = os.getenv("REPO_NAME")
    base_path = os.getenv("REPO_BASE_PATH", "/opt")
    service   = os.getenv("SERVICE_NAME", "odoo")

    if not token or not owner or not repo:
        logging.error("Faltan GITHUB_TOKEN, REPO_OWNER o REPO_NAME en el .env")
        sys.exit(1)

    repo_dir = os.path.join(base_path, repo)
    if not os.path.isdir(repo_dir):
        logging.error(f"No existe el directorio del repo: {repo_dir}")
        sys.exit(1)

    # 3) Hacer git pull
    git_url = f"https://{token}@github.com/{owner}/{repo}.git"
    if not run_command(["git", "pull", git_url], cwd=repo_dir):
        sys.exit(1)

    # 4) Reiniciar servicio
    if not run_command(["sudo", "service", service, "restart"]):
        sys.exit(1)

    logging.info("Actualización completada con éxito.")
    sys.exit(0)

if __name__ == "__main__":
    # Logging sólo a consola
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s: %(message)s"
    )
    logging.info("=== Inicio de actualización de repositorio ===")
    main()