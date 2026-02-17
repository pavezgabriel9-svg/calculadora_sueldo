import customtkinter as ctk
from tkinter import messagebox 
from typing import Callable, Optional, List
from .components.results_popup import ResultadosPopup
from .components.bonos import BonosFrame 
from DATA import data
import os
import sys

class ConfigUI:
    
    def __init__(self):
        """Inicializa la ventana principal"""
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        
        # Callbacks
        self.formato_chile_sueldo_callback: Optional[Callable] = None
        self.calculo_isapre_callback: Optional[Callable] = None
        self.calcular_callback = None
        self.cambio_afp_callback: Optional[Callable] = None
        
        self.lista_bonos = []
        
        # Variables del formulario
        self.sueldo_var = ctk.StringVar()  # Variable única para el monto principal
        self.afp_seleccionada_var = ctk.StringVar(value="Uno")
        self.tasa_afp_actual_var = ctk.StringVar(value="10.49%")
        self.tipo_salud_var = ctk.StringVar(value="fonasa")
        self.valor_isapre_uf_var = ctk.StringVar(value="")
        self.movilizacion_var = ctk.StringVar(value="40.000")
        
        # NUEVA: Variable para el modo de cálculo
        self.modo_calculo_var = ctk.StringVar(value="liquido_a_base")

        # Variable para el país seleccionado
        self.pais_seleccionado_var = ctk.StringVar(value="chile")

        self._configuracion_ventana()
        self._crear_interfaz()
        
    def _configuracion_ventana(self):
        self.root.title("Calculadora de Sueldos")
        self.root.geometry("700x800")
        
        try:
            if getattr(sys, 'frozen', False):
                application_path = sys._MEIPASS
            else:
                application_path = os.path.dirname(os.path.abspath(__file__))
                application_path = os.path.join(application_path, '..')

            icon_path = os.path.join(application_path, 'assets', 'logo.ico')
            self.root.iconbitmap(icon_path)
            
        except Exception as e:
            print(f"⚠️ No se pudo cargar el icono: {e}")
            pass

        self.root.eval('tk::PlaceWindow . center')

    def _crear_interfaz(self):
        self._crear_header()
        
        scroll_frame = ctk.CTkScrollableFrame(self.root, fg_color="transparent")
        scroll_frame.pack(fill='both', expand=True, padx=20, pady=(10, 20))
        
        # 0. NUEVO: Selector de Modo
        self._crear_selector_modo(scroll_frame)
        
        # 1. Entradas Principales
        self.crear_seccion_entradas(scroll_frame)
        
        # 2. Componente de Bonos
        self.bonos_component = BonosFrame(scroll_frame, self.lista_bonos, self._proxy_formato)
        self.bonos_component.pack(fill='x', pady=(0, 15))
        
        # 3. Botón Calcular
        self._crear_boton_calcular(scroll_frame)

    def _crear_header(self):
        header = ctk.CTkFrame(self.root, fg_color=("#3b8ed0", "#1f6aa5"), corner_radius=0)
        header.pack(fill='x', pady=(0, 10))

        inner_header = ctk.CTkFrame(header, fg_color="transparent")
        inner_header.pack(pady=10, fill='x', padx=20)

        ctk.CTkLabel(inner_header, text="Calculadora de Sueldos",
                     font=ctk.CTkFont(size=24, weight="bold"), text_color="white").pack(side='left')

        color_status = "#2ecc71" if data.ESTADO_CONEXION == "ONLINE" else "#e67e22"

        status_frame = ctk.CTkFrame(inner_header, fg_color=color_status, corner_radius=20)
        status_frame.pack(side='right')

        ctk.CTkLabel(status_frame, text=data.MENSAJE_ESTADO,
                     font=ctk.CTkFont(size=12, weight="bold"),
                     text_color="white").pack(padx=15, pady=5)

        # Agregar selector de país al header
        self._crear_selector_pais(header)

    def _crear_selector_pais(self, parent):
        """Crea el selector de país en el header"""
        frame_pais = ctk.CTkFrame(parent, fg_color="transparent")
        frame_pais.pack(pady=(10, 5), fill='x', padx=20)

        # Label
        ctk.CTkLabel(
            frame_pais,
            text="🌎 País:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="white"
        ).pack(side='left', padx=(0, 10))

        # Segmented Button para países
        self.pais_segmented = ctk.CTkSegmentedButton(
            frame_pais,
            values=["🇨🇱 Chile", "🇵🇪 Perú", "🇧🇷 Brasil"],
            command=self._on_pais_change,
            font=ctk.CTkFont(size=13, weight="bold"),
            height=40,
            corner_radius=8,
            fg_color=("white", "#1f538d"),
            selected_color=("#FDD835", "#F9A825"),
            selected_hover_color=("#FBC02D", "#F57F17")
        )
        self.pais_segmented.pack(side='left', fill='x', expand=True)
        self.pais_segmented.set("🇨🇱 Chile")  # Default

    def _on_pais_change(self, seleccion: str):
        """Callback ejecutado al cambiar de país"""
        # Mapeo de nombres a códigos
        pais_map = {
            "🇨🇱 Chile": "chile",
            "🇵🇪 Perú": "peru",
            "🇧🇷 Brasil": "brasil"
        }

        codigo_pais = pais_map.get(seleccion, "chile")
        self.pais_seleccionado_var.set(codigo_pais)

        # TODO Fase 2: Cargar configuración específica del país
        # - Actualizar labels (AFP → ONP → INSS según país)
        # - Actualizar opciones de sistemas previsionales
        # - Actualizar sistemas de salud
        # - Recargar valores por defecto

        print(f"🌎 País cambiado a: {codigo_pais.upper()}")

        # Feedback visual al usuario
        from tkinter import messagebox
        messagebox.showinfo(
            "País Actualizado",
            f"Configuración actualizada para:\n\n{seleccion}\n\n"
            f"(Fase 2: Se cargarán las configuraciones específicas)"
        )

    def _crear_selector_modo(self, parent):
        """Crea el toggle para seleccionar el modo de cálculo"""
        frame = ctk.CTkFrame(parent, corner_radius=15)
        frame.pack(fill='x', pady=(0, 15))
        
        ctk.CTkLabel(
            frame, 
            text="Modo de Cálculo", 
            font=ctk.CTkFont(size=18, weight="bold"), 
            anchor="w"
        ).pack(pady=(15, 10), padx=20, fill='x')
        
        # Contenedor para el segmented button
        toggle_container = ctk.CTkFrame(frame, fg_color="transparent")
        toggle_container.pack(fill='x', padx=20, pady=(0, 15))
        
        # SegmentedButton para elegir modo
        self.modo_segmented = ctk.CTkSegmentedButton(
            toggle_container,
            values=["Líquido → Base", "Base → Líquido"],
            command=self._on_modo_change,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=45,
            corner_radius=10
        )
        self.modo_segmented.pack(fill='x')
        self.modo_segmented.set("Líquido → Base")  # Valor por defecto
        
        # Label explicativo
        self.lbl_explicacion = ctk.CTkLabel(
            frame,
            text="💡 Ingresa el sueldo líquido deseado y calcula el sueldo base necesario",
            font=ctk.CTkFont(size=12),
            text_color=("gray40", "gray60"),
            anchor="w"
        )
        self.lbl_explicacion.pack(padx=20, pady=(0, 15), fill='x')

    def _on_modo_change(self, seleccion):
        """Callback cuando cambia el modo de cálculo"""
        if seleccion == "Base → Líquido":
            self.modo_calculo_var.set("base_a_liquido")
            self.lbl_sueldo_principal.configure(text="Sueldo Base Deseado")
            self.entry_sueldo_principal.configure(placeholder_text="Ingresa el sueldo base")
            self.lbl_explicacion.configure(
                text="💡 Ingresa el sueldo base y calcula el sueldo líquido resultante"
            )
            self.btn_calcular.configure(
                text="CALCULAR SUELDO LÍQUIDO",
                fg_color=("#2980b9", "#1a5276")
            )
        else:
            self.modo_calculo_var.set("liquido_a_base")
            self.lbl_sueldo_principal.configure(text="Sueldo Líquido Deseado")
            self.entry_sueldo_principal.configure(placeholder_text="Monto líquido deseado")
            self.lbl_explicacion.configure(
                text="💡 Ingresa el sueldo líquido deseado y calcula el sueldo base necesario"
            )
            self.btn_calcular.configure(
                text="CALCULAR SUELDO BASE",
                fg_color=("#27ae60", "#229954")
            )
        
        # Limpiar el campo al cambiar de modo
        self.sueldo_var.set("")

    def crear_seccion_entradas(self, parent):
        frame = ctk.CTkFrame(parent, corner_radius=15)
        frame.pack(fill='x', pady=(0, 15))
        
        ctk.CTkLabel(frame, text="Datos Principales", font=ctk.CTkFont(size=18, weight="bold"), anchor="w").pack(pady=(15, 10), padx=20, fill='x')
        
        inputs_container = ctk.CTkFrame(frame, fg_color="transparent")
        inputs_container.pack(fill='x', padx=20, pady=(0, 15))
        
        # Campo principal (dinámico según modo)
        self._crear_campo_sueldo_principal(inputs_container, row=0)
        self._crear_selector_afp(inputs_container, "AFP", row=1)
        self._crear_campo_salud(inputs_container, row=2)
        self._crear_campo_moderno(inputs_container, "Movilización", self.movilizacion_var, "Monto movilización", row=3)

    def _crear_campo_sueldo_principal(self, parent, row):
        """Crea el campo principal de sueldo (dinámico según modo)"""
        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.grid(row=row, column=0, pady=8, sticky='ew')
        parent.grid_columnconfigure(0, weight=1)
        
        # Label dinámico (guardamos referencia para modificarlo)
        self.lbl_sueldo_principal = ctk.CTkLabel(
            f, 
            text="Sueldo Líquido Deseado", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.lbl_sueldo_principal.pack(anchor='w')
        
        # Entry (guardamos referencia)
        self.entry_sueldo_principal = ctk.CTkEntry(
            f, 
            textvariable=self.sueldo_var, 
            placeholder_text="Monto líquido deseado", 
            height=40, 
            font=ctk.CTkFont(size=14)
        )
        self.entry_sueldo_principal.pack(fill='x')
        self.entry_sueldo_principal.bind('<KeyRelease>', self._manejo_formato_sueldo)

    def _crear_boton_calcular(self, parent):
        self.btn_calcular = ctk.CTkButton(
            parent,
            text="CALCULAR SUELDO BASE",
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color=("#27ae60", "#229954"),
            height=60,
            corner_radius=15,
            cursor="hand2",
            command=self._al_presionar_calcular
        )
        self.btn_calcular.pack(pady=10, fill='x')

    def _al_presionar_calcular(self):
        if self.calcular_callback:
            self.calcular_callback()

    def _crear_campo_moderno(self, parent, label, var, ph, row):
        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.grid(row=row, column=0, pady=8, sticky='ew')
        parent.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(f, text=label, font=ctk.CTkFont(size=14, weight="bold")).pack(anchor='w')
        entry = ctk.CTkEntry(f, textvariable=var, placeholder_text=ph, height=40, font=ctk.CTkFont(size=14))
        entry.pack(fill='x')
        
        if var == self.movilizacion_var:
            entry.bind('<KeyRelease>', self._manejo_formato_movilizacion)
    
    def _manejo_formato_movilizacion(self, e):
        """Formatea el campo movilización al escribir"""
        if self.formato_chile_sueldo_callback:
            val_formateado = self.formato_chile_sueldo_callback(self.movilizacion_var.get())
            self.movilizacion_var.set(val_formateado)

    def _proxy_formato(self, valor: str) -> str:
        """Método puente que BonosFrame llamará para formatear"""
        if self.formato_chile_sueldo_callback:
            return self.formato_chile_sueldo_callback(valor)
        return valor

    def _crear_selector_afp(self, parent, label, row):
        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.grid(row=row, column=0, pady=8, sticky='ew')
        ctk.CTkLabel(f, text=label, font=ctk.CTkFont(size=14, weight="bold")).pack(anchor='w')
        cf = ctk.CTkFrame(f, fg_color="transparent")
        cf.pack(fill='x')
        self.afp_combo = ctk.CTkOptionMenu(cf, variable=self.afp_seleccionada_var, values=[], command=self._on_afp_change)
        self.afp_combo.pack(side='left', fill='x', expand=True, padx=(0, 10))
        ctk.CTkLabel(cf, textvariable=self.tasa_afp_actual_var).pack(side='left')

    def _on_afp_change(self, seleccion):
        if self.cambio_afp_callback:
            tasa = self.cambio_afp_callback(seleccion)
            self.tasa_afp_actual_var.set(f"{tasa*100:.2f}%")

    def configurar_lista_afps(self, lista):
        self.afp_combo.configure(values=lista)

    def _crear_campo_salud(self, parent, row):
        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.grid(row=row, column=0, pady=8, sticky='ew')
        ctk.CTkLabel(f, text="Sistema de Salud", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor='w')
        rc = ctk.CTkFrame(f, fg_color="transparent")
        rc.pack(fill='x')
        ctk.CTkRadioButton(rc, text="Fonasa", variable=self.tipo_salud_var, value="fonasa", command=self._act_salud).pack(side='left', padx=(0,20))
        ctk.CTkRadioButton(rc, text="Isapre", variable=self.tipo_salud_var, value="isapre", command=self._act_salud).pack(side='left')
        
        self.fi = ctk.CTkFrame(f, fg_color="transparent")
        ctk.CTkLabel(self.fi, text="UF:").pack(side='left', padx=(0,5))
        e = ctk.CTkEntry(self.fi, textvariable=self.valor_isapre_uf_var, width=80)
        e.pack(side='left', padx=(0,5))
        e.bind('<KeyRelease>', self._on_isapre_uf_change)
        self.lbl_isapre_pesos = ctk.CTkLabel(self.fi, text="$ 0", text_color="gray")
        self.lbl_isapre_pesos.pack(side='left')
        self._act_salud()

    def _act_salud(self):
        if self.tipo_salud_var.get() == "isapre":
            self.fi.pack(fill='x', pady=(10,0))
            self._on_isapre_uf_change(None)
        else:
            self.fi.pack_forget()

    def _on_isapre_uf_change(self, e):
        if self.calculo_isapre_callback:
            self.lbl_isapre_pesos.configure(text=f"({self.calculo_isapre_callback(self.valor_isapre_uf_var.get())})")

    def _manejo_formato_sueldo(self, e):
        if self.formato_chile_sueldo_callback:
            self.sueldo_var.set(self.formato_chile_sueldo_callback(self.sueldo_var.get()))

    def obtener_valores_formulario(self) -> dict:
        """Retorna los valores del formulario incluyendo el modo de cálculo"""
        try:
            sueldo = int(self.sueldo_var.get().replace('.', '').replace(',', '') or 0)
            mov = int(self.movilizacion_var.get().replace('.', '').replace(',', '') or 0)
            salud_uf = 0.0
            if self.tipo_salud_var.get() == 'isapre':
                try: 
                    salud_uf = float(self.valor_isapre_uf_var.get().replace(',', '.'))
                except: 
                    pass
            
            modo = self.modo_calculo_var.get()
            
            resultado = {
                "modo": modo,
                "movilizacion": mov,
                "afp_nombre": self.afp_seleccionada_var.get(),
                "salud_sistema": self.tipo_salud_var.get(),
                "salud_uf": salud_uf,
                "bonos": self.lista_bonos 
            }
            
            # Según el modo, el sueldo va en diferente key
            if modo == "base_a_liquido":
                resultado["sueldo_base"] = sueldo
            else:
                resultado["sueldo_liquido"] = sueldo
                
            return resultado
        except: 
            return {}
    
    # UI/ui.py - Agregar nuevos campos:

    def crear_seccion_opciones_patronales(self, parent):
        """Nueva sección para configurar costos patronales"""
        frame = ctk.CTkFrame(parent, corner_radius=15)
        frame.pack(fill='x', pady=(0, 15))
        
        ctk.CTkLabel(
            frame, 
            text="Costos Patronales", 
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(15, 10), padx=20, fill='x')
        
        # Tipo de Contrato
        self.tipo_contrato_var = ctk.StringVar(value="indefinido")
        self._crear_selector_simple(
            frame, 
            "Tipo de Contrato",
            self.tipo_contrato_var,
            ["indefinido", "plazo_fijo", "casa_particular"]
        )
        
        # Nivel de Riesgo
        self.nivel_riesgo_var = ctk.StringVar(value="bajo")
        self._crear_selector_simple(
            frame,
            "Nivel de Riesgo Laboral",
            self.nivel_riesgo_var,
            ["bajo", "medio", "alto"]
        )
        
        # Número de Cargas Familiares
        self.numero_cargas_var = ctk.StringVar(value="0")
        self._crear_campo_moderno(
            frame,
            "Número de Cargas Familiares",
            self.numero_cargas_var,
            "0"
        )

    def _crear_selector_simple(self, parent, label, variable, opciones):
        """Crea un selector desplegable simple"""
        f = ctk.CTkFrame(parent, fg_color="transparent")
        f.pack(fill='x', padx=20, pady=8)
        
        ctk.CTkLabel(
            f, 
            text=label, 
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor='w', pady=(0, 5))
        
        ctk.CTkOptionMenu(
            f,
            variable=variable,
            values=opciones,
            height=35,
            font=ctk.CTkFont(size=13)
        ).pack(fill='x')
    
    def obtener_modo_calculo(self) -> str:
        """Retorna el modo de cálculo actual"""
        return self.modo_calculo_var.get()

    def obtener_pais_seleccionado(self) -> str:
        """Retorna el código del país seleccionado"""
        return self.pais_seleccionado_var.get()

    def mostrar_resultados_popup(self, res, modo="liquido_a_base"): 
        ResultadosPopup(self.root, res, modo)
        
    def mostrar_error(self, t, m): 
        messagebox.showerror(t, m)
        
    def mostrar_advertencia(self, t, m): 
        messagebox.showwarning(t, m)
        
    def run(self): 
        self.root.mainloop()
