import numpy as np
import matplotlib.pyplot as plt

def deflection_udl(x, L, E, I, q):
	"""
	Прогиб y(x) в метрах для шарнирно-опертой балки под равномерной нагрузкой.
	Параметры:
	L - м
	E - ГПа
	I - м^4
	q - кН/м
	Вывод:
	y(x) - мм (отрицательные значения - прогиб вниз)
	"""
	E_SI = E * 1e9 # ГПа → Па
	q_SI = q * 1e3 # кН → Н
	y_m = q_SI * x * (L**3 - 2*L*x**2 + x**3) / (24 * E_SI * I)  # результат прогиба в метрах
	return -y_m *1e3 # результат прогиба в мм, отрицательное значение по вертикали

def deflection_point_load(x, L, E, I, P, a):
    """
    Прогиб y(x) в мм для шарнирно-опёртой балки длиной L под действием сосредоточенной силы P в точке a.
	Параметры:
      L — м
      E — ГПа
      I — м^4
      P — кН (вниз)
      a — м (координата приложения силы от левой опоры)
    Вывод:
      y(x) — мм (отрицательные значения — прогиб вниз)
    """
    E_SI = E * 1e9   # ГПа → Па
    P_SI = P * 1000  # кН → Н
    b = L - a        # Участок справа от приложенной нагрузки Р

    y = np.zeros_like(x, dtype=float) # Создаем пустой массив 'у' размера 'х'

    # Участок слева от нагрузки (0 <= x <= a)
    mask_left = (x <= a) # Массив точек слева от силы
    x_left = x[mask_left]
    y[mask_left] = -P_SI * b * x_left * (L**2 - b**2 - x_left**2) / (6 * E_SI * I * L)

    # Участок справа от нагрузки (a <= x <= L)
    mask_right = (x >= a) # Массив точек справа от силы
    x_right = x[mask_right]
    y[mask_right] = -P_SI * a * (L - x_right) * (L**2 - a**2 - (L - x_right)**2) / (6 * E_SI * I * L)

    return y * 1000  # переводим в мм


def main():
	print("=== Расчет прогиба балки под равномерной нагрузкой (UDL) ===")

	# # Ввод параметров от пользователя
	# L = float(input("Введите длину балки L (м): ")) 
	# E = float(input("Введите модуль Юнга E (ГПа): "))
	# I = float(input("Введите момент инерции I (м^4): "))
	# q = float(input("Введите равномерно-распределенную нагрузку q (кН/м): "))
	# L = 10
	# E = 200
	# I = 0.0001
	# q = 5

	# Сетка точек вдоль балки для построения графика
	x = np.linspace(0, L, 2001)
	y = deflection_udl(x, L, E, I, q) # прогиб в мм

	# Координата и вычисление максимального прогиба (в миллиметрах)
	idx_min = np.argmin(y)
	x_max = x[idx_min]
	y_max = y[idx_min]
	y_max_abs = abs(y_max)


	# Вывод результата
	print("\n===Результат===")
	print(f"Максмальный прогиб: {y_max:.3f} мм (в точке х = {x_max:.2f} м)")

	# Построение графика 
	plt.plot(x, y, label="Прогиб балки (мм)")
	plt.scatter(x_max, y_max, color="red", zorder=5)
	plt.annotate(
		f"{-y_max_abs:.2f} мм\nx={x_max:.2f} м",
		xy = (x_max, y_max),
		xytext=(x_max, y_max*0.7),
		arrowprops=dict(arrowstyle="->", color="red"),
		ha="center", color ="red"
	)
	plt.title("Прогиб шарнирно-опертой балки под равномерной нагрузкой")
	plt.xlabel("Координата х, м")
	plt.ylabel("Прогиб, мм")
	plt.grid(True)
	plt.legend()

	# Сохраняем график в results/
	plt.savefig("results/beam_deflection.png", dpi=150)

	plt.show()

if __name__ == "__main__":
	# main()
	L, E, I, P = 10, 200, 1e-4, 10  # м, ГПа, м^4, кН
	a = L / 2
	x = np.linspace(0, L, 5)  # пять точек для проверки
	y = deflection_point_load(x, L, E, I, P, a)
	print("Прогибы (мм):", y)