
import arithmetic

def main():
    # Примеры использования функций из arithmetic.py
    a, b = 10, 5

    sum_result = arithmetic.add(a, b)
    print(f"Сложение: {a} + {b} = {sum_result}")

    subtract_result = arithmetic.subtract(a, b)
    print(f"Вычитание: {a} - {b} = {subtract_result}")

    multiply_result = arithmetic.multiply(a, b)
    print(f"Умножение: {a} * {b} = {multiply_result}")

    try:
        divide_result = arithmetic.divide(a, b)
        print(f"Деление: {a} / {b} = {divide_result}")
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()
