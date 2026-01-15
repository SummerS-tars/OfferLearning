# Python 中的 Queue（队列）使用归纳

> 分为基础部分、实践示例部分、延伸部分，适合刷题与工程实践快速查阅。

## 一、基础部分

### 1. 队列的核心特性

- 先进先出（FIFO）
- 典型操作：`enqueue`（入队）、`dequeue`（出队）、`front`（队首）

### 2. 使用 `collections.deque`（推荐）

`deque` 支持两端 $O(1)$ 操作，是 Python 中最常见的队列实现。

```python
from collections import deque

q = deque()

# enqueue
q.append(1)
q.append(2)

# front
front = q[0]  # 1

# dequeue
val = q.popleft()  # 1

# empty check
is_empty = not q
```

**复杂度**：

- `append` / `popleft` 均摊 $O(1)$

### 3. 使用 `queue.Queue`（线程安全）

适用于多线程生产者/消费者场景，内部带锁。

```python
from queue import Queue

q = Queue()

q.put(1)
q.put(2)

front = q.queue[0]  # 访问内部队列（仅限了解）
val = q.get()

is_empty = q.empty()
```

**适用场景**：

- 需要线程安全的队列

### 4. 不推荐的方式：`list`

`list.pop(0)` 是 $O(n)$，不适合高频出队。

```python
q = []
q.append(1)
q.append(2)

val = q.pop(0)  # 慢
```

---

## 二、实践示例部分

### 1. BFS 模板（图/树的层序遍历）

```python
from collections import deque

def bfs(start, graph):
    q = deque([start])
    visited = {start}
    order = []

    while q:
        node = q.popleft()
        order.append(node)
        for nei in graph[node]:
            if nei not in visited:
                visited.add(nei)
                q.append(nei)

    return order
```

### 2. 滑动窗口固定大小（保持队列长度）

```python
from collections import deque

def window_sum(nums, k):
    q = deque()
    s = 0
    res = []

    for i, x in enumerate(nums):
        q.append(x)
        s += x
        if len(q) > k:
            s -= q.popleft()
        if i >= k - 1:
            res.append(s)

    return res
```

### 3. 双端队列实现单调队列（窗口最大值）

```python
from collections import deque

def max_sliding_window(nums, k):
    dq = deque()  # 存下标
    res = []

    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)

        if dq[0] <= i - k:
            dq.popleft()

        if i >= k - 1:
            res.append(nums[dq[0]])

    return res
```

---

## 三、延伸部分

### 1. `asyncio.Queue`

适用于异步任务之间的生产/消费。

```python
import asyncio

async def producer(q):
    await q.put(1)

async def consumer(q):
    item = await q.get()
    q.task_done()

async def main():
    q = asyncio.Queue()
    await producer(q)
    await consumer(q)

asyncio.run(main())
```

### 2. `queue.PriorityQueue`（优先队列）

按优先级出队，常用于 Dijkstra / 任务调度。

```python
from queue import PriorityQueue

pq = PriorityQueue()

pq.put((2, "task-b"))
pq.put((1, "task-a"))

priority, task = pq.get()  # (1, "task-a")
```

### 3. `heapq` 实现优先队列（非线程安全）

更轻量，性能更好。

```python
import heapq

pq = []
heapq.heappush(pq, (2, "task-b"))
heapq.heappush(pq, (1, "task-a"))

priority, task = heapq.heappop(pq)
```

---

如果你希望加入“阻塞队列/延迟队列/环形队列”相关内容，我可以继续扩展。
