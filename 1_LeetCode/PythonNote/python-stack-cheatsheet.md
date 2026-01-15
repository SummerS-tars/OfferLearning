# Python 中的 Stack（栈）使用归纳

> 适合刷题与工程实践的轻量笔记，聚焦常见实现方式与复杂度。

## 1. 栈的核心特性

- 后进先出（LIFO）
- 典型操作：`push`（入栈）、`pop`（出栈）、`peek`（查看栈顶）

## 2. 使用 `list` 实现（最常见）

Python 的 `list` 末尾操作是 $O(1)$ 均摊，适合作为栈。

```python
stack = []

# push
stack.append(1)
stack.append(2)

# peek
top = stack[-1]  # 2

# pop
val = stack.pop()  # 2

# empty check
is_empty = len(stack) == 0
```

**复杂度**：

- `append`/`pop`（末尾）均摊 $O(1)$

**注意**：

- 不要使用 `pop(0)`，那是队列的错误用法，会导致 $O(n)$。

## 3. 使用 `collections.deque` 实现

`deque` 也可作为栈，支持两端 $O(1)$ 操作。

```python
from collections import deque

stack = deque()
stack.append(1)
stack.append(2)

top = stack[-1]
val = stack.pop()

is_empty = not stack
```

**何时选择 `deque`**：

- 如果同时需要当队列用，或频繁在两端操作。

## 4. 使用 `queue.LifoQueue`（线程安全）

用于多线程场景，带锁，开销更大。

```python
from queue import LifoQueue

stack = LifoQueue()
stack.put(1)
stack.put(2)

# peek 不直接支持，可通过 get/put 或维护额外变量
val = stack.get()

is_empty = stack.empty()
```

**适用场景**：

- 需要线程安全的生产者/消费者模型。

## 5. 常见题型用法模板

### 5.1 括号匹配

```python
def is_valid(s: str) -> bool:
    stack = []
    pairs = {')': '(', ']': '[', '}': '{'}
    for ch in s:
        if ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
        else:
            stack.append(ch)
    return not stack
```

### 5.2 单调栈（以求下一个更大元素为例）

```python
def next_greater(nums):
    stack = []  # 存下标
    res = [-1] * len(nums)
    for i, x in enumerate(nums):
        while stack and nums[stack[-1]] < x:
            res[stack.pop()] = x
        stack.append(i)
    return res
```

## 6. 边界与坑

- **空栈弹出**：`list.pop()` 会抛 `IndexError`，需先判断。
- **栈顶访问**：`stack[-1]` 需保证非空。
- **性能**：大多数刷题场景用 `list` 即可。

## 7. 速查表

| 操作 | list 栈 | deque 栈 | LifoQueue |
| ---- | ------- | -------- | --------- |
| 入栈 | `append(x)` | `append(x)` | `put(x)` |
| 出栈 | `pop()` | `pop()` | `get()` |
| 栈顶 | `stack[-1]` | `stack[-1]` | 不直接支持 |
| 判空 | `not stack` | `not stack` | `empty()` |
| 线程安全 | 否 | 否 | 是 |

---

如果你有指定题目或想要加入更完整的刷题模板（如表达式求值、逆波兰等），告诉我，我可以继续补充。
