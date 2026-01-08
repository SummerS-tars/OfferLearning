# C++ STL 迭代器使用方法大全（实战速查）

> 更新时间：2026-01-08

本文系统整理 C++ STL 迭代器（iterator）的核心概念、分类、常用操作、与算法的协作、迭代器失效规则与安全改容器的技巧，并配套常见容器示例与易错点，力求够用、好用、能避坑。

---

## 什么是迭代器

- 迭代器是“泛型指针”，提供统一的方式遍历容器中的元素，并与算法协作。
- 迭代器提供访问接口（解引用、前进后退、比较等），不关心容器内部结构。
- 使用 `begin()/end()` 获取迭代器范围；`end()` 指向尾后位置，不能解引用。

---

## 迭代器分类（能力由弱到强）

- InputIterator：只读，单遍扫描，支持 `++`、解引用 `*`、比较 `==/!=`。
- OutputIterator：只写，单遍扫描，支持 `++`、写入 `*it = value`。
- ForwardIterator：可读写，多遍扫描，支持 `++`、比较，类似单向链表迭代。
- BidirectionalIterator：在 Forward 基础上支持 `--`，如 `list`、关联容器迭代器。
- RandomAccessIterator：随机访问，支持 `it[n]`、`it + n`、`it - n`、关系比较，如 `vector`、`deque`、`array`、`string`。
- ContiguousIterator（C++20）：元素物理连续，如 `vector`、`array`、`string`；可与 C API 互操作。

提示：算法会根据迭代器类别选择最优实现；随机访问迭代器能让 `sort`/`nth_element` 等高效工作。

---

## 容器与迭代器能力映射

- 连续序列容器：
    - `vector<string>` / `std::string` / `array<T,N>`：RandomAccess + Contiguous
    - `deque<T>`：RandomAccess（非连续）
    - `list<T>`：Bidirectional
    - `forward_list<T>`：Forward
- 关联容器：
    - `set/map/multiset/multimap`：Bidirectional
    - `unordered_set/unordered_map`（哈希）：至少 Forward（多数实现为 Forward/Bidirectional）
- 适配器（无迭代器）：`stack`、`queue`、`priority_queue`

---

## 获取迭代器的方式

- `begin(), end()`：可变迭代器（容器非 const 时）。
- `cbegin(), cend()`：只读迭代器（const_iterator）。
- `rbegin(), rend()` / `crbegin(), crend()`：反向迭代器（从尾到头）。

示例：

```cpp
std::vector<int> v{1,2,3};
for (auto it = v.begin(); it != v.end(); ++it) {
    std::cout << *it << " ";
}
```

---

## 常用迭代器操作

- 解引用与成员访问：`*it`、`it->member`
- 移动：`++it`、`it++`、（双向容器）`--it`、`it--`
- 随机访问（RandomAccess）：`it + n`、`it - n`、`it[n]`、`it2 - it1`
- 比较：`it == jt`、`it != jt`；随机访问还支持 `<, <=, >, >=`
- 通用工具：`std::next(it, n)`、`std::prev(it, n)`、`std::advance(it, n)`、`std::distance(first, last)`

```cpp
auto it = std::next(v.begin(), 2); // 指向第 3 个元素
std::advance(it, -1);              // 回到第 2 个元素
auto len = std::distance(v.begin(), v.end());
```

---

## const 与非 const 迭代器

- `const_iterator`：不能通过迭代器写元素，但容器本身仍可变（若容器非 const）。
- `iterator`：可读写元素。
- 规则：
    - `const Container c;` 只能 `cbegin()/cend()`。
    - 非 const 容器可用 `begin()/end()` 或显式 `const_iterator` 保持只读遍历。

---

## 反向迭代器与 `base()`

- `rbegin()` 指向最后一个元素，`rend()` 指向首元素前一个位置的“反向尾后”。
- `reverse_iterator::base()` 返回对应的正向迭代器，它指向“当前反向迭代器所指元素的下一个位置”。

```cpp
std::vector<int> v{1,2,3,4};
auto rit = v.rbegin();      // 指向 4
auto it  = rit.base();      // 指向 4 的下一个，即 end()
// 若要在正向视图中删除反向迭代器所指的元素：
v.erase(std::prev(rit.base())); // 删除 4
```

---

## 插入迭代器（输出迭代器族）

- `std::back_inserter(c)`：将赋值重定向为 `c.push_back(value)`。
- `std::front_inserter(c)`：将赋值重定向为 `c.push_front(value)`（需支持 push_front）。
- `std::inserter(c, pos)`：将赋值重定向为 `c.insert(pos, value)`。

```cpp
std::vector<int> src{1,2,3};
std::deque<int>  dst;
std::copy(src.begin(), src.end(), std::back_inserter(dst));
```

---

## 流迭代器（与 IO 流协作）

- `std::istream_iterator<T>`：从输入流读取元素。
- `std::ostream_iterator<T>`：向输出流写元素。

```cpp
std::istream_iterator<int> in(std::cin), eof;
std::vector<int> v(in, eof); // 读到 EOF
std::sort(v.begin(), v.end());
std::ostream_iterator<int> out(std::cout, " ");
std::copy(v.begin(), v.end(), out);
```

---

## 与算法的协作（algorithm 头文件）

- 查找/计数：`std::find`、`std::find_if`、`std::count_if`
- 复制/变换：`std::copy`、`std::copy_if`、`std::transform`
- 排序/选择：`std::sort`、`std::stable_sort`、`std::nth_element`、`std::partial_sort`
- 合并/集合：`std::merge`、`std::set_union`、`std::set_intersection`
- 移除族：`std::remove`、`std::remove_if`、`std::unique`（注意不改变容器大小，仅重排）
- 其他：`std::for_each`、`std::accumulate`（numeric 头文件）等

```cpp
// 将偶数提取到另一个容器
std::vector<int> v{1,2,3,4,5,6};
std::vector<int> evens;
std::copy_if(v.begin(), v.end(), std::back_inserter(evens), [](int x){return x%2==0;});
```

---

## “擦除-去除”惯用法（erase-remove idiom）

- `std::remove`/`remove_if` 仅将需要移除的元素“挪到末尾”，返回新的逻辑尾迭代器。
- 需再调用容器的 `erase` 真正缩小容器大小。

```cpp
// 删除所有偶数
v.erase(std::remove_if(v.begin(), v.end(), [](int x){return x%2==0;}), v.end());
```

---

## 迭代器失效（非常重要）

- `vector/string`：
    - `push_back`/`insert` 可能导致扩容，所有迭代器、引用、指针失效。
    - `erase` 删除位置及其后的迭代器失效。
- `deque`：
    - 在首尾插入可能导致部分迭代器失效；中间插入/删除影响更大。
- `list/forward_list`：
    - `insert`/`erase` 不使其他迭代器失效（指向被删元素的迭代器失效）。
- 关联容器（`set/map/unordered_*`）：
    - 插入/删除通常不使其他迭代器失效（被删元素的迭代器失效）。

建议：

1) 修改容器后，优先使用返回的新迭代器继续遍历（如 `it = c.erase(it)`）。
2) 对 `vector` 等可能扩容的操作，先 `reserve` 以避免扩容导致失效。

---

## 安全修改容器时的遍历模板

```cpp
// 方案 A：使用 erase 返回的新迭代器（推荐）
for (auto it = v.begin(); it != v.end(); ) {
    if (*it % 2 == 0) it = v.erase(it); // 删除后返回下一个有效迭代器
    else ++it;
}

// 方案 B：先收集要删的迭代器/索引，后统一处理（适合复杂条件）
std::vector<size_t> idx;
for (size_t i = 0; i < v.size(); ++i) if (should_remove(v[i])) idx.push_back(i);
for (auto it = idx.rbegin(); it != idx.rend(); ++it) v.erase(v.begin() + *it); // 从后往前删
```

---

## 范围 for 与 Ranges（C++20+）

- 范围 for：语法糖，底层仍用 `begin()/end()`。

```cpp
for (const auto& x : v) std::cout << x << " ";
```

- `std::ranges`：以“范围”为中心的算法与视图，减少手工迭代器操作。

```cpp
// 筛偶数、平方、输出
using namespace std::ranges;
std::vector<int> v{1,2,3,4,5,6};
auto view = v | views::filter([](int x){return x%2==0;})
               | views::transform([](int x){return x*x;});
for (int x : view) std::cout << x << ' ';
```

---

## 常用容器迭代示例

```cpp
// vector：随机访问
std::vector<int> v{1,2,3};
auto it = v.begin();
it += 2;           // 指向 3
std::cout << *it;  // 3

// list：双向，不能随机访问
std::list<int> L{1,2,3};
auto it2 = L.begin();
std::advance(it2, 2); // O(n) 前进到第 3 个
std::cout << *it2;    // 3

// map：迭代器指向 pair<const K, V>
std::map<std::string, int> m{{"a",1},{"b",2}};
for (auto it = m.begin(); it != m.end(); ++it) {
    std::cout << it->first << ":" << it->second << "\n";
}

// unordered_set：至少 Forward
std::unordered_set<int> us{1,2,3};
for (auto it = us.begin(); it != us.end(); ++it) {
    std::cout << *it << " ";
}

// string：随机访问 + contiguous
std::string s = "hello";
for (auto rit = s.rbegin(); rit != s.rend(); ++rit) std::cout << *rit; // 反序输出
```

---

## 迭代器速查表（Cheat Sheet）

- 获取：`begin/end`、`cbegin/cend`、`rbegin/rend`、`crbegin/crend`
- 工具：`next/prev/advance/distance`
- 插入迭代器：`back_inserter/front_inserter/inserter`
- 流迭代器：`istream_iterator/ostream_iterator`
- 常用算法：`copy/copy_if/transform/find/remove/remove_if/unique/sort/for_each`
- 安全删除：`it = c.erase(it)`、或 `erase(remove_if(...), end)`
- 失效规避：`vector.reserve(n)`、使用 `erase` 返回的迭代器继续遍历

---

## 常见坑与避免

1) 解引用 `end()`：未定义行为，绝对禁止。
2) 修改容器导致迭代器失效：对 `vector`/`deque`/`string` 尤其警惕扩容与删除。
3) `remove` 不改变容器大小：必须配合 `erase`。
4) `reverse_iterator::base()` 指向“下一个”位置：常与 `prev` 配合得正向位置。
5) 在 `map` 中修改 `key`：不可行（`key` 是 `const`）；如需改键，需插入新元素并删除旧元素。
6) `unordered_*` 遍历顺序不稳定：不要依赖遍历顺序做逻辑。

---

## 小结

迭代器让容器与算法解耦、统一协作。掌握迭代器类别与失效规则，是写对 STL 的关键。实战中优先使用算法与插入迭代器减少手写循环；复杂改容器时用 `erase` 返回值或“先收集后处理”的策略，避免失效与未定义行为。
