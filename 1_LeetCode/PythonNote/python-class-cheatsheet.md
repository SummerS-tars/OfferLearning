# Python 中的 Class（类）使用归纳

> 结构化整理：基础部分 / 实践示例部分 / 延伸部分。

## 一、基础部分

### 1. 类与对象的基本概念

- **类**：一组数据与行为的抽象
- **对象**：类的实例
- **属性**：对象持有的数据
- **方法**：对象的行为（函数）

### 2. 最小可用示例

```python
class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def greet(self) -> str:
        return f"Hi, I am {self.name}"  

p = Person("Alice", 18)
print(p.name)   # Alice
print(p.greet())
```

**关键点**：

- `__init__` 是构造方法
- `self` 指向当前对象

### 3. 类属性 vs 实例属性

```python
class Counter:
    total = 0  # 类属性

    def __init__(self):
        Counter.total += 1
        self.index = Counter.total  # 实例属性

c1 = Counter()
c2 = Counter()
print(Counter.total)  # 2
print(c1.index, c2.index)  # 1 2
```

### 4. 访问控制与命名约定

- `_name`：受保护（约定，不强制）
- `__name`：名称改写（类内可见）

```python
class Demo:
    def __init__(self):
        self._soft = 1
        self.__hard = 2

    def get_hard(self):
        return self.__hard
```

### 5. 实例方法 / 类方法 / 静态方法

```python
class Tool:
    def instance_method(self):
        return "instance"

    @classmethod
    def class_method(cls):
        return cls.__name__

    @staticmethod
    def static_method():
        return "static"
```

**使用场景**：

- 实例方法：访问实例数据
- 类方法：访问类级别数据、备用构造器
- 静态方法：工具函数，和类逻辑相关但不依赖实例

---

## 二、实践示例部分

### 1. 典型刷题模板（数据结构包装）

```python
class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, x: int) -> None:
        self.stack.append(x)
        if not self.min_stack or x <= self.min_stack[-1]:
            self.min_stack.append(x)

    def pop(self) -> None:
        val = self.stack.pop()
        if val == self.min_stack[-1]:
            self.min_stack.pop()

    def get_min(self) -> int:
        return self.min_stack[-1]
```

### 2. 使用 `@dataclass` 简化样板代码

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int

p = Point(1, 2)
print(p)
```

### 3. 自定义字符串表示

```python
class User:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"User(name={self.name!r})"

    def __str__(self):
        return f"{self.name}"
```

---

## 三、延伸部分

### 1. 继承与方法重写

```python
class Animal:
    def speak(self):
        return "..."

class Dog(Animal):
    def speak(self):
        return "woof"
```

### 2. 抽象类（ABC）

```python
from abc import ABC, abstractmethod

class Repository(ABC):
    @abstractmethod
    def get(self, key):
        pass
```

### 3. 魔术方法（常见）

- `__init__`：构造
- `__repr__` / `__str__`：打印
- `__len__`：长度
- `__iter__`：可迭代
- `__eq__`：相等判断

```python
class Bag:
    def __init__(self, items):
        self.items = items

    def __len__(self):
        return len(self.items)

    def __iter__(self):
        return iter(self.items)
```

### 4. 组合优于继承（实践建议）

```python
class Engine:
    def start(self):
        return "start"

class Car:
    def __init__(self, engine: Engine):
        self.engine = engine

    def run(self):
        return self.engine.start()
```

---

如果你希望加入“类与模块、元类、描述符、property 深入”部分，我可以继续扩展。
