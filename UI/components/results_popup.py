import customtkinter as ctk

class ResultadosPopup(ctk.CTkToplevel):
    def __init__(self, parent, resultados: dict):
        """
        Crea una ventana flotante independiente con los resultados.
        """
        super().__init__(parent)
        
        # 1. Configuración básica de la ventana
        liquido_fmt = f"{resultados['sueldo_liquido']:,}".replace(",", ".")
        self.title(f"Resultado: $ {liquido_fmt}")
        self.geometry("420x550")
        
        # 2. Construir la interfaz
        self._crear_interfaz(resultados)

    def _crear_interfaz(self, resultados):
        # --- Header ---
        header = ctk.CTkFrame(self, fg_color=("#27ae60", "#229954"), corner_radius=0)
        header.pack(fill='x', pady=(0, 20))
        
        ctk.CTkLabel(
            header, 
            text="RESULTADO CÁLCULO", 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        ).pack(pady=15)

        # --- Cuerpo Scrollable ---
        self.info_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.info_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        # --- Filas de datos ---
        self._crear_fila("Sueldo Líquido:", resultados['sueldo_liquido'])
        
        self._crear_separador()
        
        self._crear_fila("Sueldo Base:", resultados['sueldo_base'], es_total=True)
        self._crear_fila("Gratificación:", resultados['gratificacion'])
        
        if resultados.get('bonos_imponibles', 0) > 0:
            self._crear_fila("Bonos Imponibles:", resultados['bonos_imponibles'])
            
        self._crear_fila("Haberes Imponible:", resultados['imponible'], es_total=True)
        
        
        self._crear_fila("Movilización:", resultados.get('movilizacion', 0))
        
        if resultados.get('bonos_no_imponibles', 0) > 0:
            self._crear_fila("Bonos No Imponibles:", resultados['bonos_no_imponibles'])

        self._crear_fila("Total Haberes:", resultados['total_haberes'], es_total=True)
        
        self._crear_separador()
        
        # Cálculo visual rápido de AFP+Salud para mostrarlo agrupado (opcional)
        #otros_dctos = resultados.get('total_descuentos', 0) - resultados.get('impuesto', 0) - resultados.get('cesantia', 0)
        #self._crear_fila("AFP + Salud:", otros_dctos) 
        self._crear_fila('Cotización Previsional', resultados.get('cotizacion_previsional', 0))
        self._crear_fila('Cotización Salud', resultados.get('cotizacion_salud', 0))
        self._crear_fila("Seguro Cesantía:", resultados.get('cesantia', 0))
        self._crear_fila("Impuesto Único:", resultados['impuesto'])
        self._crear_fila("Total Descuentos:", resultados['total_descuentos'], es_descuento=True)
        

        ctk.CTkButton(
            self, 
            text="Cerrar Ventana", 
            command=self.destroy, 
            fg_color="gray",
            hover_color="darkgray",
            height=35
        ).pack(pady=10)

    def _crear_fila(self, titulo, valor, es_total=False, es_descuento=False):
        """Helper interno para crear filas"""
        f = ctk.CTkFrame(self.info_frame, fg_color="transparent")
        f.pack(fill='x', pady=2)
        
        font_size = 15 if es_total or es_descuento else 13
        font_weight = "bold" if es_total or es_descuento else "normal"
        if es_total == True:
            color_texto = ("#2ecc71", "#2ecc71")
        elif es_descuento == True:
            color_texto  = ("#e74c3c", "#c0392b")
        else: 
            color_texto = ("black", "white") 
            
        ctk.CTkLabel(f, text=titulo, font=ctk.CTkFont(size=font_size)).pack(side='left')
        
        val_fmt = f"$ {valor:,}".replace(",", ".")
        ctk.CTkLabel(
            f, 
            text=val_fmt, 
            font=ctk.CTkFont(size=font_size, weight=font_weight),
            text_color=color_texto
        ).pack(side='right')

    def _crear_separador(self):
        ctk.CTkFrame(self.info_frame, height=2, fg_color="gray").pack(fill='x', pady=10)