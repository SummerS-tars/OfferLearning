# Python 循环穷举与遍历常用写法速查

适用于列表、元组、字符串、字典、集合、文件、迭代器等可迭代对象；涵盖基础写法、带索引、同时遍历多个序列、局部/部分遍历、推导式、高级 itertools 用法与注意事项。

---

## 1) 基础 for 遍历

- 遍历任意可迭代对象（元素只读，不改变原容器）

```python
for x in iterable:
    ...
```

- 示例：

```python
for ch in "hello":
    print(ch)
```

---

## 2) 带索引：enumerate

- 同时拿到索引和值，推荐替代 `range(len(seq))`
- 可设置起始索引：`enumerate(seq, start=1)`

 
```python
for i, x in enumerate(seq):
    ...

for i, x in enumerate(seq, start=1):
    ...
```

- 修改原列表（确实需要索引时）：

```python
for i, x in enumerate(nums):
    nums[i] = x * 2
```

---

## 3) 按索引遍历：range / len

- 需要“索引运算”或“原地赋值”时可用；否则更推荐 enumerate。

```python
for i in range(len(seq)):
    x = seq[i]
    ...
```

- 自定义起止步长：

```python
for i in range(start, stop, step):
    ...
```

---

## 4) 同时遍历多个序列：zip

- 默认按最短序列对齐。
- Python 3.10+ 可用 `zip(a, b, strict=True)` 强制等长。

 
```python
for a, b in zip(list1, list2):
    ...

# 3.10+
# for a, b in zip(list1, list2, strict=True):
#     ...
```

- 三个或更多：

```python
for a, b, c in zip(xs, ys, zs):
    ...
```

---

## 5) 解包遍历（序列/元组元素）

```python
pairs = [(1, 'a'), (2, 'b')]
for n, ch in pairs:
    ...
```

---

## 6) 反向 / 排序遍历

```python
for x in reversed(seq):
    ...

for x in sorted(seq):
    ...

for x in sorted(seq, key=lambda t: t[1], reverse=True):
    ...
```

---

## 7) 条件过滤遍历

- 常规写法：

```python
for x in seq:
    if cond(x):
        ...
```

- 推导式中过滤（见下一节）：

```python
[x for x in seq if cond(x)]
```

---

## 8) 推导式（列表/集合/字典/生成器）

- 列表推导式：

```python
squares = [x*x for x in nums if x % 2 == 0]
```

- 集合推导式：

```python
unique_lowers = {s.lower() for s in words}
```

- 字典推导式：

```python
index_map = {name: i for i, name in enumerate(names, start=1)}
```

- 生成器表达式（惰性、更省内存）：

```python
gen = (x*x for x in nums)  # 用于 any/all/sum/max/min 等
```

---

## 9) 局部/部分遍历

- 切片（适合序列，创建了副本；大数据注意开销）：

```python
for x in seq[:10]:      # 取前10个
    ...

for x in seq[::2]:     # 间隔取样
    ...
```

- itertools.islice（不复制，适合迭代器/大数据流）：

```python
from itertools import islice

for x in islice(iterable, 0, 10):     # 前10个
    ...

for x in islice(iterable, 100, 200, 2):  # [100, 200) 步长2
    ...
```

---

## 10) 窗口/配对遍历

- Python 3.10+：`itertools.pairwise`

```python
from itertools import pairwise
for a, b in pairwise(seq):
    ...  # 连续配对 (s[i], s[i+1])
```

- 通用滑动窗口（任意窗口大小）：

```python
from itertools import islice
from collections import deque

def sliding_window(iterable, n):
    it = iter(iterable)
    d = deque(islice(it, n), maxlen=n)
    if len(d) == n:
        yield tuple(d)
    for x in it:
        d.append(x)
        yield tuple(d)

for win in sliding_window(seq, 3):
    ...  # (s[i], s[i+1], s[i+2])
```

- 简洁相邻配对（不限版本）：

```python
for a, b in zip(seq, seq[1:]):
    ...
```

---

## 11) 遍历字典

```python
d = {"a": 1, "b": 2}

for k in d:                 # 键
    ...

for k in d.keys():          # 同上，更显式
    ...

for v in d.values():        # 值
    ...

for k, v in d.items():      # 键值对
    ...
```

- 修改时的安全遍历：不要在迭代中直接改结构；先复制视图或构造新字典。

```python
for k in list(d.keys()):
    if need_delete(k):
        del d[k]

# 或用推导式创建新字典
new_d = {k: f(v) for k, v in d.items() if keep(k, v)}
```

---

## 12) 遍历集合（set/frozenset）

- 无序、不保证稳定顺序；需要顺序时可配合 `sorted()`。

```python
for x in s:
    ...

for x in sorted(s):
    ...
```

---

## 13) 遍历文件

- 文本文件逐行：

```python
with open("data.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.rstrip("\n")
        ...
```

- 二进制分块读取（示例）：

```python
def read_chunks(fp, size=8192):
    while chunk := fp.read(size):
        yield chunk

with open("bin.dat", "rb") as f:
    for chunk in read_chunks(f):
        ...
```

---

## 14) for-else、break、continue、pass

```python
for x in seq:
    if bad(x):
        break         # 中断循环，不会执行 else
    if skip(x):
        continue      # 跳过本次
    ...
else:
    # 仅当 for 正常耗尽（非 break）时执行
    print("全部检查通过")
```

---

## 15) 迭代器协议与高级用法

- 迭代器基础：

```python
it = iter(iterable)
val = next(it)                 # 取下一个
val = next(it, default=None)   # 取不到返回默认值
```

- `iter(callable, sentinel)`：反复调用直到遇到“哨兵值”

```python
# 每次读取固定大小，直到返回空字节串
with open("bin.dat", "rb") as f:
    for chunk in iter(lambda: f.read(8192), b""):
        ...
```

- itertools 常用：

```python
from itertools import islice, takewhile, dropwhile, chain, cycle, product, permutations, combinations, groupby
```

---

## 16) 计数/判断聚合：优先用生成器表达式

```python
# 是否存在满足条件的元素
if any(x > 100 for x in nums):
    ...

# 是否全部满足
if all(x >= 0 for x in nums):
    ...

# 计数/求和（避免先构建列表）
count = sum(1 for x in nums if x % 2 == 0)
acc   = sum(f(x) for x in nums)
```

---

## 17) 性能与最佳实践

- 优先使用 `enumerate`、`zip`、生成器表达式，避免不必要的中间列表。
- 成员检测（in）大量调用时，优先把容器改为 `set`/`dict`，复杂度由 O(n) 降为均摊 O(1)。
- 大数据流做“部分遍历”时，用 `itertools.islice`，避免切片复制。
- 遍历时不要原地修改容器结构；需要删除/插入请遍历副本或用推导式创建新容器。
- 需要顺序的集合/字典遍历时，用 `sorted()` 或 `collections.OrderedDict`（3.7+ 字典保持插入顺序，但算法上不要依赖旧版本特性）。

---

## 18) 常见场景小抄

- 带行号打印：

```python
for i, line in enumerate(lines, start=1):
    print(f"{i}: {line}")
```

- 同时遍历并判断长度一致（3.10+）：

```python
for a, b in zip(a_list, b_list, strict=True):
    ...
```

- 相邻差分：

```python
for a, b in zip(nums, nums[1:]):
    diff = b - a
```

- 滑动窗口最大值（示意）：

```python
from collections import deque

window, k = deque(), 3
for i, x in enumerate(nums):
    window.append(x)
    if len(window) > k:
        window.popleft()
    if len(window) == k:
        ans = max(window)
```

- 字典筛选与变换：

```python
filtered = {k: v*2 for k, v in d.items() if v > 0}
```

---

参考版本特性：本文用法基于 Python 3.8+；`zip(..., strict=True)` 与 `itertools.pairwise` 需要 Python 3.10+。
