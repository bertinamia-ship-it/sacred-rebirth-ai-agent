#!/bin/bash
# 🚂 Script automático para deploy en Railway

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║       🚂 RAILWAY DEPLOYMENT - Sacred Rebirth Bot            ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Función de error
error_exit() {
    echo -e "${RED}❌ Error: $1${NC}" 1>&2
    exit 1
}

# Función de éxito
success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Función de advertencia
warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

echo "1️⃣  Verificando requisitos..."

# Verificar que estamos en el directorio correcto
if [ ! -f "telegram_bot.py" ]; then
    error_exit "No se encontró telegram_bot.py. Ejecuta este script desde la raíz del proyecto."
fi
success "Directorio correcto"

# Verificar git
if ! command -v git &> /dev/null; then
    error_exit "Git no está instalado. Instálalo con: sudo apt install git"
fi
success "Git instalado"

# Verificar archivos necesarios
FILES=("railway.json" "Procfile" "requirements.txt" "telegram_bot.py" ".gitignore")
for file in "${FILES[@]}"; do
    if [ ! -f "$file" ]; then
        error_exit "Falta archivo: $file"
    fi
done
success "Todos los archivos necesarios presentes"

echo ""
echo "2️⃣  Verificando .gitignore..."

# Verificar que .env está en .gitignore
if ! grep -q "^\.env$" .gitignore 2>/dev/null; then
    warning ".env no está en .gitignore, agregándolo..."
    echo ".env" >> .gitignore
    echo "*.log" >> .gitignore
    echo "backups/" >> .gitignore
    echo "__pycache__/" >> .gitignore
    echo "*.pyc" >> .gitignore
fi
success ".gitignore configurado correctamente"

echo ""
echo "3️⃣  Configurando Git..."

# Inicializar git si no existe
if [ ! -d ".git" ]; then
    git init
    success "Git inicializado"
else
    success "Git ya inicializado"
fi

# Configurar usuario si no está configurado
if [ -z "$(git config user.name)" ]; then
    echo ""
    read -p "👤 Tu nombre para Git: " git_name
    git config user.name "$git_name"
fi

if [ -z "$(git config user.email)" ]; then
    echo ""
    read -p "📧 Tu email para Git: " git_email
    git config user.email "$git_email"
fi

success "Git configurado"

echo ""
echo "4️⃣  Verificando cambios..."

# Mostrar status
git status --short

echo ""
read -p "¿Quieres continuar con el commit? (s/n): " continue_commit

if [ "$continue_commit" != "s" ]; then
    warning "Cancelado por el usuario"
    exit 0
fi

echo ""
echo "5️⃣  Haciendo commit..."

# Agregar archivos
git add .

# Commit
echo ""
read -p "📝 Mensaje del commit [Deploy a Railway]: " commit_msg
commit_msg=${commit_msg:-"Deploy a Railway"}

git commit -m "$commit_msg" || warning "No hay cambios para commitear"
success "Commit realizado"

echo ""
echo "6️⃣  Configurando repositorio remoto..."

# Verificar si ya existe remote
if git remote get-url origin &> /dev/null; then
    REPO_URL=$(git remote get-url origin)
    echo "   Remote actual: $REPO_URL"
    read -p "¿Usar este remote? (s/n): " use_existing
    
    if [ "$use_existing" != "s" ]; then
        read -p "📦 URL del repositorio GitHub: " new_repo_url
        git remote remove origin
        git remote add origin "$new_repo_url"
    fi
else
    echo ""
    echo "   Necesitas crear un repositorio en GitHub:"
    echo "   👉 https://github.com/new"
    echo ""
    read -p "📦 URL del repositorio GitHub (ej: https://github.com/usuario/repo.git): " repo_url
    git remote add origin "$repo_url"
fi

success "Remote configurado"

echo ""
echo "7️⃣  Pusheando a GitHub..."

# Asegurar que estamos en main
git branch -M main

# Push
if git push -u origin main; then
    success "Código subido a GitHub"
else
    warning "Error al pushear. Puede que necesites autenticarte."
    echo ""
    echo "   Si es tu primera vez, necesitas:"
    echo "   1. Personal Access Token de GitHub"
    echo "   2. O configurar SSH keys"
    echo ""
    echo "   Guía: https://docs.github.com/en/authentication"
    echo ""
    read -p "¿Reintentar push? (s/n): " retry
    if [ "$retry" = "s" ]; then
        git push -u origin main || error_exit "No se pudo pushear"
    fi
fi

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                  ✅ CÓDIGO EN GITHUB                         ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

echo "📝 PRÓXIMOS PASOS EN RAILWAY:"
echo ""
echo "1. Ve a: https://railway.app"
echo ""
echo "2. Login con GitHub"
echo ""
echo "3. New Project → Deploy from GitHub repo"
echo ""
echo "4. Selecciona tu repositorio"
echo ""
echo "5. Configura Variables (Settings → Variables):"
echo "   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Leer variables de .env si existe
if [ -f ".env" ]; then
    echo "   📋 COPIA ESTAS VARIABLES A RAILWAY:"
    echo ""
    
    while IFS= read -r line; do
        # Ignorar comentarios y líneas vacías
        if [[ ! "$line" =~ ^# ]] && [[ -n "$line" ]]; then
            # Obtener nombre de variable (antes del =)
            var_name=$(echo "$line" | cut -d= -f1)
            # Mostrar solo nombre (no valor por seguridad en terminal)
            echo "   • $var_name"
        fi
    done < .env
    
    echo ""
    echo "   ⚠️  IMPORTANTE: Copia los VALORES de tu archivo .env"
    echo ""
else
    echo "   Variables necesarias:"
    echo "   • OPENAI_API_KEY"
    echo "   • OPENAI_MODEL"
    echo "   • TELEGRAM_BOT_TOKEN"
    echo "   • TELEGRAM_AUTHORIZED_USERS"
    echo "   • (y otras de tu .env)"
    echo ""
fi

echo "6. Deploy automático comenzará"
echo ""
echo "7. Ver logs: Tab 'Logs' en Railway"
echo ""
echo "8. Verifica en Telegram: @Marketing9502_bot"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📚 Guía completa: RAILWAY_SETUP.md"
echo ""
echo "🎉 ¡Listo para deploy 24/7!"
echo ""
