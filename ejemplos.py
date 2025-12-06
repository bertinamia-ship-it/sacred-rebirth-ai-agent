#!/usr/bin/env python3
"""
Script de ejemplo para demostrar el uso del Marketing Crew
Ejecuta: python ejemplos.py
"""

from src.crew import MarketingCrew, quick_instagram_post, quick_facebook_post, quick_email


def ejemplo_1_post_instagram():
    """Ejemplo 1: Generar un post simple de Instagram"""
    print("\n" + "="*60)
    print("EJEMPLO 1: Generar Post de Instagram")
    print("="*60)
    
    tema = "Beneficios de la ceremonia de Ayahuasca"
    print(f"\nGenerando post sobre: {tema}")
    
    resultado = quick_instagram_post(tema)
    print(f"\n✅ Post generado:\n{resultado}")


def ejemplo_2_post_facebook():
    """Ejemplo 2: Generar un post de Facebook"""
    print("\n" + "="*60)
    print("EJEMPLO 2: Generar Post de Facebook")
    print("="*60)
    
    tema = "Preparación para tu primer retiro espiritual"
    print(f"\nGenerando post sobre: {tema}")
    
    resultado = quick_facebook_post(tema)
    print(f"\n✅ Post generado:\n{resultado}")


def ejemplo_3_email_promocional():
    """Ejemplo 3: Crear email promocional"""
    print("\n" + "="*60)
    print("EJEMPLO 3: Email Promocional")
    print("="*60)
    
    print("\nGenerando email promocional...")
    resultado = quick_email(campaign_type='promotional')
    print(f"\n✅ Email generado:\n{resultado}")


def ejemplo_4_crew_completo():
    """Ejemplo 4: Usar el crew completo para estrategia"""
    print("\n" + "="*60)
    print("EJEMPLO 4: Planificación Estratégica con Crew")
    print("="*60)
    
    print("\nInicializando crew de agentes...")
    crew = MarketingCrew()
    
    print("\nEjecutando planificación estratégica...")
    resultado = crew.run_content_strategy()
    print(f"\n✅ Estrategia creada:\n{resultado}")


def ejemplo_5_crear_contenido():
    """Ejemplo 5: Crear contenido para múltiples plataformas"""
    print("\n" + "="*60)
    print("EJEMPLO 5: Crear Contenido Multicanal")
    print("="*60)
    
    crew = MarketingCrew()
    
    temas = [
        "Transformación espiritual con Ayahuasca",
        "Valle de Bravo: el lugar ideal para tu retiro"
    ]
    
    print(f"\nGenerando contenido para: {temas}")
    resultado = crew.run_content_creation(temas)
    print(f"\n✅ Contenido generado:\n{resultado}")


def ejemplo_6_gestion_leads():
    """Ejemplo 6: Gestionar y nutrir leads"""
    print("\n" + "="*60)
    print("EJEMPLO 6: Gestión de Leads")
    print("="*60)
    
    crew = MarketingCrew()
    
    print("\nNutriendo leads interesados...")
    resultado = crew.run_leads_management('nurture', 'interested')
    print(f"\n✅ Leads nutridos:\n{resultado}")


def menu_interactivo():
    """Menú para seleccionar ejemplos"""
    while True:
        print("\n" + "="*60)
        print("🎯 EJEMPLOS DE USO - Sacred Rebirth AI Agent")
        print("="*60)
        print("\n1. 📸 Generar Post de Instagram")
        print("2. 📘 Generar Post de Facebook")
        print("3. 📧 Crear Email Promocional")
        print("4. 🎯 Planificación Estratégica")
        print("5. ✍️  Crear Contenido Multicanal")
        print("6. 👥 Gestión de Leads")
        print("7. 🚀 Ver Todos los Ejemplos")
        print("0. ❌ Salir")
        
        opcion = input("\n👉 Selecciona un ejemplo (0-7): ").strip()
        
        if opcion == '0':
            print("\n👋 ¡Hasta luego!")
            break
        elif opcion == '1':
            ejemplo_1_post_instagram()
        elif opcion == '2':
            ejemplo_2_post_facebook()
        elif opcion == '3':
            ejemplo_3_email_promocional()
        elif opcion == '4':
            ejemplo_4_crew_completo()
        elif opcion == '5':
            ejemplo_5_crear_contenido()
        elif opcion == '6':
            ejemplo_6_gestion_leads()
        elif opcion == '7':
            print("\n🚀 Ejecutando todos los ejemplos...\n")
            ejemplo_1_post_instagram()
            input("\n⏸️  Presiona Enter para continuar...")
            ejemplo_2_post_facebook()
            input("\n⏸️  Presiona Enter para continuar...")
            ejemplo_3_email_promocional()
            input("\n⏸️  Presiona Enter para continuar...")
            # Los ejemplos 4-6 son más pesados, se omiten en "todos"
            print("\n✅ Ejemplos básicos completados!")
        else:
            print("❌ Opción no válida")
        
        if opcion != '0':
            input("\n⏸️  Presiona Enter para volver al menú...")


if __name__ == '__main__':
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║            🌟 EJEMPLOS DE USO - MARKETING CREW 🌟        ║
    ║                                                           ║
    ║          Scripts de demostración para aprender           ║
    ║             cómo usar el crew de agentes IA              ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    print("\n📝 IMPORTANTE:")
    print("- Asegúrate de tener configurado tu OPENAI_API_KEY en .env")
    print("- Algunos ejemplos pueden tardar 1-2 minutos")
    print("- Los resultados se guardan en data/generated/")
    
    menu_interactivo()
