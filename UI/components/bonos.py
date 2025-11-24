import customtkinter as ctk
from tkinter import messagebox

class BonosFrame(ctk.CTkFrame):
    def __init__(self, parent, lista_bonos_ref, callback_formato=None):
        super().__init__(parent, corner_radius=15)
        self.lista_bonos = lista_bonos_ref
        self.callback_formato = callback_formato 
        # Variables locales
        self.bono_nombre_var = ctk.StringVar()
        self.bono_monto_var = ctk.StringVar(value="")
        self.bono_imponible_var = ctk.BooleanVar(value=True)
        
        self._crear_interfaz()
    
    def _crear_interfaz(self):
        """Crea la sección de bonos"""
        # Título
        ctk.CTkLabel(
            self,
            text="Bonos",
            font=ctk.CTkFont(size=18, weight="bold"),
            anchor="w"
        ).pack(pady=(15, 10), padx=20, fill='x')
        
        # Formulario
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(fill='x', padx=20, pady=(0, 10))
        
        # Grid de inputs
        input_grid = ctk.CTkFrame(form_frame, fg_color="transparent")
        input_grid.pack(fill='x', pady=(0, 10))
        
        # Nombre
        ctk.CTkLabel(input_grid, text="Nombre:", font=ctk.CTkFont(size=12)).grid(
            row=0, column=0, padx=(0, 5), sticky='w')
        ctk.CTkEntry(
            input_grid, 
            textvariable=self.bono_nombre_var,
            width=150,
            height=35,
            placeholder_text="Ej: Producción"
        ).grid(row=0, column=1, padx=5)
        
        # Monto
        ctk.CTkLabel(input_grid, text="Monto:", font=ctk.CTkFont(size=12)).grid(
            row=0, column=2, padx=(15, 5), sticky='w')
        
        self.entry_monto = ctk.CTkEntry(
            input_grid,
            textvariable=self.bono_monto_var,
            width=120,
            height=35,
            placeholder_text="$ 0"
        )
        self.entry_monto.grid(row=0, column=3, padx=5)

        self.entry_monto.bind('<KeyRelease>', self._al_escribir_monto)

        # ctk.CTkEntry(
        #     input_grid,
        #     textvariable=self.bono_monto_var,
        #     width=120,
        #     height=35,
        #     placeholder_text="$ 0"
        # ).grid(row=0, column=3, padx=5)
        
        # Checkbox y botón
        control_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        control_frame.pack(fill='x')
        
        ctk.CTkCheckBox(
            control_frame,
            text="Imponible",
            variable=self.bono_imponible_var,
            font=ctk.CTkFont(size=12)
        ).pack(side='left', padx=(0, 10))
        
        ctk.CTkButton(
            control_frame,
            text="Agregar",
            width=100,
            height=35,
            fg_color=("#27ae60", "#229954"),
            hover_color=("#229954", "#1e8449"),
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self._agregar_bono_interno
        ).pack(side='left')
        
        # Lista de bonos (Textbox)
        ctk.CTkLabel(
            self,
            text="Bonos agregados:",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        ).pack(pady=(10, 5), padx=20, fill='x')
        
        self.bonos_textbox = ctk.CTkTextbox(
            self,
            height=100,
            font=ctk.CTkFont(size=12),
            corner_radius=10
        )
        self.bonos_textbox.pack(fill='x', padx=20, pady=(0, 10))
        self.bonos_textbox.configure(state="disabled") # Inicializar bloqueado
        
        # Botón eliminar
        ctk.CTkButton(
            self,
            text="Eliminar Último Bono",
            fg_color=("#c0392b", "#a93226"),
            hover_color=("#a93226", "#922b21"),
            height=35,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self._eliminar_ultimo_bono
        ).pack(pady=(0, 15), padx=20, fill='x')

    def _al_escribir_monto(self, event):
        """Llama al callback de formato cuando el usuario escribe"""
        if self.callback_formato:
            nuevo_valor = self.callback_formato(self.bono_monto_var.get())
            self.bono_monto_var.set(nuevo_valor)

    def _agregar_bono_interno(self):
        """Valida y agrega un bono a la lista"""
        nombre = self.bono_nombre_var.get().strip()
        monto_str = self.bono_monto_var.get().replace('.', '').replace(',', '')
        es_imponible = self.bono_imponible_var.get()
        
        if not nombre:
            messagebox.showwarning("Datos", "Falta el nombre del bono.")
            return
            
        if not monto_str.isdigit() or int(monto_str) <= 0:
            messagebox.showwarning("Datos", "Monto inválido.")
            return

        monto = int(monto_str)
        
        self.lista_bonos.append({
            "nombre": nombre,
            "monto": monto,
            "imponible": es_imponible
        })
        
        self._actualizar_textbox_bonos()
        
        # Limpiar campos
        self.bono_nombre_var.set("")
        self.bono_monto_var.set("")
        self.bono_imponible_var.set(True)

    def _eliminar_ultimo_bono(self):
        if self.lista_bonos:
            self.lista_bonos.pop()
            self._actualizar_textbox_bonos()

    def _actualizar_textbox_bonos(self):
        self.bonos_textbox.configure(state="normal")
        self.bonos_textbox.delete("1.0", "end")
        
        for i, bono in enumerate(self.lista_bonos, 1):
            tipo = "IMPONIBLE" if bono['imponible'] else "NO IMPONIBLE"
            texto = f"{i}. {bono['nombre']} | ${bono['monto']:,}".replace(",", ".") + f" | {tipo}\n"
            self.bonos_textbox.insert("end", texto)
            
        self.bonos_textbox.configure(state="disabled")