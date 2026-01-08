import customtkinter as ctk

class ResultadosPopup(ctk.CTkToplevel):
    def __init__(self, parent, resultados: dict, modo: str = "liquido_a_base"):
        """
        Crea una ventana flotante independiente con los resultados.
        
        Args:
            parent: Ventana padre
            resultados: Diccionario con los resultados del cálculo
            modo: "liquido_a_base" o "base_a_liquido"
        """
        super().__init__(parent)
        
        self.modo = modo
        self.title("Resultado del Cálculo")
        self.geometry("450x620")
        
        self._crear_interfaz(resultados)

    def _crear_interfaz(self, resultados):
        # --- Header con color según modo ---
        if self.modo == "base_a_liquido":
            color_header = ("#2980b9", "#1a5276")  # Azul para Base→Líquido
            titulo_header = "CÁLCULO: BASE → LÍQUIDO"
        else:
            color_header = ("#27ae60", "#229954")  # Verde para Líquido→Base
            titulo_header = "CÁLCULO: LÍQUIDO → BASE"
            
        header = ctk.CTkFrame(self, fg_color=color_header, corner_radius=0)
        header.pack(fill='x', pady=(0, 20))
        
        ctk.CTkLabel(
            header, 
            text=titulo_header, 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        ).pack(pady=15)

        # --- Cuerpo Scrollable ---
        self.info_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.info_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        # --- SECCIÓN PRINCIPAL según modo ---
        if self.modo == "base_a_liquido":
            # Primero el BASE (dato de entrada)
            self._crear_fila("Sueldo Base (entrada):", resultados['sueldo_base'], es_entrada=True)
            self._crear_separador()
            # Luego el LÍQUIDO (resultado principal)
            self._crear_fila("SUELDO LÍQUIDO:", resultados['sueldo_liquido'], es_total=True, es_principal=True)
        else:
            # Primero el LÍQUIDO objetivo
            self._crear_fila("Líquido Objetivo (entrada):", resultados.get('sueldo_liquido', 0) - resultados.get('diferencia', 0), es_entrada=True)
            self._crear_separador()
            # Luego el BASE (resultado principal)
            self._crear_fila("SUELDO BASE:", resultados['sueldo_base'], es_total=True, es_principal=True)
        
        self._crear_separador()
        
        # --- DETALLE DE HABERES ---
        self._crear_fila("Gratificación:", resultados['gratificacion'])
        
        if resultados.get('bonos_imponibles', 0) > 0:
            self._crear_fila("Bonos Imponibles:", resultados['bonos_imponibles'])
            
        self._crear_fila("Total Haberes Imponibles:", resultados['imponible'], es_total=True)
        
        self._crear_fila("Movilización:", resultados.get('movilizacion', 0))
        
        if resultados.get('bonos_no_imponibles', 0) > 0:
            self._crear_fila("Bonos No Imponibles:", resultados['bonos_no_imponibles'])

        self._crear_fila("Total Haberes:", resultados['total_haberes'], es_total=True)
        
        self._crear_separador()
        
        # --- DETALLE DE DESCUENTOS ---
        self._crear_fila('Cotización Previsional (AFP):', resultados.get('cotizacion_previsional', 0))
        self._crear_fila('Cotización Salud:', resultados.get('cotizacion_salud', 0))
        self._crear_fila("Seguro Cesantía:", resultados.get('cesantia', 0))
        self._crear_fila("Impuesto Único:", resultados['impuesto'])
        self._crear_fila("Total Descuentos:", resultados['total_descuentos'], es_descuento=True)
        
        self._crear_separador()
        
        # # --- RESULTADO FINAL (repetido para claridad) ---
        # if self.modo == "base_a_liquido":
        #     self._crear_fila("SUELDO LÍQUIDO FINAL:", resultados['sueldo_liquido'], es_total=True, es_principal=True)
        # else:
        #     self._crear_fila("SUELDO LÍQUIDO RESULTANTE:", resultados['sueldo_liquido'], es_total=True, es_principal=True)
        #     # Mostrar diferencia si hay redondeo
        #     diferencia = resultados.get('diferencia', 0)
        #     if diferencia != 0:
        #         self._crear_nota_diferencia(diferencia)

        # --- Botón cerrar ---
        ctk.CTkButton(
            self, 
            text="Cerrar Ventana", 
            command=self.destroy, 
            fg_color="gray",
            hover_color="darkgray",
            height=35
        ).pack(pady=10)

    def _crear_fila(self, titulo, valor, es_total=False, es_descuento=False, es_principal=False, es_entrada=False):
        """Helper interno para crear filas de datos"""
        f = ctk.CTkFrame(self.info_frame, fg_color="transparent")
        f.pack(fill='x', pady=2)
        
        # Determinar estilo según tipo
        if es_principal:
            font_size = 16
            font_weight = "bold"
            color_texto = ("#1a5f2a", "#2ecc71")  # Verde destacado
        elif es_entrada:
            font_size = 14
            font_weight = "bold"
            color_texto = ("#7f8c8d", "#95a5a6")  # Gris para entrada
        elif es_total:
            font_size = 14
            font_weight = "bold"
            color_texto = ("#2980b9", "#3498db")  # Azul
        elif es_descuento:
            font_size = 14
            font_weight = "bold"
            color_texto = ("#c0392b", "#e74c3c")  # Rojo
        else:
            font_size = 13
            font_weight = "normal"
            color_texto = ("gray20", "gray80")
            
        ctk.CTkLabel(
            f, 
            text=titulo, 
            font=ctk.CTkFont(size=font_size, weight=font_weight if es_principal else "normal")
        ).pack(side='left')
        
        val_fmt = f"$ {valor:,}".replace(",", ".")
        ctk.CTkLabel(
            f, 
            text=val_fmt, 
            font=ctk.CTkFont(size=font_size, weight=font_weight),
            text_color=color_texto
        ).pack(side='right')

    def _crear_nota_diferencia(self, diferencia: int):
        """Muestra la diferencia respecto al líquido objetivo (solo en modo inverso)"""
        f = ctk.CTkFrame(self.info_frame, fg_color=("#fff3cd", "#3d3520"), corner_radius=8)
        f.pack(fill='x', pady=(10, 5), padx=5)
        
        signo = "+" if diferencia > 0 else ""
        dif_fmt = f"{signo}$ {diferencia:,}".replace(",", ".")
        
        if diferencia > 0:
            texto = f"📈 Diferencia por redondeo: {dif_fmt}"
        else:
            texto = f"📉 Diferencia: {dif_fmt}"
        
        ctk.CTkLabel(
            f,
            text=texto,
            font=ctk.CTkFont(size=11),
            text_color=("#856404", "#ffc107"),
            justify="left"
        ).pack(pady=8, padx=10, anchor='w')

    def _crear_separador(self):
        ctk.CTkFrame(self.info_frame, height=2, fg_color="gray").pack(fill='x', pady=10)
