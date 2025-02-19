import json

# serializer, Parser
# Data format - JSON
# Python

bar = {"name" : "ycjung" , "age" : 20 , "roomnum" : [404, 511]}

# 파일로 전송 -> 문자열(Text) -> JSON
# bar는 메모리에 존재하는 데이터 -> JSON Serializer 
# -> JSON 기반의 Text 
# with open("test.txt", "w") as file_handler:
#     json.dump(bar, file_handler)

# serializing
json_str = json.dumps(bar)

print(type(json_str), json_str)

# parsing -> 예외 발생
rcvd_data =json.loads(json_str)

print(rcvd_data.get('phone')) # parsing 한 이후에 해당하는 key 값이 있는지 확인, 값이 없을 경우 어떤 식으로 처리해아할지 알아야함.
print(rcvd_data.get('name'))

print(type(rcvd_data), rcvd_data)

print(type(rcvd_data['age']), type(rcvd_data['roomnum']),
        type(rcvd_data['name']))

