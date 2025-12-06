#!/usr/bin/env python3
"""
Sacred Rebirth AI Marketing Agent - Main Entry Point
Sistema de agentes IA para automatización de marketing

Uso:
    python main.py --mode [strategy|content|campaign|daily|email|social|leads|analytics]
    python main.py --help
"""

import argparse
import sys
from src.crew import MarketingCrew, quick_instagram_post, quick_facebook_post, quick_email


def print_banner():
    """Imprime banner de inicio"""
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║         🌟 SACRED REBIRTH AI MARKETING AGENT 🌟          ║
    ║                                                           ║
    ║              Crew de Agentes Inteligentes                ║
    ║           para Automatización de Marketing               ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


def run_strategy_mode():
    """Modo: Planificación estratégica de contenido"""
    print("\n🎯 MODO: Planificación Estratégica")
    crew = MarketingCrew()
    result = crew.run_content_strategy()
    print(f"\n📋 Resultado:\n{result}")
    return result


def run_content_mode(topics=None):
    """Modo: Creación de contenido"""
    print("\n✍️ MODO: Creación de Contenido")
    crew = MarketingCrew()
    
    if topics:
        topics_list = topics.split(',')
        result = crew.run_content_creation(topics_list)
    else:
        result = crew.run_content_creation()
    
    print(f"\n📝 Resultado:\n{result}")
    return result


def run_campaign_mode(goal=None):
    """Modo: Campaña completa multicanal"""
    print("\n🚀 MODO: Campaña Completa")
    crew = MarketingCrew()
    
    campaign_goal = goal or "Promoción del retiro del 11 de Enero, 2026"
    result = crew.run_full_campaign(campaign_goal)
    
    print(f"\n🎯 Resultado de la campaña:\n{result}")
    return result


def run_daily_mode():
    """Modo: Automatización diaria"""
    print("\n⏰ MODO: Automatización Diaria")
    crew = MarketingCrew()
    result = crew.run_daily_automation()
    
    print(f"\n📊 Resumen del día:\n{result}")
    return result


def run_email_mode(campaign_type='promotional'):
    """Modo: Campaña de email"""
    print(f"\n📧 MODO: Email Marketing ({campaign_type})")
    crew = MarketingCrew()
    result = crew.run_email_campaign(campaign_type)
    
    print(f"\n✉️ Resultado:\n{result}")
    return result


def run_social_mode(platform='both', topic=None):
    """Modo: Publicación en redes sociales"""
    print(f"\n📱 MODO: Redes Sociales ({platform})")
    
    if not topic:
        topic = "Transformación espiritual con Sacred Rebirth"
    
    if platform == 'instagram':
        result = quick_instagram_post(topic)
    elif platform == 'facebook':
        result = quick_facebook_post(topic)
    elif platform == 'both':
        print("Generando para Instagram...")
        ig_result = quick_instagram_post(topic)
        print("\nGenerando para Facebook...")
        fb_result = quick_facebook_post(topic)
        result = {'instagram': ig_result, 'facebook': fb_result}
    else:
        print(f"❌ Plataforma no reconocida: {platform}")
        return None
    
    print(f"\n📱 Resultado:\n{result}")
    return result


def run_leads_mode(action='nurture', segment='interested'):
    """Modo: Gestión de leads"""
    print(f"\n👥 MODO: Gestión de Leads ({action} - {segment})")
    crew = MarketingCrew()
    result = crew.run_leads_management(action, segment)
    
    print(f"\n📊 Resultado:\n{result}")
    return result


def run_analytics_mode(metric='engagement'):
    """Modo: Análisis de métricas"""
    print(f"\n📊 MODO: Analytics ({metric})")
    crew = MarketingCrew()
    result = crew.run_analytics(metric)
    
    print(f"\n📈 Resultado:\n{result}")
    return result


def run_interactive_mode():
    """Modo interactivo con menú"""
    while True:
        print("\n" + "="*60)
        print("🎯 MENÚ PRINCIPAL - Sacred Rebirth AI Agent")
        print("="*60)
        print("\n1. 📋 Planificación Estratégica de Contenido")
        print("2. ✍️  Crear Contenido (Instagram/Facebook)")
        print("3. 📧 Campaña de Email Marketing")
        print("4. 📱 Publicar en Redes Sociales")
        print("5. 👥 Gestión de Leads")
        print("6. 📊 Análisis de Métricas")
        print("7. 🚀 Campaña Completa Multicanal")
        print("8. ⏰ Automatización Diaria")
        print("9. 🔧 Herramientas Rápidas")
        print("0. ❌ Salir")
        
        choice = input("\n👉 Selecciona una opción (0-9): ").strip()
        
        if choice == '0':
            print("\n👋 ¡Hasta luego!")
            break
        elif choice == '1':
            run_strategy_mode()
        elif choice == '2':
            topics = input("📝 Temas (separados por coma) o Enter para usar por defecto: ").strip()
            run_content_mode(topics if topics else None)
        elif choice == '3':
            print("\nTipos de campaña: promotional, educational, testimonial, nurture")
            campaign_type = input("Tipo de campaña: ").strip() or 'promotional'
            run_email_mode(campaign_type)
        elif choice == '4':
            platform = input("Plataforma (instagram/facebook/both): ").strip() or 'both'
            topic = input("Tema del post: ").strip()
            run_social_mode(platform, topic if topic else None)
        elif choice == '5':
            action = input("Acción (view/nurture/segment): ").strip() or 'nurture'
            segment = input("Segmento (interested/converted/all): ").strip() or 'interested'
            run_leads_mode(action, segment)
        elif choice == '6':
            metric = input("Métrica (engagement/conversion/reach/all): ").strip() or 'engagement'
            run_analytics_mode(metric)
        elif choice == '7':
            goal = input("Objetivo de la campaña: ").strip()
            run_campaign_mode(goal if goal else None)
        elif choice == '8':
            run_daily_mode()
        elif choice == '9':
            run_quick_tools()
        else:
            print("❌ Opción no válida")
        
        input("\n⏸️  Presiona Enter para continuar...")


def run_quick_tools():
    """Herramientas rápidas"""
    print("\n🔧 HERRAMIENTAS RÁPIDAS")
    print("1. 📸 Post rápido de Instagram")
    print("2. 📘 Post rápido de Facebook")
    print("3. ✉️  Email rápido")
    
    choice = input("\nSelecciona (1-3): ").strip()
    
    if choice == '1':
        topic = input("Tema: ").strip() or "Sacred Rebirth"
        quick_instagram_post(topic)
    elif choice == '2':
        topic = input("Tema: ").strip() or "Sacred Rebirth"
        quick_facebook_post(topic)
    elif choice == '3':
        campaign_type = input("Tipo (promotional/educational/testimonial): ").strip() or 'promotional'
        quick_email(campaign_type)


def main():
    """Función principal"""
    parser = argparse.ArgumentParser(
        description='Sacred Rebirth AI Marketing Agent - Crew de Agentes IA',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python main.py                                    # Modo interactivo
  python main.py --mode strategy                    # Planificación estratégica
  python main.py --mode content --topics "Ayahuasca,Kambo"
  python main.py --mode campaign --goal "Retiro de Enero"
  python main.py --mode email --type promotional
  python main.py --mode social --platform instagram --topic "Sanación"
  python main.py --mode daily                       # Automatización diaria
  python main.py --mode analytics --metric engagement
        """
    )
    
    parser.add_argument(
        '--mode',
        choices=['strategy', 'content', 'campaign', 'daily', 'email', 'social', 'leads', 'analytics', 'interactive'],
        help='Modo de operación'
    )
    
    parser.add_argument('--topics', help='Temas separados por coma (para modo content)')
    parser.add_argument('--goal', help='Objetivo de la campaña (para modo campaign)')
    parser.add_argument('--type', help='Tipo de email: promotional/educational/testimonial/nurture')
    parser.add_argument('--platform', help='Plataforma social: instagram/facebook/both')
    parser.add_argument('--topic', help='Tema del post')
    parser.add_argument('--action', help='Acción para leads: view/nurture/segment')
    parser.add_argument('--segment', help='Segmento de leads: interested/converted/all')
    parser.add_argument('--metric', help='Métrica a analizar: engagement/conversion/reach/all')
    
    args = parser.parse_args()
    
    # Imprimir banner
    print_banner()
    
    # Si no se especifica modo, usar interactivo
    if not args.mode:
        run_interactive_mode()
        return
    
    # Ejecutar según modo
    try:
        if args.mode == 'strategy':
            run_strategy_mode()
        
        elif args.mode == 'content':
            run_content_mode(args.topics)
        
        elif args.mode == 'campaign':
            run_campaign_mode(args.goal)
        
        elif args.mode == 'daily':
            run_daily_mode()
        
        elif args.mode == 'email':
            campaign_type = args.type or 'promotional'
            run_email_mode(campaign_type)
        
        elif args.mode == 'social':
            platform = args.platform or 'both'
            run_social_mode(platform, args.topic)
        
        elif args.mode == 'leads':
            action = args.action or 'nurture'
            segment = args.segment or 'interested'
            run_leads_mode(action, segment)
        
        elif args.mode == 'analytics':
            metric = args.metric or 'engagement'
            run_analytics_mode(metric)
        
        elif args.mode == 'interactive':
            run_interactive_mode()
        
        print("\n✅ Ejecución completada exitosamente")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Operación cancelada por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
