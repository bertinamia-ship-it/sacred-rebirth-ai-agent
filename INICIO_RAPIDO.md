# ⚡ INICIO RÁPIDO - 3 PASOS

## 🎯 Para tener el agente funcionando en 5 minutos

---

## ✅ PASO 1: Instalar (1 minuto)

```bash
pip install -r requirements.txt
```

---

## ✅ PASO 2: Configurar OpenAI (3 minutos)

### Opción A: Script Automático (MÁS FÁCIL)

```bash
bash configurar.sh
```
El script te guiará paso a paso.

### Opción B: Manual

1. **Consigue tu API Key:**
   - Ve a: https://platform.openai.com/api-keys
   - Click "Create new secret key"
   - Copia la key (empieza con `sk-...`)

2. **Configura:**
   ```bash
   cp .env.example .env
   nano .env
   ```

3. **Edita la línea:**
   ```
   OPENAI_API_KEY=sk-TU-KEY-AQUI
   ```

4. **Guarda:** Ctrl+O, Enter, Ctrl+X

---

## ✅ PASO 3: ¡Usar! (1 minuto)

### 💬 Modo CHAT (Recomendado)

```bash
python chat.py
```

Luego habla naturalmente:
```
💬 "crea un post de instagram sobre ayahuasca"
💬 "necesito una campaña para el retiro de enero"
💬 "muéstrame las métricas"
```

### O usa el menú tradicional:

```bash
python main.py
```

---

## 🎉 ¡LISTO!

Con solo OpenAI configurado ya puedes:

✅ Generar posts de Instagram  
✅ Generar posts de Facebook  
✅ Crear emails  
✅ Planificar estrategias  
✅ Gestionar leads  
✅ **Hablar con el agente en modo chat** 💬  

---

## 📚 Siguiente Nivel (OPCIONAL)

Para publicar automáticamente:

**Instagram/Facebook:** Lee [CONFIGURACION.md](CONFIGURACION.md) sección "Paso 3"  
**Emails:** Lee [CONFIGURACION.md](CONFIGURACION.md) sección "Paso 4"

---

## 🆘 Problemas?

```bash
# Verifica que .env existe
ls -la .env

# Verifica tu API key
cat .env | grep OPENAI_API_KEY

# Debe mostrar algo como:
# OPENAI_API_KEY=sk-proj-abc123...
```

Si sigue sin funcionar, lee [CONFIGURACION.md](CONFIGURACION.md)

---

## 💡 Ejemplos de Uso

```bash
# Modo chat
python chat.py
> "crea un post sobre kambo"

# Modo comando
python main.py --mode social --platform instagram --topic "Ayahuasca"

# Modo interactivo
python main.py
# Luego selecciona opción 2
```

---

## 📖 Documentación Completa

- **CONFIGURACION.md** - Guía detallada de setup
- **GUIA_USO.md** - Manual completo de uso
- **README.md** - Documentación general
- **ARQUITECTURA.md** - Documentación técnica

---

**¡Empieza ahora! 🚀**

```bash
bash configurar.sh
python chat.py
```
