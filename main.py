#-------------------------------------------------------------------------------
# Name:        main.py
# Purpose:     Esta herramienta sirve para generar mapas de texturas en base a
#              un "Diffuse" brindado por el usuario.
#              La herramienta tiene calidad de imágen estandarizado desde 32px
#              hasta 8192px.
#              También cuenta con controles para manejar cada uno de los mapas.
#
# Author:      Mauricio José Tobares
#
# Created:     15/12/2024
# Copyright:   (c) Mauricio 2024
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import os
import height
import diffuse
import normal
import metallic
import smoothness
import edge
import ao
import composite  # Importar el módulo composite

class TextureGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de Texturas")

        # Variables de configuración
        self.diffuse_image = None
        self.resized_diffuse_image = None
        self.generated_images = {}  # Almacenar los mapas generados
        self.labels_and_buttons = {}  # Almacenar referencias a labels y botones
        self.height_percentage = tk.IntVar(value=50)
        self.normal_intensity = tk.IntVar(value=50)
        self.metallic_intensity = tk.IntVar(value=50)
        self.smoothness_intensity = tk.IntVar(value=50)
        self.edge_intensity = tk.IntVar(value=50)
        self.ao_intensity = tk.IntVar(value=50)
        self.target_resolution = tk.IntVar(value=1024)
        self.selected_res_button = None
        self.light_intensity = tk.DoubleVar(value=1.0)  # Valor inicial del slider de iluminacion

        # Obtener la resolución de la pantalla
        self.ancho_pantalla = self.root.winfo_screenwidth()
        self.alto_pantalla = self.root.winfo_screenheight()

        # establece el tamaño de la ventana
        self.root.geometry(f"{self.ancho_pantalla}x{self.alto_pantalla}")

        # maximiza la ventana
        self.root.state('zoomed')

        # modo ventana/pantalla completa (fullscreen)
        self.root.attributes('-fullscreen', False)

        # tamaño mínimo de la ventana
        self.root.minsize(400, 300)

        # Frame para la barra superior (botones de resolución)
        self.top_bar_frame = tk.Frame(self.root)
        self.top_bar_frame.pack(side="top", fill="x")

        # Botón ver composición (arriba a la derecha, solo visible si existe una imagen cargada)
        self.composite_button = tk.Button(self.top_bar_frame, text="Ver Composición", command=self.open_composite_window)
        self.composite_button.pack(side="right", pady=10)
        self.composite_button.pack_forget()  # Ocultar el botón hasta que se cargue una imagen

        # Botones de resolución
        resolutions = [32, 64, 128, 256, 512, 1024, 2048, 4096, 8192]
        self.resolution_buttons = {}
        for res in resolutions:
            res_button = tk.Button(self.top_bar_frame, text=f"{res}px",
                                  command=lambda r=res: self.set_resolution(r))
            res_button.pack(side="left", padx=5)
            self.resolution_buttons[res] = res_button
        self.set_resolution(self.target_resolution.get())  # Resaltar el valor por defecto, 1024px

        # Notebook para las pestañas de cada mapa
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")

        # Crear las pestañas y sus respectivos frames
        self.tab_frames = {}
        for tab_name in ['diffuse', 'height', 'normal', 'metallic', 'smoothness', 'edge', 'ao']:
            frame = tk.Frame(self.notebook)
            self.notebook.add(frame, text=tab_name.capitalize())
            self.tab_frames[tab_name] = frame

        # Crear las pestañas y sus respectivos frames (por defecto la pestaña de altura permanece bloqueada)
        self.disable_other_tabs()

        # Barras laterales (frames) para todos los mapas (se crea un frame para cada mapa)
        self.sidebar_frames = {}
        for tab_name in ['diffuse', 'height', 'normal', 'metallic', 'smoothness', 'edge', 'ao']:
             sidebar_frame = tk.Frame(self.tab_frames[tab_name], width=int(self.ancho_pantalla * 0.25))  # Ancho dinámico
             sidebar_frame.pack(side="left", fill="y")
             self.sidebar_frames[tab_name] = sidebar_frame

        # Botón cargar/cambiar imagen (ubicado en la barra lateral de la pestaña "diffuse")
        self.load_diffuse_button = tk.Button(self.sidebar_frames['diffuse'], text="Cargar Diffuse", command=self.load_diffuse)
        self.load_diffuse_button.pack(pady=10)

        # Botón Guardar diffuse, solo activo si existe una imagen
        self.save_diffuse_button = None # Inicializamos como None

        # Botón reset para cada mapa
        self.create_reset_button(self.sidebar_frames['height'], 'height')
        self.create_reset_button(self.sidebar_frames['normal'], 'normal')
        self.create_reset_button(self.sidebar_frames['metallic'], 'metallic')
        self.create_reset_button(self.sidebar_frames['smoothness'], 'smoothness')
        self.create_reset_button(self.sidebar_frames['edge'], 'edge')
        self.create_reset_button(self.sidebar_frames['ao'], 'ao')

         # Sliders para mapa Height (barra lateral del mapa height)
        self.height_slider = None
        self.height_minus_button = None
        self.height_plus_button = None
        self.create_slider_control(self.sidebar_frames['height'], "Intensidad de Altura (%)", self.height_percentage, self.height_slider, self.height_minus_button, self.height_plus_button)

        # Sliders para mapa Normal (barra lateral del mapa normal)
        self.normal_slider = None
        self.normal_minus_button = None
        self.normal_plus_button = None
        self.create_slider_control(self.sidebar_frames['normal'], "Intensidad Normal (%)", self.normal_intensity, self.normal_slider, self.normal_minus_button, self.normal_plus_button)

         # Sliders para mapa metallic (barra lateral del mapa metallic)
        self.metallic_slider = None
        self.metallic_minus_button = None
        self.metallic_plus_button = None
        self.create_slider_control(self.sidebar_frames['metallic'], "Intensidad Metallic (%)", self.metallic_intensity, self.metallic_slider, self.metallic_minus_button, self.metallic_plus_button)

        # Sliders para mapa smoothness (barra lateral del mapa smoothness)
        self.smoothness_slider = None
        self.smoothness_minus_button = None
        self.smoothness_plus_button = None
        self.create_slider_control(self.sidebar_frames['smoothness'], "Intensidad Smoothness (%)", self.smoothness_intensity, self.smoothness_slider, self.smoothness_minus_button, self.smoothness_plus_button)

        # Sliders para mapa edge (barra lateral del mapa edge)
        self.edge_slider = None
        self.edge_minus_button = None
        self.edge_plus_button = None
        self.create_slider_control(self.sidebar_frames['edge'], "Intensidad Edge (%)", self.edge_intensity, self.edge_slider, self.edge_minus_button, self.edge_plus_button)

        # Sliders para mapa ao (barra lateral del mapa ao)
        self.ao_slider = None
        self.ao_minus_button = None
        self.ao_plus_button = None
        self.create_slider_control(self.sidebar_frames['ao'], "Intensidad AO (%)", self.ao_intensity, self.ao_slider, self.ao_minus_button, self.ao_plus_button)

        # Control para la intensidad de la luz (en la barra lateral del mapa diffuse)
        self.light_slider_frame = tk.Frame(self.sidebar_frames['diffuse'])
        self.light_slider_frame.pack(pady=5)

        tk.Label(self.light_slider_frame, text="Intensidad de la luz:").pack(side="left")
        self.light_slider = tk.Scale(self.light_slider_frame, from_=0, to=1, orient="horizontal", resolution=0.05, variable=self.light_intensity, command=self.on_slider_change)
        self.light_slider.pack(side="left")

        # Frame para las imágenes de todos los mapas de textura
        self.results_frames = {}
        for tab_name in ['diffuse', 'height', 'normal', 'metallic', 'smoothness', 'edge', 'ao']:
           results_frame = tk.Frame(self.tab_frames[tab_name])
           results_frame.pack(side="left", expand=True, fill="both")
           self.results_frames[tab_name] = results_frame

        # Inicializar los labels de cada mapa
        self.labels_and_buttons = {}
        self.create_image_grid()

    def create_slider_control(self, frame, label_text, slider_var, slider_attribute, minus_button_attribute, plus_button_attribute):
        # Crea un frame para el slider
        slider_frame = tk.Frame(frame)
        slider_frame.pack(pady=5)

        # Botón -
        minus_button_attribute = tk.Button(slider_frame, text="-", width=3, command=lambda: self.adjust_slider(slider_attribute, -10))
        minus_button_attribute.pack(side="left")

        # Slider
        slider_attribute = tk.Scale(slider_frame, from_=0, to=100, orient="horizontal", label=label_text,
                                        variable=slider_var, command=self.on_slider_change)
        slider_attribute.pack(side="left")

        # Botón +
        plus_button_attribute = tk.Button(slider_frame, text="+", width=3, command=lambda: self.adjust_slider(slider_attribute, 10))
        plus_button_attribute.pack(side="left")

    def create_reset_button(self, frame, texture_type):
        # Botón reset especifico
        reset_button = tk.Button(frame, text="RESET", command=lambda type=texture_type: self.reset_sliders(type))
        reset_button.pack(pady=10)


    def create_image_grid(self):
        texture_names = ['diffuse', 'height', 'normal', 'metallic', 'smoothness', 'edge', 'ao']
        for tab_name in texture_names:
           row, col = 0, 0
           for i, name in enumerate(texture_names):
             if col == 2:
               col = 0
               row += 2

             if tab_name == name:

                label = tk.Label(self.results_frames[tab_name])

                # Botón guardar (solo se agrega si no es diffuse)
                if name != "diffuse":
                    save_button = tk.Button(self.sidebar_frames[tab_name], text=f"Guardar {name.capitalize()}",
                                            command=lambda type=name: self.save_image(type))
                    save_button.pack(pady=10)

                label.grid(row=row, column=col, padx=5, pady=5)

                self.labels_and_buttons[name] = (label, None)
                col+=1
                break

    def disable_other_tabs(self):
         for tab_name in  ['height', 'normal', 'metallic', 'smoothness', 'edge', 'ao']:
             self.notebook.tab(self.tab_frames[tab_name], state="disabled")

    def enable_other_tabs(self):
         for tab_name in  ['height', 'normal', 'metallic', 'smoothness', 'edge', 'ao']:
             self.notebook.tab(self.tab_frames[tab_name], state="normal")

    def load_diffuse(self):
        file_path = filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg *.jpeg *.png")])
        if file_path:
            try:
                self.diffuse_image = Image.open(file_path)

                # Redimensionar a la resolución por defecto
                target_res = self.target_resolution.get()
                self.resized_diffuse_image = self.diffuse_image.resize((target_res, target_res), Image.Resampling.LANCZOS) # Redimensionar al cargar

                self.generate_textures()
                self.enable_other_tabs()
                self.load_diffuse_button.config(text="Cambiar Diffuse")
                self.composite_button.pack(side="right", pady=10) # Muestra el botón ver composición

                # Crear botón Guardar Diffuse (si no existe)
                if not self.save_diffuse_button:
                   self.save_diffuse_button = tk.Button(self.sidebar_frames['diffuse'], text="Guardar Diffuse",
                                        command=lambda type='diffuse': self.save_image(type))
                   self.save_diffuse_button.pack(pady=10)
            except Exception as e:
                tk.messagebox.showerror("Error", f"Error al cargar la imagen: {e}")

    def display_image(self, label, image):
        image_resized = image.resize((200, 200)) # Redimensionar para display
        photo = ImageTk.PhotoImage(image_resized)
        label.config(image=photo)
        label.image = photo  # Mantener referencia


    def set_resolution(self, resolution):

        if self.selected_res_button:
           self.selected_res_button.config(relief=tk.RAISED, bg="SystemButtonFace")  # Desactiva el resaltado y vuelve a su color por defecto

        self.target_resolution.set(resolution)
        self.selected_res_button = self.resolution_buttons[resolution]
        self.selected_res_button.config(relief=tk.SUNKEN, bg="lime green") # Resalta el botón con color verde fluo

        if self.resized_diffuse_image:
            self.generate_textures()

    def open_composite_window(self):

        if not self.resized_diffuse_image:
            tk.messagebox.showwarning("Advertencia", "Por favor, carga una imagen Diffuse primero.")
            return

        target_res = self.target_resolution.get()
        # Generar todos los mapas de texturas
        height_value = self.height_percentage.get() / 100.0
        normal_value = self.normal_intensity.get() / 100.0
        metallic_value = self.metallic_intensity.get() / 100.0
        smoothness_value = self.smoothness_intensity.get() / 100.0
        edge_value = self.edge_intensity.get() / 100.0
        ao_value = self.ao_intensity.get() / 100.0


        diffuse_image = diffuse.process_diffuse(self.resized_diffuse_image)
        height_map = height.generate_height_map(self.resized_diffuse_image, height_value)
        normal_map = normal.generate_normal_map(height_map, normal_value)
        metallic_map = metallic.generate_metallic_map(self.resized_diffuse_image, metallic_value)
        smoothness_map = smoothness.generate_smoothness_map(self.resized_diffuse_image, smoothness_value)
        edge_map = edge.generate_edge_map(self.resized_diffuse_image, smoothness_map, edge_value)
        ao_map = ao.generate_ao_map(self.resized_diffuse_image, ao_value)

        # Crear imagen compuesta con la función del módulo
        composite_image = composite.create_composite_image(diffuse_image, height_map, normal_map, metallic_map, smoothness_map, edge_map, ao_map, target_res, float(self.light_intensity.get())) # Pasa la resolución seleccionada y la intensidad de la luz

        if composite_image:
          # Crear la nueva ventana
          composite_window = tk.Toplevel(self.root)
          composite_window.title("Composición de Texturas")

          # Mostrar imagen compuesta
          composite_label = tk.Label(composite_window)
          self.display_image(composite_label, composite_image)

          # Slider de iluminación
          light_slider = tk.Scale(composite_window, from_=0, to=1, orient="horizontal", resolution=0.05, variable=self.light_intensity, command=lambda value, c_label = composite_label, d_image=diffuse_image, h_map = height_map, n_map = normal_map, m_map = metallic_map, s_map = smoothness_map, e_map = edge_map, a_map = ao_map, t_res = target_res : self.update_composite_window(c_label, d_image, h_map, n_map, m_map, s_map, e_map, a_map, t_res, value))
          light_slider.pack(side="bottom", fill="x", padx=20, pady=10)
          composite_label.pack(padx=20, pady=10)

          # Boton de Descarga
          save_composite_button = tk.Button(composite_window, text="Guardar Composición", command=lambda: self.save_composite_image(composite_image))
          save_composite_button.pack(side="bottom", fill="x", padx=20, pady=10)


    def generate_textures(self):
        if not self.resized_diffuse_image:

            return

        # Obtener la resolución objetivo
        target_res = self.target_resolution.get()

        # Generar todos los mapas de texturas
        height_value = self.height_percentage.get() / 100.0
        normal_value = self.normal_intensity.get() / 100.0
        metallic_value = self.metallic_intensity.get() / 100.0
        smoothness_value = self.smoothness_intensity.get() / 100.0
        edge_value = self.edge_intensity.get() / 100.0
        ao_value = self.ao_intensity.get() / 100.0


        self.generated_images['diffuse'] = diffuse.process_diffuse(self.resized_diffuse_image) # No es necesaria, pero se añade por consistencia
        self.generated_images['height'] = height.generate_height_map(self.resized_diffuse_image, height_value)
        self.generated_images['normal'] = normal.generate_normal_map(self.generated_images['height'], normal_value)
        self.generated_images['metallic'] = metallic.generate_metallic_map(self.resized_diffuse_image, metallic_value)
        self.generated_images['smoothness'] = smoothness.generate_smoothness_map(self.resized_diffuse_image, smoothness_value)
        self.generated_images['edge'] = edge.generate_edge_map(self.resized_diffuse_image, self.generated_images['smoothness'], edge_value)
        self.generated_images['ao'] = ao.generate_ao_map(self.resized_diffuse_image, ao_value)

        self.display_results()

    def on_slider_change(self, value):
        if self.resized_diffuse_image:
            self.generate_textures()

    def adjust_slider(self, slider, amount):
        current_value = slider.get()
        new_value = max(0, min(100, current_value + amount))
        slider.set(new_value)
        if self.resized_diffuse_image:
            self.generate_textures()


    def reset_sliders(self, texture_type):
        if texture_type == 'height':
            self.height_percentage.set(50)
        elif texture_type == 'normal':
            self.normal_intensity.set(50)
        elif texture_type == 'metallic':
             self.metallic_intensity.set(50)
        elif texture_type == 'smoothness':
             self.smoothness_intensity.set(50)
        elif texture_type == 'edge':
            self.edge_intensity.set(50)
        elif texture_type == 'ao':
             self.ao_intensity.set(50)

        if self.resized_diffuse_image:
            self.generate_textures()

    def display_results(self):
         for texture_type, texture_image in self.generated_images.items():
            label, _ = self.labels_and_buttons[texture_type]


            # Redimensionar la imagen al máximo disponible manteniendo la proporción

            if texture_image: # Evitar errores en caso de que se trate de una imagen vacía


                width, height = self.results_frames[texture_type].winfo_width(), self.results_frames[texture_type].winfo_height()

                if width > 0 and height > 0 : # Verificar que los valores de width y height no sean 0

                     image_resized = texture_image
                     image_resized.thumbnail((width,height)) # Redimensionar al máximo posible
                     photo = ImageTk.PhotoImage(image_resized)

                     label.config(image=photo)
                     label.image = photo
                else:
                   print(f"Error al redimensionar {texture_type}, width y/o height = 0")

    def update_composite_window(self, label, diffuse_image, height_map, normal_map, metallic_map, smoothness_map, edge_map, ao_map, target_res, light_value):
       composite_image = composite.create_composite_image(diffuse_image, height_map, normal_map, metallic_map, smoothness_map, edge_map, ao_map, target_res, float(light_value))  # Pasa la resolución seleccionada y la intensidad de la luz

       if composite_image:
           self.display_image(label, composite_image)

    def save_composite_image(self, composite_image):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("Imágenes PNG", "*.png")])
        if file_path:
           try:
               composite_image.save(file_path)
               tk.messagebox.showinfo("Éxito", "Imagen compuesta guardada exitosamente.")
           except Exception as e:
               tk.messagebox.showerror("Error", f"Error al guardar la imagen compuesta: {e}")


    def save_image(self, texture_type):

       if texture_type in self.generated_images:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("Imágenes PNG", "*.png")])
            if file_path:
                try:
                   self.generated_images[texture_type].save(file_path)
                   tk.messagebox.showinfo("Éxito", f"Imagen {texture_type.capitalize()} guardada exitosamente.")
                except Exception as e:
                   tk.messagebox.showerror("Error", f"Error al guardar la imagen {texture_type.capitalize()}: {e}")
       else:
            tk.messagebox.showerror("Error", f"Imagen no encontrada: {texture_type.capitalize()}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TextureGeneratorApp(root)
    root.mainloop()
