import re


user_string = " I need to find this \"strid \" "
results = re.search(r'"(.*?)"', user_string)

results = results.group()

print(results.group())