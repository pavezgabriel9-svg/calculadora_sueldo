# main.py
from UI.ui import ConfigUI
from SERVICE import services, engine
from DATA import db_loader 

def main():
    db_loader.actualizar_configuracion_desde_db()
    
    app = ConfigUI()
    
    # Configurar callbacks
    app.formato_chile_sueldo_callback = services.formato_chile_sueldo
    app.calculo_isapre_callback = services.calcular_costo_isapre_pesos
    
    def al_cambiar_afp(nombre_afp):
        return services.obtener_tasa_afp(nombre_afp)
    app.cambio_afp_callback = al_cambiar_afp
    
    app.configurar_lista_afps(services.obtener_lista_afps())
    valor_uf, default_plan = services.obtener_defaults_salud()
    app.valor_isapre_uf_var.set(str(default_plan))
    
    tasa_init = services.obtener_tasa_afp("Uno")
    app.tasa_afp_actual_var.set(f"{tasa_init*100:.2f}%")

    def procesar_calculo():
        """Procesa el cálculo según el modo seleccionado"""
        datos = app.obtener_valores_formulario()
        modo = datos.get('modo', 'liquido_a_base')
        
        bonos = datos.get('bonos', [])
        print(f"Modo: {modo}")
        print(f"Datos recibidos: {datos}")
        print(f"Bonos Count: {len(bonos)}")

        try:
            if modo == "base_a_liquido":
                # Modo: Base → Líquido
                sueldo_base = datos.get('sueldo_base', 0)
                
                if sueldo_base <= 0:
                    app.mostrar_advertencia(
                        "Faltan Datos", 
                        "Debes ingresar un sueldo base mayor a $0."
                    )
                    return
                
                resultado = engine.calcular_liquido_desde_base(datos)
                app.mostrar_resultados_popup(resultado, modo="base_a_liquido")
                
            else:
                # Modo: Líquido → Base (original)
                sueldo_liquido = datos.get('sueldo_liquido', 0)
                
                if sueldo_liquido <= 0:
                    app.mostrar_advertencia(
                        "Faltan Datos", 
                        "Debes ingresar un sueldo líquido mayor a $0."
                    )
                    return

                resultado = engine.resolver_sueldo_base(datos)
                app.mostrar_resultados_popup(resultado, modo="liquido_a_base")
            
        except Exception as e:
            print(f"Error detallado: {e}")
            import traceback
            traceback.print_exc()
            app.mostrar_error("Error de Cálculo", f"❌ Ocurrió un error interno:\n{e}")

    app.calcular_callback = procesar_calculo
    
    app.run()

if __name__ == "__main__":
    main()
