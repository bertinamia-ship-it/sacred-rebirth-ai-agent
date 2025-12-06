"""
Prompts templates para generación de contenido con IA
"""

INSTAGRAM_POST_PROMPT = """
Eres un experto en marketing espiritual y wellness. Crea un post atractivo para Instagram para Sacred Rebirth.

Información del negocio:
- Nombre: Sacred Rebirth
- Ubicación: Valle de Bravo, Mexico
- Servicios: Retiros de Ayahuasca, Kambo, Rapé, Qigong
- Próximo retiro: 11 de Enero, 2026
- Website: https://sacred-rebirth.com
- Instagram: @sacredrebirthvalle

Tema del post: {topic}

Requisitos:
- Texto en español
- Máximo 2200 caracteres
- Incluye emojis relevantes
- Tono: Espiritual, acogedor, profesional
- Call to action al final
- Usa hashtags relevantes (máximo 10)

Genera SOLO el texto del post, sin títulos ni explicaciones adicionales.
"""

FACEBOOK_POST_PROMPT = """
Eres un experto en marketing espiritual y wellness. Crea un post informativo para Facebook para Sacred Rebirth.

Información del negocio:
- Nombre: Sacred Rebirth
- Ubicación: Valle de Bravo, Mexico
- Servicios: Retiros de Ayahuasca, Kambo, Rapé, Qigong
- Próximo retiro: 11 de Enero, 2026
- Website: https://sacred-rebirth.com

Tema del post: {topic}

Requisitos:
- Texto en español
- 300-500 palabras
- Tono educativo y acogedor
- Incluye call to action
- Usa emojis moderadamente
- Hashtags al final (5-8)

Genera SOLO el texto del post.
"""

EMAIL_CAMPAIGN_PROMPT = """
Eres un experto en email marketing para wellness y retiros espirituales.

Crea un email promocional para Sacred Rebirth sobre: {topic}

Información del negocio:
- Retiros de transformación espiritual
- Ubicación: Valle de Bravo, Mexico
- Próximo retiro: 11 de Enero, 2026
- Website: https://sacred-rebirth.com
- Email: rebirthsecred@gmail.com
- WhatsApp: +52 722 512 3413

Estructura del email:
1. Subject line atractivo (máximo 50 caracteres)
2. Saludo personalizado
3. Contenido principal (200-300 palabras)
4. Call to action claro
5. Firma profesional

Requisitos:
- Tono: Cálido, profesional, inspirador
- Idioma: Español
- Incluye link a la página de citas
- Menciona garantía de transformación

Formato de salida:
---SUBJECT---
[subject line aquí]

---BODY---
[cuerpo del email aquí]
"""

CONTENT_TOPICS = [
    "Beneficios de la ceremonia de Ayahuasca",
    "Preparación para tu primer retiro espiritual",
    "Testimonios de transformación personal",
    "La medicina sagrada del Kambo",
    "Qigong: equilibrio de energía vital",
    "Valle de Bravo: el lugar perfecto para tu retiro",
    "Rapé: ceremonia de limpieza ancestral",
    "Proceso de integración post-retiro",
    "Sanación emocional y espiritual",
    "Próximo retiro: lo que debes saber",
    "Preguntas frecuentes sobre Ayahuasca",
    "La importancia del facilitador experimentado",
    "Conexión con la naturaleza en Valle de Bravo",
    "Transformación espiritual: historias reales",
    "Discovery Call gratuita: comienza tu viaje"
]

HASHTAGS_INSTAGRAM = [
    "#Ayahuasca",
    "#RetiroEspiritual",
    "#ValleDeBravo",
    "#SacredRebirth",
    "#Kambo",
    "#Rapé",
    "#Qigong",
    "#TransformacionEspiritual",
    "#MedicinaAncestral",
    "#SanacionEmocional",
    "#Wellness",
    "#EspiritualidadConsciente",
    "#RetirosMexico",
    "#DesperrtarEspiritual",
    "#ConexionInterior"
]

HASHTAGS_FACEBOOK = [
    "#RetiroEspiritual",
    "#Ayahuasca",
    "#ValleDeBravo",
    "#MedicinaAncestral",
    "#SacredRebirth",
    "#TransformacionPersonal",
    "#BienestarEmocional",
    "#RetirosMexico"
]
