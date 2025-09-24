import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import os

# Proyecto GastoController5000
# Cargamos librerias, tkinter, flet
# Comenzaremos definiendo funciones 

# nombre del archivo donde se guardaran los gastos (en formato CSV)
DATA_FILE = 'expenses.csv' 

# Función que cargara los datos de gastos desde el archivo CSV
def load_expenses(): 
    """Carga los datos de gastos desde el archivo CSV si existe; 
    si no existe, crea una tabla vacía con las columnas necesarias."""

    # Declaramos que vamos a usar una variable global llamada "expenses_df"
    # (esto significa que la variable existirá fuera de la función también)
    global expenses_df 

    #verificamos si el archivo "expenses.csv existe en la carpeta actual"
    if os.path.exists(DATA_FILE):
        # Si el arcicho SÍ existe:
        #   -lo leemos con pandas y lo guardamos en la variable "expenses_df"
        expenses_df = pd.read_csv(DATA_FILE)

        #Aseguramos que la columna "Amount" (monto) contenga números
        #   - pd.to_numeric convierte los valores a números
        #   - errors='coerce' significa: si hay algo que no es número (como texto),
        #       cámbialo a "valor nulo" en vez de fallar
        expenses_df['Amount'] = pd.to_numeric(expenses_df['Amount'], errors='coerce')

    else:
        # Si el archivo no existe: 
        #   - creamos un dataframe vacío (una tabla sin filas)
        #   - pero con las columnas que necesitamos: 'Product', 'Category', 'Amount', 'Date'
        expenses_df = pd.DataFrame(columns=['Product', 'Category', 'Amount', 'Date'])

def save_expenses():
    """Saves expense data to the CSV file."""
    expenses_df.to_csv(DATA_FILE, index=False)

def update_pie_chart():
    """Updates the pie chart with current expense data."""
    global category_expenses

    # Ensure the 'Amount' column is numeric before calculating
    expenses_df['Amount'] = pd.to_numeric(expenses_df['Amount'], errors='coerce')

    # Group by category and sum the amount, dropping rows with NaN in 'Amount'
    category_expenses = expenses_df.dropna(subset=['Amount']).groupby('Category')['Amount'].sum()

    # Clear previous plot
    ax.clear()

    if not category_expenses.empty:
        # Create the pie chart
        ax.pie(category_expenses, labels=category_expenses.index, autopct='%1.1f%%', startangle=140)
        ax.set_title("Expense Distribution by Category")
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    else:
        ax.text(0, 0, "No expense data available", horizontalalignment='center', verticalalignment='center')
        ax.set_title("Expense Distribution by Category")


    # Redraw the canvas
    canvas.draw()


def add_expense():
    """Retrieves and prints the expense details from the input fields."""
    product = product_entry.get()
    category = category_entry.get()
    amount = amount_entry.get()
    date = date_entry.get()

    new_expense = pd.DataFrame([{
        'Product': product,
        'Category': category,
        'Amount': amount, # Keep as string for now, convert to numeric later
        'Date': date
    }])
    global expenses_df
    expenses_df = pd.concat([expenses_df, new_expense], ignore_index=True)
    save_expenses() # Save the DataFrame after adding the expense

    # Update the pie chart
    update_pie_chart()

# Load expenses when the application starts
load_expenses()

# Create the main application window
root = tk.Tk()
root.title("Expense Tracker")

# Create labels and entry widgets
product_label = tk.Label(root, text="Product:")
product_entry = tk.Entry(root)

category_label = tk.Label(root, text="Category:")
category_entry = tk.Entry(root)

amount_label = tk.Label(root, text="Amount:")
amount_entry = tk.Entry(root)

date_label = tk.Label(root, text="Date (YYYY-MM-DD):")
date_entry = tk.Entry(root)

# Create an 'Add Expense' button
add_button = tk.Button(root, text="Add Expense", command=add_expense)

# Arrange widgets using grid layout
product_label.grid(row=0, column=0, padx=5, pady=5)
product_entry.grid(row=0, column=1, padx=5, pady=5)

category_label.grid(row=1, column=0, padx=5, pady=5)
category_entry.grid(row=1, column=1, padx=5, pady=5)

amount_label.grid(row=2, column=0, padx=5, pady=5)
amount_entry.grid(row=2, column=1, padx=5, pady=5)

date_label.grid(row=3, column=0, padx=5, pady=5)
date_entry.grid(row=3, column=1, padx=5, pady=5)

add_button.grid(row=4, column=0, columnspan=2, pady=10)

# Create a Matplotlib figure and Axes
fig, ax = plt.subplots(figsize=(6, 6))

# Create a Tkinter widget to display the Matplotlib figure
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()

# Place the canvas widget in the GUI window
canvas_widget.grid(row=0, column=2, rowspan=5, padx=10, pady=10)

# Initial plot
update_pie_chart()

# Start the main event loop
root.mainloop()