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
	return -q * 1e3 * x * (L**3 - 2*L*x**2 +x**3)/(24 * E * 1e9 * I) ## результат в мм


def main():
	print("=== Расчет прогиба балки под равномерной нагрузкой (UDL) ===")

	# # Ввод параметров от пользователя
	# L = float(input("Введите длину балки L (м): ")) 
	# E = float(input("Введите модуль Юнга E (ГПа): "))
	# I = float(input("Введите момент инерции I (м^4): "))
	# q = float(input("Введите равномерно-распределенную нагрузку q (кН/м): "))
	L = 10
	E = 200
	I = 0.0001
	q = 5

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
	print(f"Максмальный прогиб: {y_max*1e3:.3f} мм (в {x_max:.2f} м)")

	# Построение графика 
	plt.plot(x, y, label="Прогиб балки (мм)")
	plt.scatter(x_max, y_max, color="red", zorder=5)
	plt.annotate(
		f"{y_max_abs*1e3:.2f} мм\nx={x_max:.2f} м",
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

	#plt.show()

if __name__ == "__main__":
	main()
