from interface import *
from backend.database import Database
from backend.operations import ClientOperations
from tkinter import END, messagebox
import tkinter as tk
from backend.data_quality import DataQuality

app = None
selected = None

def init_db():
    db = Database()
    try:
        db.connect()  # Estabelece a conexão explicitamente
        return ClientOperations(db)
    except Exception as e:
        messagebox.showerror("Erro de Banco de Dados", f"Não foi possível conectar ao banco: {str(e)}")
        print("Estado da conexão:", db.conn)  # Deve mostrar objeto de conexão, não None
        print("Operações disponíveis:", dir(operations.db.conn))  # Deve incluir 'cursor'
        return None
    
operations = init_db()  # Inicializa com conexão ativa

def clean_input_command():
    app.txtNome.set("")
    app.txtSobrenome.set("")
    app.txtEmail.set("")
    app.txtCPF.set("")
    
# Funções para manipulação dos dados e atualização da interface
def view_command():
    try:
        # Limpa a tabela
        for item in app.treeClientes.get_children():
            app.treeClientes.delete(item)
            
        # Preenche com novos dados incluindo todas as colunas
        rows = operations.view()
        for row in rows:
            # Formata os campos booleanos e datas
            ativo = 'Sim' if row[7] else 'Não'
            criacao = row[5].strftime('%d/%m/%Y %H:%M') if row[5] else ''
            atualizacao = row[6].strftime('%d/%m/%Y %H:%M') if row[6] else ''
            
            app.treeClientes.insert('', 'end', values=(
                row[0],  # ID
                row[1],  # Nome
                row[2],  # Sobrenome
                row[3],  # Email
                row[4],  # CPF
                criacao,
                atualizacao,
                ativo
            ))
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao carregar clientes: {str(e)}")
        
def search_command():
    try:
        # Limpa a tabela
        for item in app.treeClientes.get_children():
            app.treeClientes.delete(item)
            
        # Obtém os valores dos campos de pesquisa
        nome = app.txtNome.get().strip()
        sobrenome = app.txtSobrenome.get().strip()
        email = app.txtEmail.get().strip()
        cpf = app.txtCPF.get().strip()
        
        # Verifica se pelo menos um campo foi preenchido
        if not any([nome, sobrenome, email, cpf]):
            messagebox.showwarning("Aviso", "Preencha pelo menos um campo para pesquisar")
            return
            
        rows = operations.search(nome, sobrenome, email, cpf)
        
        # Formata os resultados igual à view_command
        for row in rows:
            ativo = 'Sim' if row[7] else 'Não'
            criacao = row[5].strftime('%d/%m/%Y %H:%M') if row[5] else ''
            atualizacao = row[6].strftime('%d/%m/%Y %H:%M') if row[6] else ''
            
            app.treeClientes.insert('', 'end', values=(
                row[0],  # ID
                row[1],  # Nome
                row[2],  # Sobrenome
                row[3],  # Email
                row[4],  # CPF
                criacao,
                atualizacao,
                ativo
            ))
            
        clean_input_command()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro na busca: {str(e)}")

def insert_command():
    if operations is None:
        messagebox.showerror("Erro", "Banco de dados não conectado")
        return
    
    try:
        if not DataQuality.validate_email(app.txtEmail.get()):
            raise ValueError("E-mail inválido!")
        
        # Primeiro remove formatação do cpf
        cpf_raw = DataQuality.normalize_cpf(app.txtCPF.get()) 
        
        # Depois valida o CPF limpo
        if not DataQuality.validate_cpf(cpf_raw):
            raise ValueError("CPF inválido! Verifique os dígitos.")

        operations.insert(
            DataQuality.normalize_name(app.txtNome.get()),
            DataQuality.normalize_name(app.txtSobrenome.get()),
            app.txtEmail.get(),
            cpf_raw  # Já está limpo e validado
        )
        view_command()
        messagebox.showinfo("Sucesso", "Cliente inserido!")
        clean_input_command()
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def update_command():
    if not selected:
        messagebox.showwarning("Aviso", "Nenhum cliente selecionado")
        return
        
    try:
        operations.update(
            selected[0], 
            app.txtNome.get(), 
            app.txtSobrenome.get(), 
            app.txtEmail.get(), 
            app.txtCPF.get()
        )
        view_command()
        messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!")
        clean_input_command()  # Limpa os campos após atualização
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def delete_command():
    if not selected:
        messagebox.showwarning("Aviso", "Nenhum cliente selecionado")
        return
        
    if not messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este cliente?"):
        return
        
    try:
        operations.delete(selected[0])
        view_command()
        messagebox.showinfo("Sucesso", "Cliente removido com sucesso!")
        clean_input_command()  # Limpa os campos após deleção
    except Exception as e:
        messagebox.showerror("Erro", str(e))
    
def getSelectedRow(event):
    global selected
    selected_item = app.treeClientes.focus()
    if not selected_item:
        return
        
    selected = app.treeClientes.item(selected_item)['values']
    app.entNome.delete(0, END)
    app.entNome.insert(END, selected[1])
    app.entSobrenome.delete(0, END)
    app.entSobrenome.insert(END, selected[2])
    app.entEmail.delete(0, END)
    app.entEmail.insert(END, selected[3])
    app.entCPF.delete(0, END)
    app.entCPF.insert(END, selected[4])
    # Não preenchemos os campos de data/ativo no formulário
    return selected

if __name__=="__main__":
   app = Gui()
   app.treeClientes.bind('<<TreeviewSelect>>', getSelectedRow)
   
    # Configuração dos comandos dos botões na interface
   app.btnViewAll.configure(command=view_command)
   app.btnBuscar.configure(command=search_command)
   app.btnInserir.configure(command=insert_command)
   app.btnUpdate.configure(command=update_command)
   app.btnDelete.configure(command=delete_command)
   app.btnLimpar.configure(command=clean_input_command)
   #app.btnClose.configure(command=app.window.destroy)
   
 
   '''
    # Configura máscara para CPF
    def format_cpf(event=None):
        cpf = app.txtCPF.get().replace(".", "").replace("-", "")
        if len(cpf) > 11:
            cpf = cpf[:11]
        if len(cpf) > 3:
            cpf = f"{cpf[:3]}.{cpf[3:]}"
        if len(cpf) > 7:
            cpf = f"{cpf[:7]}.{cpf[7:]}"
        if len(cpf) > 11:
            cpf = f"{cpf[:11]}-{cpf[11:]}"
        app.txtCPF.set(cpf[:14])
    
    app.entCPF.bind("<KeyRelease>", format_cpf)
   '''
   def format_cpf(event=None):
    # Pega o texto atual e a posição do cursor
    current_pos = app.entCPF.index(tk.INSERT)
    current_text = app.txtCPF.get()
    
    # Remove toda formatação
    raw_cpf = ''.join(filter(str.isdigit, current_text))
    
    # Aplica formatação apenas se tiver tamanho suficiente
    formatted = ''
    if len(raw_cpf) > 0:
        formatted = raw_cpf[:3]
    if len(raw_cpf) > 3:
        formatted += '.' + raw_cpf[3:6]
    if len(raw_cpf) > 6:
        formatted += '.' + raw_cpf[6:9]
    if len(raw_cpf) > 9:
        formatted += '-' + raw_cpf[9:11]
    
    # Mantém máximo de 14 caracteres (com formatação)
    formatted = formatted[:14]
    
    # Atualiza o campo apenas se houve mudança
    if formatted != current_text:
        app.txtCPF.set(formatted)
        
        # Tenta reposicionar o cursor de forma inteligente
        try:
            if current_pos <= 3:
                new_pos = current_pos
            elif current_pos <= 7:
                new_pos = current_pos + 1
            elif current_pos <= 11:
                new_pos = current_pos + 2
            else:
                new_pos = current_pos + 3
                
            app.entCPF.icursor(min(new_pos, len(formatted)))
        except:
            app.entCPF.icursor(tk.END)

    # Vincula ao evento KeyRelease
   app.entCPF.bind("<KeyRelease>", format_cpf)

   app.run()