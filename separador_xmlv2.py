# Importações necessárias
import os
import shutil
import json
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog, ttk, messagebox, scrolledtext
import threading
import re
import sys # <--- Adicionado para o executável

# ==============================================================================
# Bloco de código para garantir que o executável encontre o arquivo de mapeamentos
# ==============================================================================
if getattr(sys, 'frozen', False):
    # Se estiver rodando como um executável (.exe)
    application_path = os.path.dirname(sys.executable)
else:
    # Se estiver rodando como um script .py normal
    application_path = os.path.dirname(os.path.abspath(__file__))

MAPPINGS_FILE = os.path.join(application_path, 'mapeamentos.json')
# ==============================================================================

class XmlSorterApp:
    # (O restante do código permanece exatamente o mesmo da versão anterior)
    # ... cole aqui o resto da classe XmlSorterApp ...
    def __init__(self, root):
        self.root = root
        self.root.title("Organizador de XML por Anexo do Simples Nacional v2.1")
        self.root.geometry("700x650")

        self.cnae_map = {}
        self.municipio_map = {}

        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        folder_frame = ttk.LabelFrame(main_frame, text="1. Selecione a pasta de origem dos XMLs")
        folder_frame.pack(fill=tk.X, padx=5, pady=5)
        self.folder_path = tk.StringVar()
        folder_entry = ttk.Entry(folder_frame, textvariable=self.folder_path, width=70)
        folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        browse_button = ttk.Button(folder_frame, text="Procurar...", command=self.browse_folder)
        browse_button.pack(side=tk.LEFT, padx=5, pady=5)

        mapping_frame = ttk.LabelFrame(main_frame, text="2. Configure os códigos de atividade e seus anexos")
        mapping_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=10)
        
        notebook = ttk.Notebook(mapping_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=5, padx=5)

        self.cnae_tab = self.create_mapping_tab(notebook, "CNAE (7 dígitos)", self.add_cnae_mapping, self.remove_selected_mapping)
        self.municipio_tab = self.create_mapping_tab(notebook, "Cód. Municipal (9 dígitos)", self.add_municipio_mapping, self.remove_selected_mapping)
        
        notebook.add(self.cnae_tab['frame'], text="CNAE (7 dígitos)")
        notebook.add(self.municipio_tab['frame'], text="Cód. Municipal (9 dígitos)")

        self.start_button = ttk.Button(main_frame, text="3. Iniciar Processamento", command=self.start_processing_thread)
        self.start_button.pack(fill=tk.X, padx=5, pady=10)

        log_frame = ttk.LabelFrame(main_frame, text="Log de Processamento")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.log_area = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, height=10)
        self.log_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.log_area.config(state=tk.DISABLED)

        self.load_mappings()

    def create_mapping_tab(self, parent, title, add_command, remove_command):
        tab_frame = ttk.Frame(parent, padding="10")
        
        input_frame = ttk.Frame(tab_frame)
        input_frame.pack(fill=tk.X)
        
        ttk.Label(input_frame, text="Código:").pack(side=tk.LEFT, padx=(0, 5))
        code_entry = ttk.Entry(input_frame, width=15)
        code_entry.pack(side=tk.LEFT, padx=5)

        ttk.Label(input_frame, text="Anexo:").pack(side=tk.LEFT, padx=(10, 5))
        anexo_options = [
            "Anexo III", "Anexo IV", "Anexo III ou V (Depende do Fator R)"
        ]
        anexo_combobox = ttk.Combobox(input_frame, values=anexo_options, width=30)
        anexo_combobox.pack(side=tk.LEFT, padx=5)

        add_button = ttk.Button(input_frame, text="Adicionar", command=lambda: add_command(code_entry, anexo_combobox))
        add_button.pack(side=tk.LEFT, padx=10)

        list_frame = ttk.Frame(tab_frame, padding=(0, 10, 0, 0))
        list_frame.pack(fill=tk.BOTH, expand=True)

        columns = ('code', 'anexo')
        treeview = ttk.Treeview(list_frame, columns=columns, show='headings')
        treeview.heading('code', text='Código')
        treeview.heading('anexo', text='Anexo')
        treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=treeview.yview)
        treeview.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        remove_button = ttk.Button(tab_frame, text="Remover Selecionado", command=lambda: remove_command(treeview, title))
        remove_button.pack(pady=5)
        
        return {'frame': tab_frame, 'code_entry': code_entry, 'anexo_combobox': anexo_combobox, 'treeview': treeview}

    def log(self, message):
        self.log_area.config(state=tk.NORMAL)
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state=tk.DISABLED)

    def browse_folder(self):
        directory = filedialog.askdirectory()
        if directory:
            self.folder_path.set(directory)
            self.log(f"Pasta de origem selecionada: {directory}")
            
    def add_cnae_mapping(self, code_entry, anexo_combobox):
        code = code_entry.get().strip()
        anexo = anexo_combobox.get().strip()
        if not code.isdigit() or len(code) != 7:
            messagebox.showerror("Erro", "O código CNAE deve ser um número de 7 dígitos.")
            return
        if not anexo:
            messagebox.showerror("Erro", "O campo 'Anexo' não pode estar vazio.")
            return
        self.cnae_map[code] = anexo
        self.update_treeviews()
        self.save_mappings()
        code_entry.delete(0, tk.END)
        anexo_combobox.set('')

    def add_municipio_mapping(self, code_entry, anexo_combobox):
        code = code_entry.get().strip()
        anexo = anexo_combobox.get().strip()
        if not code.isdigit() or len(code) != 9:
            messagebox.showerror("Erro", "O código Municipal deve ser um número de 9 dígitos.")
            return
        if not anexo:
            messagebox.showerror("Erro", "O campo 'Anexo' não pode estar vazio.")
            return
        self.municipio_map[code] = anexo
        self.update_treeviews()
        self.save_mappings()
        code_entry.delete(0, tk.END)
        anexo_combobox.set('')

    def remove_selected_mapping(self, treeview, title):
        selected_items = treeview.selection()
        if not selected_items:
            messagebox.showwarning("Aviso", "Nenhum item selecionado para remover.")
            return
        
        for item_id in selected_items:
            item_data = treeview.item(item_id, 'values')
            code_to_remove = item_data[0]
            if "CNAE" in title:
                if code_to_remove in self.cnae_map: del self.cnae_map[code_to_remove]
            else:
                if code_to_remove in self.municipio_map: del self.municipio_map[code_to_remove]
        
        self.update_treeviews()
        self.save_mappings()

    def update_treeviews(self):
        for i in self.cnae_tab['treeview'].get_children(): self.cnae_tab['treeview'].delete(i)
        for i in self.municipio_tab['treeview'].get_children(): self.municipio_tab['treeview'].delete(i)
        
        for code, anexo in sorted(self.cnae_map.items()):
            self.cnae_tab['treeview'].insert('', tk.END, values=(code, anexo))
        for code, anexo in sorted(self.municipio_map.items()):
            self.municipio_tab['treeview'].insert('', tk.END, values=(code, anexo))

    def save_mappings(self):
        try:
            data_to_save = {'cnae': self.cnae_map, 'municipio': self.municipio_map}
            with open(MAPPINGS_FILE, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, indent=4)
        except Exception as e:
            self.log(f"ERRO: Não foi possível salvar os mapeamentos. {e}")

    def load_mappings(self):
        if os.path.exists(MAPPINGS_FILE):
            try:
                with open(MAPPINGS_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.cnae_map = data.get('cnae', {})
                    self.municipio_map = data.get('municipio', {})
                self.update_treeviews()
                self.log(f"Mapeamentos carregados de '{MAPPINGS_FILE}'.")
            except Exception as e:
                self.log(f"ERRO: Não foi possível carregar os mapeamentos. {e}")
        else:
            self.log("Arquivo de mapeamento não encontrado. Crie novos mapeamentos.")
            
    def find_activity_code(self, root, cnae_map, municipio_map):
        pattern_7_digits = re.compile(r'\b(\d{7})\b')
        pattern_9_digits = re.compile(r'\b(\d{9})\b')
        
        found_code_7, found_code_9 = None, None

        for element in root.iter():
            if element.text:
                if not found_code_7:
                    for code in pattern_7_digits.findall(element.text):
                        if code in cnae_map:
                            found_code_7 = code
                            break
                if not found_code_9:
                     for code in pattern_9_digits.findall(element.text):
                        if code in municipio_map:
                            found_code_9 = code
                            break
            if found_code_7: break
        
        if found_code_7: return (found_code_7, cnae_map[found_code_7])
        if found_code_9: return (found_code_9, municipio_map[found_code_9])
        return (None, None)

    def process_files(self):
        source_dir = self.folder_path.get()
        if not source_dir:
            messagebox.showerror("Erro", "Por favor, selecione uma pasta de origem.")
            self.start_button.config(state=tk.NORMAL)
            return
        if not self.cnae_map and not self.municipio_map:
            messagebox.showwarning("Aviso", "Nenhum mapeamento foi configurado. O programa não saberá como classificar os arquivos.")
            self.start_button.config(state=tk.NORMAL)
            return

        destination_dir = os.path.join(os.path.dirname(source_dir), "xml_organizados")
        os.makedirs(destination_dir, exist_ok=True)
        
        self.log("="*50)
        self.log("Iniciando processamento...")
        
        files_to_process = [f for f in os.listdir(source_dir) if f.lower().endswith('.xml')]
        moved_files = 0

        for filename in files_to_process:
            filepath = os.path.join(source_dir, filename)
            try:
                tree = ET.parse(filepath)
                root = tree.getroot()
                activity_code, anexo = self.find_activity_code(root, self.cnae_map, self.municipio_map)

                if activity_code and anexo:
                    self.log(f"Arquivo: {filename} | Código: {activity_code} -> Movido para '{anexo}'")
                    target_folder = os.path.join(destination_dir, anexo)
                    os.makedirs(target_folder, exist_ok=True) 
                    shutil.move(filepath, os.path.join(target_folder, filename))
                    moved_files += 1
                else:
                    self.log(f"AVISO: Código não mapeado em '{filename}'. O arquivo permanecerá na pasta de origem.")
            
            except Exception as e:
                self.log(f"ERRO ao processar {filename}: {e}. O arquivo permanecerá na pasta de origem.")

        self.log("="*50)
        self.log(f"Processamento concluído!")
        self.log(f"Total de arquivos XML encontrados: {len(files_to_process)}")
        self.log(f"Total de arquivos movidos: {moved_files}")
        messagebox.showinfo("Sucesso", "Processamento concluído!")
        self.start_button.config(state=tk.NORMAL)

    def start_processing_thread(self):
        self.start_button.config(state=tk.DISABLED)
        thread = threading.Thread(target=self.process_files)
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = XmlSorterApp(root)
    root.mainloop()