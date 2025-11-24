import PyInstaller.__main__
import customtkinter
import os

# 1. Obtener la ruta de instalación de CustomTkinter
ctk_path = os.path.dirname(customtkinter.__file__)

# 2. Argumentos para PyInstaller en Windows
args = [
    'main.py',                            # Tu archivo principal
    '--name=CalculadoraSueldos',          # Nombre del .exe final
    '--noconsole',                        # Ocultar la pantalla negra (CMD) de fondo
    '--onedir',                           # Crear una CARPETA (Vital para que funcione el .env editable)
    '--clean',                            # Limpiar caché de compilaciones fallidas
    
    # IMPORTANTE: Incluir los archivos de diseño de CustomTkinter
    f'--add-data={ctk_path};customtkinter/',
    
    # Importaciones ocultas (Módulos que a veces PyInstaller no ve)
    '--hidden-import=pyodbc',
    '--hidden-import=dotenv',
    '--hidden-import=DATA',
    '--hidden-import=UI',
    '--hidden-import=SERVICE',
    
    # AGREGA ESTAS DOS LÍNEAS NUEVAS:
    '--icon=assets/logo.ico', 
    
    # 2. Le decimos que COPIE el archivo dentro de la carpeta final (para que la ventana lo encuentre)
    '--add-data=assets/logo.ico;assets/'
]

print("🚀 Iniciando compilación en Windows...")
PyInstaller.__main__.run(args)