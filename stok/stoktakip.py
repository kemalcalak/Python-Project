import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class StockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stok Takip Uygulaması")

        self.db_connection = sqlite3.connect("stock.db")
        self.create_table()

        self.products = {}
        self.load_data_from_db()
        self.create_ui()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT,
            quantity INTEGER,
            min_stock INTEGER
        );
        """
        self.db_connection.execute(query)
        self.db_connection.commit()

    def load_data_from_db(self):
        query = "SELECT * FROM products"
        cursor = self.db_connection.execute(query)
        for row in cursor:
            self.products[row[1]] = {'quantity': row[2], 'min_stock': row[3]}

    def save_data_to_db(self):
        query = "DELETE FROM products"
        self.db_connection.execute(query)
        for product, data in self.products.items():
            query = f"INSERT INTO products (name, quantity, min_stock) VALUES ('{product}', {data['quantity']}, {data['min_stock']})"
            self.db_connection.execute(query)
        self.db_connection.commit()

    def create_ui(self):
        tk.Label(self.root, text="Ürün Adı:").grid(row=0, column=0)
        self.entry_name = tk.Entry(self.root)
        self.entry_name.grid(row=0, column=1)

        tk.Label(self.root, text="Stok Miktarı:").grid(row=1, column=0)
        self.entry_quantity = tk.Entry(self.root)
        self.entry_quantity.grid(row=1, column=1)

        tk.Label(self.root, text="Minimum Stok:").grid(row=2, column=0)
        self.entry_min_stock = tk.Entry(self.root)
        self.entry_min_stock.grid(row=2, column=1)

        self.add_button = tk.Button(self.root, text="Ürün Ekle", command=self.add_product)
        self.add_button.grid(row=3, column=0, columnspan=2)

        self.show_button = tk.Button(self.root, text="Stok Görüntüle", command=self.show_stock)
        self.show_button.grid(row=4, column=0, columnspan=2)

        tk.Label(self.root, text="Ürün Adına Göre Filtrele:").grid(row=5, column=0)
        self.entry_filter = tk.Entry(self.root)
        self.entry_filter.grid(row=5, column=1)
        self.filter_button = tk.Button(self.root, text="Filtrele", command=self.filter_products)
        self.filter_button.grid(row=6, column=0, columnspan=2)

        self.total_stock_label = tk.Label(self.root, text="Toplam Stok:")
        self.total_stock_label.grid(row=7, column=0)
        self.show_total_stock_button = tk.Button(self.root, text="Toplam Stok Görüntüle", command=self.show_total_stock)
        self.show_total_stock_button.grid(row=7, column=1)

        tk.Label(self.root, text="Ürün Sil:").grid(row=8, column=0)
        self.entry_delete = tk.Entry(self.root)
        self.entry_delete.grid(row=8, column=1)
        self.delete_button = tk.Button(self.root, text="Ürünü Sil", command=self.delete_product)
        self.delete_button.grid(row=9, column=0, columnspan=2)

        tk.Label(self.root, text="Stok Azalt:").grid(row=10, column=0)
        self.entry_decrease = tk.Entry(self.root)
        self.entry_decrease.grid(row=10, column=1)
        tk.Label(self.root, text="Eksilme Miktarı:").grid(row=11, column=0)
        self.entry_decrease_amount = tk.Entry(self.root)
        self.entry_decrease_amount.grid(row=11, column=1)
        self.decrease_button = tk.Button(self.root, text="Stok Azalt", command=self.decrease_stock)
        self.decrease_button.grid(row=12, column=0, columnspan=2)

        # Sağ tarafta tablo
        self.tree = ttk.Treeview(self.root, columns=("Ürün", "Stok Miktarı", "Min. Stok"), show="headings")
        self.tree.heading("Ürün", text="Ürün")
        self.tree.heading("Stok Miktarı", text="Stok Miktarı")
        self.tree.heading("Min. Stok", text="Min. Stok")
        self.tree.grid(row=0, column=2, rowspan=13, padx=10)

        self.update_table()


    def add_product(self):
        product_name = self.entry_name.get()
        quantity = int(self.entry_quantity.get())
        min_stock = int(self.entry_min_stock.get())

        if product_name and quantity >= 0 and min_stock >= 0:
            if product_name in self.products:
                self.products[product_name]['quantity'] += quantity
            else:
                self.products[product_name] = {'quantity': quantity, 'min_stock': min_stock}

            messagebox.showinfo("Başarılı", f"{product_name} stoklara eklendi.")
            self.entry_name.delete(0, tk.END)
            self.entry_quantity.delete(0, tk.END)
            self.entry_min_stock.delete(0, tk.END)
            self.update_table()
        else:
            messagebox.showerror("Hata", "Geçersiz giriş!")

    def show_stock(self):
        stock_text = "Stok Durumu:\n"
        for product, data in self.products.items():
            stock_text += f"{product}: {data['quantity']} adet (Min. Stok: {data['min_stock']})\n"

        messagebox.showinfo("Stok Durumu", stock_text)

    def filter_products(self):
        filter_text = self.entry_filter.get()
        filtered_text = "Filtrelenmiş Ürünler:\n"

        for product, data in self.products.items():
            if filter_text.lower() in product.lower():
                filtered_text += f"{product}: {data['quantity']} adet (Min. Stok: {data['min_stock']})\n"

        messagebox.showinfo("Filtrelenmiş Ürünler", filtered_text)

    def show_total_stock(self):
        total_stock = sum(data['quantity'] for data in self.products.values())
        messagebox.showinfo("Toplam Stok", f"Toplam Stok Miktarı: {total_stock}")

    def delete_product(self):
        product_name = self.entry_delete.get()
        if product_name in self.products:
            del self.products[product_name]
            messagebox.showinfo("Başarılı", f"{product_name} stoklardan silindi.")
            self.update_table()
        else:
            messagebox.showerror("Hata", f"{product_name} bulunamadı!")

    def decrease_stock(self):
        product_name = self.entry_decrease.get()
        decrease_amount = int(self.entry_decrease_amount.get())

        if product_name in self.products:
            if self.products[product_name]['quantity'] >= decrease_amount:
                self.products[product_name]['quantity'] -= decrease_amount
                messagebox.showinfo("Başarılı", f"{product_name} stok azaltıldı.")
                self.update_table()
            else:
                messagebox.showerror("Hata", f"{product_name} stokta yeterli miktar yok!")
        else:
            messagebox.showerror("Hata", f"{product_name} bulunamadı!")

    def update_table(self):
        self.tree.delete(*self.tree.get_children())
        for product, data in self.products.items():
            item = self.tree.insert("", "end", values=(product, data['quantity'], data['min_stock']))
            if data['quantity'] < data['min_stock']:
                self.tree.item(item, tags=("low_stock",))
            else:
                self.tree.item(item, tags=("normal_stock",))

        self.tree.tag_configure("low_stock", background="red", foreground="white")
        self.tree.tag_configure("normal_stock", background="white", foreground="black")

    def __del__(self):
        self.save_data_to_db()
        self.db_connection.close()


if __name__ == "__main__":
    root = tk.Tk()
    app = StockApp(root)
    root.mainloop()