# Zerocoder
**������� �� ����� ���������������� �� Python � ����������� Zerocoder**


**OP06. ������ � �������� random � math. �������� ����������� ������� � �������**
```python
import arithmetic

def main():
    # ������� ������������� ������� �� arithmetic.py
    a, b = 10, 5

    sum_result = arithmetic.add(a, b)
    print(f"��������: {a} + {b} = {sum_result}")

    subtract_result = arithmetic.subtract(a, b)
    print(f"���������: {a} - {b} = {subtract_result}")

    multiply_result = arithmetic.multiply(a, b)
    print(f"���������: {a} * {b} = {multiply_result}")

    try:
        divide_result = arithmetic.divide(a, b)
        print(f"�������: {a} / {b} = {divide_result}")
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()
```

![�������������� ����������](LessonOP06/dz_2.png?raw=true "�������������� ����������")

