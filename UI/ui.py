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
        
        self.formato_chile_sueldo_callback: Optional[Callable] = None
        self.calculo_isapre_callback: Optional[Callable] = None
        self.calcular_callback = None
        self.cambio_afp_callback: Optional[Callable] = None
        
        self.lista_bonos = []
        
        self.sueldo_liquido_var = ctk.StringVar()
        self.afp_seleccionada_var = ctk.StringVar(value="Uno")
        self.tasa_afp_actual_var = ctk.StringVar(value="10.49%")
        self.tipo_salud_var = ctk.StringVar(value="fonasa")
        self.valor_isapre_uf_var = ctk.StringVar(value="")
        self.movilizacion_var = ctk.StringVar(value="40.000") 
        
        self._configuracion_ventana()
        self._crear_interfaz()
        
    def _configuracion_ventana(self):
        self.root.title("Calculadora de Sueldos Bases")
        self.root.geometry("700x750")
        
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
        
        # 1. Entradas Principales
        self.crear_seccion_entradas(scroll_frame)
        
        # 2. Componente de Bonos (CORREGIDO)
        self.bonos_component = BonosFrame(scroll_frame, self.lista_bonos, self._proxy_formato)
        self.bonos_component.pack(fill='x', pady=(0, 15))
        
        # 3. Botón Calcular
        self._crear_boton_calcular(scroll_frame)

    def _crear_header(self):
        header = ctk.CTkFrame(self.root, fg_color=("#3b8ed0", "#1f6aa5"), corner_radius=0)
        header.pack(fill='x', pady=(0, 10))
        
        # Frame interno para organizar título y status
        inner_header = ctk.CTkFrame(header, fg_color="transparent")
        inner_header.pack(pady=10, fill='x', padx=20)
        
        # TÍTULO
        ctk.CTkLabel(inner_header, text="Calculadora de Sueldos Bases",
                     font=ctk.CTkFont(size=24, weight="bold"), text_color="white").pack(side='left')

        # --- INDICADOR DE ESTADO (NUEVO) ---
        # Definir color según estado
        color_status = "#2ecc71" if data.ESTADO_CONEXION == "ONLINE" else "#e67e22" # Verde o Naranja
        
        status_frame = ctk.CTkFrame(inner_header, fg_color=color_status, corner_radius=20)
        status_frame.pack(side='right')
        
        ctk.CTkLabel(status_frame, text=data.MENSAJE_ESTADO, 
                     font=ctk.CTkFont(size=12, weight="bold"), 
                     text_color="white").pack(padx=15, pady=5)
        
    def crear_seccion_entradas(self, parent):
        frame = ctk.CTkFrame(parent, corner_radius=15)
        frame.pack(fill='x', pady=(0, 15))
        
        ctk.CTkLabel(frame, text="Datos Principales", font=ctk.CTkFont(size=18, weight="bold"), anchor="w").pack(pady=(15, 10), padx=20, fill='x')
        
        inputs_container = ctk.CTkFrame(frame, fg_color="transparent")
        inputs_container.pack(fill='x', padx=20, pady=(0, 15))
        
        self._crear_campo_moderno(inputs_container, "Sueldo Líquido Deseado", self.sueldo_liquido_var, "Monto deseado", row=0)
        self._crear_selector_afp(inputs_container, "AFP", row=1)
        self._crear_campo_salud(inputs_container, row=2)
        self._crear_campo_moderno(inputs_container, "Movilización", self.movilizacion_var, "Monto movilización", row=3)

    def _crear_boton_calcular(self, parent):
        ctk.CTkButton(
            parent,
            text="CALCULAR SUELDO BASE",
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color=("#27ae60", "#229954"),
            height=60,
            corner_radius=15,
            cursor="hand2",
            command=self._al_presionar_calcular
        ).pack(pady=10, fill='x')

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
        
        if var == self.sueldo_liquido_var: 
            entry.bind('<KeyRelease>', self._manejo_formato_sueldo)
        elif var == self.movilizacion_var:
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
            self.sueldo_liquido_var.set(self.formato_chile_sueldo_callback(self.sueldo_liquido_var.get()))

    def obtener_valores_formulario(self) -> dict:
        try:
            sueldo = int(self.sueldo_liquido_var.get().replace('.', '').replace(',', '') or 0)
            mov = int(self.movilizacion_var.get().replace('.', '').replace(',', '') or 0)
            salud_uf = 0.0
            if self.tipo_salud_var.get() == 'isapre':
                try: salud_uf = float(self.valor_isapre_uf_var.get().replace(',', '.'))
                except: pass
            
            return {
                "sueldo_liquido": sueldo,
                "movilizacion": mov,
                "afp_nombre": self.afp_seleccionada_var.get(),
                "salud_sistema": self.tipo_salud_var.get(),
                "salud_uf": salud_uf,
                "bonos": self.lista_bonos 
            }
        except: return {}

    def mostrar_resultados_popup(self, res): ResultadosPopup(self.root, res)
    def mostrar_error(self, t, m): messagebox.showerror(t, m)
    def mostrar_advertencia(self, t, m): messagebox.showwarning(t, m)
    def run(self): self.root.mainloop()