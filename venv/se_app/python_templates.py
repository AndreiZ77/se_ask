СПИСКИ и СЛОВАРИ

# Фильтр пустых строк в списке строк.
list = [x for x in list if x.strip()!='']

# Соединение списка с указанным символом
theList = ["a","b","c"]
joinedString = ",".join(theList)

# Фильтр дублируемых элементов
targetList = list(set(targetList))

# Удаляем пустые значения из списка
targetList = [v for v in targetList if not v.strip()=='']
# или
targetList = filter(lambda x: len(x)>0, targetList)

# Добавление списка к другому списку Python
anotherList.extend(aList)

# Итерация словаря
for k,v in aDict.iteritems():
    print(k + v)

# Есть ли строка в списке
myList = ['one', 'two', 'ten']
if 'one' in myList:
    print('Да')

# Соединяем два словаря
x = {'a': 1, 'b': 2}
y = {'b': 3, 'c': 4}
z = {**x, **y}
print(z)  # {'c': 4, 'a': 1, 'b': 3}
# #
dict1.update(dict2)

ФАЙЛЫ

#Чтения файла по строкам
with open("/path/to/file") as f:
    for line in f:
        print(line)


f = open("/path/tofile", 'w')
for e in aList:
    f.write(e + "\n")
f.close()

СТРОКИ

# Позиционирование строки в тексте
sentence = "this is a test, not testing."
it = re.finditer('\\btest\\b', sentence)
for match in it:
    print("match position: " + str(match.start()) +"-"+ str(match.end()))

# Поиск используя регулярные выражения
m = re.search('\d+-\d+', line) # search 123-123 like strings
if m:
    current = m.group(0)

# форматирование по старому
print('Hello, %s' % name) # Вывод: "Hello, Bob"
#
errno = 50159747054
print('%x' % errno)# Вывод: 'badc0ffee'
#
errno = 50159747054
name = 'Bob'
print('Hey %s, there is a 0x%x error!' % (name, errno)) # 'Hey Bob, there is a 0xbadc0ffee error!'
#
print('Hey %(name)s, there is a 0x%(errno)x error!' % {"name": name, "errno": errno})
# форматирование по новому
print('Hey {name}, there is a 0x{errno:x} error!'.format(name=name, errno=errno))
# форматирование по python 3.6+
name = 'Bob'
print(f'Hello, {name}!')# Вывод: 'Hello, Bob!'
#
a = 5
b = 10
print(f'Five plus ten is {a + b} and not {2 * (a + b)}.') # Вывод: 'Five plus ten is 15 and not 30.'
# шаблонные строки
from string import Template
t = Template('Hey, $name!')
print(t.substitute(name=name))

БАЗЫ ДАННЫХ

db = MySQLdb.connect("localhost", "username", "password", "dbname")
cursor = db.cursor()
sql = "SELECT `name`, `age` FROM `ursers` ORDER BY `age` DESC"
cursor.execute(sql)
results = cursor.fetchall()
for row in results:
    print(row[0] + row[1])
db.close()