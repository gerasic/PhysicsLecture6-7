import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PotentialEnergyModel:
    def __init__(self, master):
        self.master = master
        self.master.title("Распределение потенциальной энергии в 2D на примере силы упругости")

        # Параметры по умолчанию
        self.m = 1  # масса
        self.g = 9.81  # гравитация
        self.k = 1  # коэффициент упругости
        self.grid_size = 100  # размер сетки
        self.x_range = np.linspace(-5, 5, self.grid_size)
        self.y_range = np.linspace(-5, 5, self.grid_size)

        # Поля ввода для параметров
        self.create_input_fields()

        # Создание кнопки для построения графика
        self.plot_button = tk.Button(master, text="Построить график", command=self.plot_potential_energy)
        self.plot_button.pack(pady=10)

        # Контейнер для графика
        self.plot_frame = tk.Frame(master)
        self.plot_frame.pack(expand=True, fill=tk.BOTH)

        # Заполнитель для фигуры matplotlib
        self.figure = None
        self.canvas = None

        # Обработчик закрытия окна
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_input_fields(self):
        # Ввод массы
        tk.Label(self.master, text="Масса (m):").pack()
        self.mass_entry = tk.Entry(self.master)
        self.mass_entry.insert(0, str(self.m))
        self.mass_entry.pack()

        # Ввод гравитации
        tk.Label(self.master, text="Гравитация (g):").pack()
        self.gravity_entry = tk.Entry(self.master)
        self.gravity_entry.insert(0, str(self.g))
        self.gravity_entry.pack()

        # Ввод коэффициента упругости
        tk.Label(self.master, text="Коэффициент упругости (k):").pack()
        self.spring_entry = tk.Entry(self.master)
        self.spring_entry.insert(0, str(self.k))
        self.spring_entry.pack()

    def potential_energy(self, x, y):
        # Получение параметров из полей ввода
        try:
            self.m = float(self.mass_entry.get())
            self.g = float(self.gravity_entry.get())
            self.k = float(self.spring_entry.get())
        except ValueError:
            tk.messagebox.showerror("Ошибка ввода", "Пожалуйста, введите корректные числовые значения для всех параметров.")
            return None  # Выход при некорректном вводе

        # Потенциальная энергия гравитации
        U_grav = self.m * self.g * y
        # Потенциальная энергия упругости
        U_elastic = 0.5 * self.k * (x**2 + y**2)
        return U_grav + U_elastic

    def plot_potential_energy(self):
        # Вычисление потенциальной энергии на всей сетке
        X, Y = np.meshgrid(self.x_range, self.y_range)
        U = self.potential_energy(X, Y)

        if U is None:  # Проверка на корректность ввода
            return

        # Создание новой фигуры для графика
        if self.figure is not None:
            self.figure.clear()

        self.figure = plt.figure(figsize=(6, 6))
        plt.contourf(X, Y, U, levels=50, cmap='viridis')
        plt.colorbar(label='Потенциальная энергия U(x, y)')
        plt.title('Распределение потенциальной энергии в 2D')
        plt.xlabel('x')
        plt.ylabel('y')

        # Встраивание графика в окно Tkinter
        if self.canvas is not None:
            self.canvas.get_tk_widget().destroy()

        # Создаем canvas и помещаем его в frame
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    def on_closing(self):
        # Очищаем график и закрываем Tkinter
        if self.canvas is not None:
            self.canvas.get_tk_widget().destroy()
        self.master.quit()
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PotentialEnergyModel(root)
    root.mainloop()
