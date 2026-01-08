# C++ 语法

## STL 常用容器与算法速查

### 1. 核心容器 (Containers)

#### **vector (变长数组)**

* **特点**: 动态数组，支持随机访问 ，尾部插入删除高效。
* **常用函数**:
    * `push_back(x)` / `pop_back()`: 尾部增/删。
    * `size()` / `empty()`: 大小/判空。
    * `clear()`: 清空。
    * `resize(n, val)`: 重置大小为 ，新元素填充 `val`。
    * `begin()` / `end()`: 首迭代器 / 尾后迭代器。

* **技巧**:
    * 局部变量开大数组易爆栈，但 vector 数据存储在堆上，相对安全。
    * `vector<int> a(n, 1)`: 初始化长度为  且全为 1 的数组。

#### **stack (栈)**

* **特点**: 先进后出 (LIFO)。
* **常用函数**:
    * `push(x)`: 入栈。
    * `pop()`: 出栈（不返回元素）。
    * `top()`: 获取栈顶元素。
* **注意**: 不支持遍历，需取出元素或用数组模拟栈来遍历。

#### **queue (队列)**

* **特点**: 先进先出 (FIFO)。
* **常用函数**:
    * `push(x)`: 入队。
    * `pop()`: 出队。
    * `front()`: 获取队首元素。
    * `back()`: 获取队尾元素。

#### **priority_queue (优先队列)**

* **特点**: 自动排序，默认**大根堆**（最大值在堆顶）。
* **常用函数**: `push(x)`, `pop()`, `top()` (注意不是 `front`)。
* **定义方式**:
    * 大根堆 (默认): `priority_queue<int> q;`
    * 小根堆: `priority_queue<int, vector<int>, greater<int>> q;`

#### **map / unordered_map (映射)**

* **区别**:
    * **map**: 基于红黑树，**有序** (按Key从小到大)，增删查复杂度 O(log n)。
    * **unordered_map**: 基于哈希表，**无序**，增删查平均 O(1)。
* **常用函数**:
    * `mp[key]`: 访问或插入元素。
    * `count(key)`: 判断键是否存在。
    * `find(key)`: 返回迭代器，没找到返回 `end()`。
* **技巧**: 访问不存在的键会自动创建空值，建议先用 `count` 判断。

#### **set (集合)**

* **特点**: 元素**唯一**且**有序** (自动去重+排序)。
* **常用函数**:
    * `insert(x)`: 插入。
    * `count(x)`: 检查是否存在。
    * `lower_bound(x)` / `upper_bound(x)`: 二分查找。

---

### 2. 常用算法 (Algorithms)

需包含头文件 `<algorithm>`。

* **sort (排序)**
    * `sort(a.begin(), a.end());`: 默认从小到大。
    * `sort(a.begin(), a.end(), greater<int>());`: 从大到小。
    * 可传入自定义 `cmp` 函数。

* **lower_bound / upper_bound (二分查找)**
    * **前提**: 序列必须有序。
    * `lower_bound`: 返回第一个大于等于 value 的迭代器。
    * `upper_bound`: 返回第一个大于 value 的迭代器。
    * 获取下标通常写作: `lower_bound(...) - a.begin()`。

* **unique (去重)**
    * **前提**: 序列需先排序。
    * 只是将重复元素移到末尾，需配合 `erase` 使用或仅利用返回的新尾部迭代器。

* **next_permutation (全排列)**
    * 生成字典序的下一个排列，常配合 `do-while` 使用。

* **reverse (翻转)**
    * `reverse(a.begin(), a.end())`: 翻转区间内元素。

### 3. 小贴士

* **遍历**: 推荐使用 C++11 的范围 for 循环，例如 `for (auto &x : v) { ... }`。
* **输入**: 对于大量数据，建议关闭流同步 `ios::sync_with_stdio(0); cin.tie(0);`。
* **deque (双端队列)**: 头尾均可 push/pop，但常数较大，非必要少用。
