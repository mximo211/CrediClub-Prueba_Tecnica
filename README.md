# Payment Reconciliation API - Prueba Técnica
## Resumen
Este proyecto implementa todo lo solicitado en el pdf "Prueba Técnica Trainees.pdf"
La demostración de habilidades en:
* Lenguaje: Python 3.10 o superior 
* Framework: FastAPI
* Base de datos: SQLite
* Generación de archivos: Excel (.xlsx)
* Consumo de API pública (HTTP REST)

## Instalación
Instrucciones de instalación:
1. Clonar repositorio:
git clone <your-repository-url>
cd <repository-folder>

2. Crear entorno virtual:
.venv\Scripts\activate

3. Instalar el requirements txt que incluye todas las librerias para correr el codigo:
pip install -r requirements.txt

4. En la línea 71 del código es IMPERATIVO borrar del api key el texto "(delete this section including parenthesis)" incluyendo los parentésis.

   
## Correr el código
Para correr el codigo de manera adecuada es IMPORTANTE realizar todos los pasos de instalación.
1. Correr el código de manera normal.
2. Escribir el siguiente código en la terminal para encender el FastAPI server:
   uvicorn main:app --reload
3. Abrir en la web el siguiente enlace local:
  http://127.0.0.1:8000/docs
4. Escoger la opción POST y escribir el Bash del cuál se quiere un reporte (ejemplo BA-202401).
5. Descargar reporte una vez haya cargado.
6. Una vez que se tengan los reportes que se buscaban regresar al código y en la terminal utilizar ctrl + c para cerrar el servidor.


## Referencias de consumo del Exchange Rate API (API externa)
* Documentación oficial: https://www.exchangerate-api.com/docs/overview
* Endpoint utilizado:
  https://v6.exchangerate-api.com/v6/YOUR_API_KEY/latest/MXN
  Se utilizó para obtener la actual conversión de la moneda mexicana a varias otras monedas del mundo. En el reporte se utilizó la conversión hacía la moneda americana.

## Referencias de consumo del GenAI API (LLM)
* Documentación oficial: https://ai.google.dev/gemini-api/docs?hl=es-419
* Modelo utilizado: model="gemini-3-flash-preview"
* Se utilizo para generar un resumen sobre los contenidos del reporte desde un enfoque analistíca de datos.
