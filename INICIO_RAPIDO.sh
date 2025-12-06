#!/bin/bash
# 🚀 Script de Inicio Rápido - Sacred Rebirth AI Agent
# Ejecuta: bash INICIO_RAPIDO.sh

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                                                           ║"
echo "║     🌟 SACRED REBIRTH AI MARKETING AGENT - SETUP 🌟      ║"
echo "║                                                           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verificar Python
echo "📋 Verificando requisitos..."
echo ""

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 no está instalado${NC}"
    echo "   Instálalo desde: https://python.org"
    exit 1
else
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✅ $PYTHON_VERSION instalado${NC}"
fi

# Verificar pip
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}❌ pip no está instalado${NC}"
    exit 1
else
    echo -e "${GREEN}✅ pip instalado${NC}"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Instalar dependencias
echo "📦 Instalando dependencias..."
echo ""

if pip3 install -r requirements.txt; then
    echo ""
    echo -e "${GREEN}✅ Dependencias instaladas correctamente${NC}"
else
    echo ""
    echo -e "${RED}❌ Error instalando dependencias${NC}"
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Configurar .env
if [ ! -f .env ]; then
    echo "⚙️  Configurando variables de entorno..."
    echo ""
    cp .env.example .env
    echo -e "${YELLOW}⚠️  IMPORTANTE: Debes editar .env y agregar tu OPENAI_API_KEY${NC}"
    echo ""
    echo "   Ejecuta: nano .env"
    echo "   O: code .env"
    echo ""
else
    echo -e "${GREEN}✅ Archivo .env ya existe${NC}"
    echo ""
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Verificar estructura
echo "📁 Verificando estructura de archivos..."
echo ""

REQUIRED_DIRS=("config" "data" "src" "data/generated" "data/reports")
for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo -e "${GREEN}✅ $dir/${NC}"
    else
        echo -e "${YELLOW}⚠️  $dir/ no existe, creando...${NC}"
        mkdir -p "$dir"
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Verificar archivos principales
REQUIRED_FILES=("main.py" "ejemplos.py" "config/settings.py" "config/prompts.py")
echo "📄 Verificando archivos principales..."
echo ""

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✅ $file${NC}"
    else
        echo -e "${RED}❌ $file no encontrado${NC}"
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Hacer ejecutables
echo "🔧 Configurando permisos..."
echo ""
chmod +x main.py ejemplos.py
echo -e "${GREEN}✅ Permisos configurados${NC}"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Resumen
echo "🎉 ¡INSTALACIÓN COMPLETADA!"
echo ""
echo "═══════════════════════════════════════════════════════════"
echo ""
echo -e "${GREEN}✅ Dependencias instaladas${NC}"
echo -e "${GREEN}✅ Estructura de archivos verificada${NC}"
echo -e "${GREEN}✅ Permisos configurados${NC}"
echo ""
echo "═══════════════════════════════════════════════════════════"
echo ""

# Próximos pasos
echo "📋 PRÓXIMOS PASOS:"
echo ""
echo "1️⃣  Configurar tu API Key de OpenAI:"
echo "   ${YELLOW}nano .env${NC}"
echo "   ${YELLOW}# Agregar: OPENAI_API_KEY=sk-tu-key-aqui${NC}"
echo ""
echo "2️⃣  Probar con ejemplos:"
echo "   ${YELLOW}python ejemplos.py${NC}"
echo ""
echo "3️⃣  O ejecutar el programa principal:"
echo "   ${YELLOW}python main.py${NC}"
echo ""
echo "4️⃣  Generar tu primer post:"
echo "   ${YELLOW}python main.py --mode social --platform instagram --topic \"Ayahuasca\"${NC}"
echo ""
echo "═══════════════════════════════════════════════════════════"
echo ""

# Documentación
echo "📚 DOCUMENTACIÓN DISPONIBLE:"
echo ""
echo "   • ${GREEN}README.md${NC} - Vista general"
echo "   • ${GREEN}GUIA_USO.md${NC} - Guía completa de uso"
echo "   • ${GREEN}INSTALACION.md${NC} - Instalación detallada"
echo "   • ${GREEN}COMANDOS.md${NC} - Lista de comandos útiles"
echo "   • ${GREEN}ARQUITECTURA.md${NC} - Documentación técnica"
echo "   • ${GREEN}RESUMEN.md${NC} - Resumen del proyecto"
echo ""

# Verificar OpenAI key
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if grep -q "OPENAI_API_KEY=sk-" .env 2>/dev/null; then
    echo -e "${GREEN}✅ OPENAI_API_KEY configurada en .env${NC}"
    echo ""
    echo "🚀 ¡TODO LISTO! Puedes empezar a usar el agente:"
    echo ""
    echo "   ${YELLOW}python main.py${NC}"
    echo ""
else
    echo -e "${YELLOW}⚠️  OPENAI_API_KEY no configurada${NC}"
    echo ""
    echo "   Antes de usar el agente, configura tu API key:"
    echo "   ${YELLOW}nano .env${NC}"
    echo ""
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "¡Bienvenido al futuro del marketing automatizado! 🚀✨"
echo ""
echo "Sacred Rebirth - Marketing Agent con IA"
echo ""
