# 1. 사용자 입력 오류
# 숫자를 입력받아야 하지만, 문자를 입력할 경우 발생하는 오류
# num = int(input("숫자를 입력하세요: "))
# result = int(num) * 2 # ValueError 발생 가능
# print(f"결과: {result}")

# try:
#     if num == 1:
#         raise ValueError # ValueError 예외 발생시키는 코드
#     else:
#         raise NameError # NameError 예외 발생시키는 코드

# except ValueError: # ValueError 의 예외가 발생할 경우 실행될 코드
#     print("ValueError 예외 발생")
# except NameError: # NameError 의 예외가 발생할 경우 실행될 코드
#     print("NameError 예외 발생")

# print(f"결과: 0")

# try:
#     raise ValueError
# # except ValueError:
# except NameError:
#     print("NameError 예외 발생")

# print(f"결과: 0")
# try:
#     result = int(num) * 2

#     print(f"결과: {result}")

# except ValueError:
#     print("정수를 입력하세요")

# try:
#     print("pos")

#     # print(1/0) # 주석처리 on/off 에 따른 결과 값 확인

#     print("bar")

#     kin() # 주석 처리 on/off 에 따른 결과 값 확인

#     raise IndexError("인덱스 예외 발생")
# except ValueError:
#     print("ValueError 예외 발생")
# except IndexError as e:
#     print(f"예외 발생: {e}")
# except NameError as e:
#     print(f"예외 발생: {e}")
# except ZeroDivisionError:
#     print("ZeroDivisionError 예외 발생")

# print(f"결과: 0")

# try:
#     print("1")
    
#     result = 1/0

#     print("2")

#     print("3")
# except ZeroDivisionError:
#     print("4")

# print("5")

# try:
#     print("1")
    
#     raise IndexError # 주석처리

#     print("2")

#     print("3")
# # 예상치 못한 에러가 발생하였을 때 사용
# # 순서 : 제일 마지막에 위치해야한다.
# except Exception:
#     print("3.1")
# except LookupError:
#     print("3.5")

# print("7")

num = 1

try:
    print("1")

    if num == 1:
        raise KeyboardInterrupt
    
    print("2")

except KeyboardInterrupt:
    print("4")
# 예외가 발생되지 않았을 때 실행
else:
    print("5")
    
finally:
    print("6")

print("7")

# # 2. 파일 오류
# # 존재하지 않는 파일을 열 경우 발생하는 오류
# # FileNotFoundError 발생가능
# file = open("non_existent_file.txt", "r")
# content = file.read()

# # 3 연산 오류
# # 0으로 나누는 경우 발생하는 오류
# x = 10
# y = 0
# result = x / y # ZeroDivisionError 발생 가능

# # 4. 파일 오류
# # 무한 재귀 호출로 인한 RecursionError
# def recursive_function():
#     return recursive_function()

# recursive_function() # RecursionError 발생 가능