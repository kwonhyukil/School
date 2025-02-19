bar = {
#   value 값을 찾기 위해 key 값이 필요!!

#   key : value
"김민규" :12345 , "하루나" : 67890, "김민정" : 98765, "하루나" : 5555
}
print(bar["하루나"])

foo = {
    "name" : "ycjung" , "age" : "24", "phone" : 12345678, "email" : "gur@naver.com"
}
print(bar.items())

for key, value in bar.items():

    print(f"key: {key}, value: {value}")

print(foo)

del foo['name']

print(foo)