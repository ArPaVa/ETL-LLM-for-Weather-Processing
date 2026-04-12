# ETL-LLM-for-Weather-Processing
## Installation
### 2. Crear el entorno virtual

```bash
python -m venv .venv
```

### 3. Activar el entorno virtual

**En PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

**En CMD:**

```bat
.\.venv\Scripts\activate.bat
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5. Desactivar el entorno virtual

```bash
deactivate
```

We are using 2 meteorogical APIs Openweathermap and weatherapi combining the info from both to get a more complete info, then we will use Gemini API to generate the suitability of some activities based on the weather info for that hour. 

