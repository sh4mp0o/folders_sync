import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from sync import DirectorySynchronizer


class DirectorySyncApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Настройка окна
        self.title("Синхронизация каталогов")
        self.geometry("600x400")
        self.resizable(False, False)
        ctk.set_appearance_mode("System")  # Поддержка темной и светлой тем
        ctk.set_default_color_theme("blue")  # Синяя цветовая тема

        # Элементы интерфейса
        self.source = None
        self.target = None
        self.synchronizer = DirectorySynchronizer()

        self.create_widgets()

    def create_widgets(self):
        # Заголовок
        self.title_label = ctk.CTkLabel(self, text="Синхронизация каталогов", font=("Arial", 20, "bold"))
        self.title_label.pack(pady=20)

        # Выбор каталога источника
        self.source_btn = ctk.CTkButton(self, text="Выбрать источник", command=self.select_source)
        self.source_btn.pack(pady=10)

        self.source_label = ctk.CTkLabel(self, text="Источник: не выбран", wraplength=500)
        self.source_label.pack(pady=5)

        # Выбор каталога приемника
        self.target_btn = ctk.CTkButton(self, text="Выбрать приемник", command=self.select_target)
        self.target_btn.pack(pady=10)

        self.target_label = ctk.CTkLabel(self, text="Приемник: не выбран", wraplength=500)
        self.target_label.pack(pady=5)

        # Кнопка синхронизации
        self.sync_btn = ctk.CTkButton(self, text="Синхронизировать", command=self.sync_directories)
        self.sync_btn.pack(pady=20)

        # Выход
        self.exit_btn = ctk.CTkButton(self, text="Выход", command=self.quit)
        self.exit_btn.pack(pady=10)

    def select_source(self):
        self.source = filedialog.askdirectory()
        if self.source:
            self.source_label.configure(text=f"Источник: {self.source}")
        else:
            self.source_label.configure(text="Источник: не выбран")

    def select_target(self):
        self.target = filedialog.askdirectory()
        if self.target:
            self.target_label.configure(text=f"Приемник: {self.target}")
        else:
            self.target_label.configure(text="Приемник: не выбран")

    def sync_directories(self):
        if not self.source or not self.target:
            messagebox.showerror("Ошибка", "Выберите оба каталога!")
            return

        try:
            self.synchronizer.synchronize(self.source, self.target)
            messagebox.showinfo("Успех", "Синхронизация завершена!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")


if __name__ == "__main__":
    app = DirectorySyncApp()
    app.mainloop()
