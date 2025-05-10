import tkinter as tk
from tkinter import StringVar, ttk

class Gui:
    # Atributos de classe
    x_pad = 5
    y_pad = 3
    width_entry = 30
    
    def __init__(self):
        self.window = tk.Tk()
        self.window.wm_title("PYSQL versao 1.0")  

        # Variáveis de controle para os campos de entrada
        self.txtNome = StringVar()
        self.txtSobrenome = StringVar()
        self.txtEmail = StringVar()
        self.txtCPF = StringVar() 
        
        # Rótulos e campos de entrada
        self.lblnome = tk.Label(self.window, text="Nome")
        self.lblsobrenome = tk.Label(self.window, text="Sobrenome")
        self.lblemail = tk.Label(self.window, text="Email")
        self.lblcpf = tk.Label(self.window, text="CPF")
        
        self.entNome = tk.Entry(self.window, textvariable=self.txtNome, width=self.width_entry)
        self.entSobrenome = tk.Entry(self.window, textvariable=self.txtSobrenome, width=self.width_entry)
        self.entEmail = tk.Entry(self.window, textvariable=self.txtEmail, width=self.width_entry)
        self.entCPF = tk.Entry(self.window, textvariable=self.txtCPF, width=self.width_entry)
        
         # Lista de clientes, barra de rolagem e botões
        #self.listClientes = tk.Listbox(self.window, width=100)
        #self.scrollClientes = tk.Scrollbar(self.window)
        self.treeClientes = ttk.Treeview(
        self.window, 
        columns=('ID', 'Nome', 'Sobrenome', 'Email', 'CPF', 'Criação', 'Atualização', 'Ativo'), 
        show='headings'
        )
    
        # Configuração das colunas
        colunas = [
            #col_id, texto, largura
            ('ID', 'ID', 50),
            ('Nome', 'Nome', 150),
            ('Sobrenome', 'Sobrenome', 150),
            ('Email', 'Email', 200),
            ('CPF', 'CPF', 120),
            ('Criação', 'Data Criação', 120),
            ('Atualização', 'Última Atualização', 120),
            ('Ativo', 'Ativo', 60)
        ]
        
        for col_id, texto, largura in colunas:
            self.treeClientes.heading(col_id, text=texto)
            self.treeClientes.column(col_id, width=largura, anchor='center' if col_id in ['ID', 'Ativo'] else 'w')
        
        # Barra de rolagem
        self.scrollClientes = ttk.Scrollbar(self.window, orient="vertical", command=self.treeClientes.yview)
        self.treeClientes.configure(yscrollcommand=self.scrollClientes.set)
        
        self.btnViewAll = tk.Button(self.window, text="Ver todos")
        self.btnBuscar = tk.Button(self.window, text="Buscar")
        self.btnInserir = tk.Button(self.window, text="Inserir")
        self.btnUpdate = tk.Button(self.window, text="Update")
        self.btnDelete = tk.Button(self.window, text="Deletar")
        self.btnLimpar = tk.Button(self.window, text="Limpar")
        #self.btnClose = tk.Button(self.window, text="Fechar")
            
        self.setup_layout()

    def setup_layout(self):
        # Posicionamento dos elementos na interface usando grid
        self.lblnome.grid(row=0, column=0)
        self.lblsobrenome.grid(row=1, column=0)
        self.lblemail.grid(row=2, column=0)
        self.lblcpf.grid(row=3, column=0)
        self.entNome.grid(row=0, column=1, padx=50, pady=50)
        self.entSobrenome.grid(row=1, column=1)
        self.entEmail.grid(row=2, column=1)
        self.entCPF.grid(row=3, column=1)
        #self.listClientes.grid(row=0, column=2, rowspan=10)
        self.treeClientes.grid(row=0, column=2, rowspan=10, sticky='nsew')
        self.scrollClientes.grid(row=0, column=6, rowspan=10, sticky='ns')
        self.scrollClientes.grid(row=0, column=6, rowspan=10)
        self.btnViewAll.grid(row=4, column=0, columnspan=2)
        self.btnBuscar.grid(row=5, column=0, columnspan=2)
        self.btnInserir.grid(row=6, column=0, columnspan=2)
        self.btnUpdate.grid(row=7, column=0, columnspan=2) 
        self.btnDelete.grid(row=8, column=0, columnspan=2) 
        self.btnLimpar.grid(row=9, column=0, columnspan=2)
        #self.btnClose.grid(row=9, column=0, columnspan=2) 
        
        #self.listClientes.configure(yscrollcommand=self.scrollClientes.set)
        #self.scrollClientes.configure(command=self.listClientes.yview)
        
        # Configura o grid para expandir
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(2, weight=1)
        
        for child in self.window.winfo_children():
            widget_class = child.__class__.__name__
            if widget_class == "Button":
                child.grid_configure(sticky='WE', padx=self.x_pad, pady=self.y_pad)
            elif widget_class == "Listbox":
                child.grid_configure(padx=0, pady=0, sticky='NS')
            elif widget_class == "Scrollbar":
                child.grid_configure(padx=0, pady=0, sticky='NS')
            else:
                child.grid_configure(padx=self.x_pad, pady=self.y_pad, sticky='NS')
    
    def run(self):
        # Inicia o loop principal da interface gráfica
        self.window.mainloop()

# Inicialização da interface gráfica
if __name__ == "__main__":
    app = Gui()
    app.run()