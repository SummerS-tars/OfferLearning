# C++ `std::string` 速查与最佳实践

> 重要内容在前，补充与参考在末尾。建议结合 C++17/20 使用。

## 一页速览（最常用）

- 构造与基本属性
    - `std::string s;` 空串；`std::string s = "hi";`
    - `s.size()`/`s.length()`，`s.empty()`，`s.clear()`，`s.reserve(n)`
    - C++17：`s.data()` 返回可写 `char*`（非常量对象）
- 访问
    - `s[i]`（不检查边界）、`s.at(i)`（越界抛 `out_of_range`）
    - `s.front()`/`s.back()`；`s.c_str()`（与 C API 交互）
- 拼接与追加
    - `s += 'x'`, `s += "abc"`, `s.append("abc")`, `s.push_back('x')`
    - 多次拼接先 `reserve` 预留容量
- 查找与子串
    - `s.find("abc", pos)`；`s.rfind("abc")`
    - `s.find_first_of("abc")` / `find_first_not_of(...)`
    - `s.substr(pos, count)`（`pos` 越界抛异常）
- 替换/插入/删除
    - `s.replace(pos, count, "xyz")`
    - `s.insert(pos, "xyz")`；`s.erase(pos, count)`/`s.pop_back()`
- 数字转换与格式化
    - `std::to_string(x)`；`std::stoi/stol/stoll/stoul/stoull`、`std::stof/stod/stold`
    - C++20：`std::format("{}-{}", a, b)`
- C++20 便捷判断
    - `s.starts_with("pre")` / `s.ends_with("suf")` / `s.contains("x")`
- 参数传递（推荐）
    - 只读形参：`std::string_view sv`
    - 需要持久化：在内部拷贝到 `std::string`

---

## 最佳实践与常见坑（务必熟悉）

1. 边界与异常

    - `operator[]` 越界为未定义行为；`at()` 才会抛异常。
    - `substr(pos, ...)` 若 `pos > size()` 抛 `out_of_range`。

1. 迭代器/指针/引用失效

    - 可能触发重分配的操作（`append/push_back/insert/resize` 等）会使全部迭代器、指针、引用失效。
    - 不增长容量但移动元素的操作（如中间 `erase/insert/replace`）会使受影响区间及其后的迭代器失效。
    - 经验法则：修改后重新获取迭代器；大量扩容前 `reserve`。

1. `\0` 内嵌与 C API

    - `std::string` 可包含内嵌 `\0`，`size()` 真实计数与 NUL 无关。
    - `c_str()` 供 C API 使用，会在首个 `\0` 处视为结束；避免把含内嵌 NUL 的串直接交给 C 函数。

1. 编码与 Unicode

    - `std::string` 是字节容器，不理解“字符/字素”。UTF‑8 下一个字符可由多个字节组成。
    - 按字节的 `substr/find` 可能截断在码点中间。涉及多语言处理，使用 ICU/Boost.Text/utf8cpp 等库。

1. 性能要点

    - 批量拼接：`reserve` + `append` 优于反复 `+`。
    - 小字符串优化（SSO）常见但非强制，短串通常不分配堆内存（实现相关）。
    - C++11 起普遍不再使用写时拷贝（COW），移动构造/赋值更廉价。

1. `string_view` 的正确使用

    - 适合只读、零拷贝视图；不要返回指向临时/已销毁对象的 `string_view`。
    - 需要持久化时，显式转换/拷贝为 `std::string`。

1. `data()` 的写入（C++17+）

    - `auto p = s.data();` 在容量足够且不越界时可原地写入，但必须保持 NUL 终止规则。

---

## 常用代码片段（拿来即用）

- 去除所有空格

    ```cpp
    s.erase(std::remove(s.begin(), s.end(), ' '), s.end());
    ```

- 左右 trim（简单空白集）

    ```cpp
    auto trim = [](std::string s) {
        const char* ws = " \t\n\r\f\v";
        auto l = s.find_first_not_of(ws);
        if (l == std::string::npos) return std::string{};
        auto r = s.find_last_not_of(ws);
        return s.substr(l, r - l + 1);
    };
    ```

- 分割为单词（按空白）

    ```cpp
    std::vector<std::string> tokens;
    std::istringstream iss(s);
    for (std::string t; iss >> t; ) tokens.push_back(std::move(t));
    ```

- 替换所有子串（朴素版）

    ```cpp
    std::string replace_all(std::string s, std::string_view from, std::string_view to) {
        if (from.empty()) return s;
        size_t pos = 0;
        while ((pos = s.find(from, pos)) != std::string::npos) {
            s.replace(pos, from.size(), to);
            pos += to.size();
        }
        return s;
    }
    ```

- 安全的数字解析

    ```cpp
    int value = 0; size_t pos = 0;
    try {
        value = std::stoi(s, &pos, 10); // 解析到 s[pos]
        // 检查是否还有残留非空白
    } catch (const std::invalid_argument&) {
        // 不是数字
    } catch (const std::out_of_range&) {
        // 超出范围
    }
    ```

- 高效拼接（预留容量）

    ```cpp
    std::string out; out.reserve(256);
    for (auto&& piece : pieces) out.append(piece);
    ```

- C++20 前的 starts_with/ends_with（简易实现）

    ```cpp
    bool starts_with(const std::string& s, std::string_view pre) {
        return s.size() >= pre.size() && std::equal(pre.begin(), pre.end(), s.begin());
    }
    bool ends_with(const std::string& s, std::string_view suf) {
        return s.size() >= suf.size() && std::equal(s.end()-suf.size(), s.end(), suf.begin());
    }
    ```

---

## API 分类参考（精选）

- 构造：`string()`, `string(n, ch)`, `string(ptr, n)`, `string(first, last)`
- 大小/容量：`size/length`, `empty`, `capacity`, `reserve`, `shrink_to_fit`, `clear`
- 访问：`operator[]`, `at`, `front`, `back`, `c_str`, `data`
- 追加：`push_back`, `append`, `operator+=`
- 插入/删除：`insert`, `erase`, `pop_back`
- 替换/赋值：`replace`, `assign`
- 子串/查找：`substr`, `find`, `rfind`, `find_first_of`, `find_last_of`, `find_first_not_of`, `find_last_not_of`
- 比较：`compare`，比较运算符 `== != < <= > >=`（字典序）
- C++20：`starts_with`, `ends_with`, `contains`, `operator<=>`（三路比较）

复杂度提示：大多数是线性于操作长度；索引访问与 `size()` 为 O(1)。

---

## 版本差异速记

- C++14：字符串字面量后缀 `"..."s`
- C++17：`string::data()` 可写（对非常量对象）；保证连续存储；`std::string_view`
- C++20：`starts_with/ends_with/contains`，`std::format`，`<=>`，`std::u8string/char8_t`

---

## 宽/Unicode 字符串（补充）

- 类型：`std::wstring`（`wchar_t`），`std::u16string`（`char16_t`），`std::u32string`（`char32_t`），C++20 `std::u8string`（`char8_t`）。
- 注意：这些也只是码元序列；真正“按字符/字素”处理需要专业库（如 ICU）。

---

## 异常与错误（补充）

- `out_of_range`：`at`/`substr` 越界
- `length_error`：长度超上限
- `bad_alloc`：分配失败

---

## 实现与性能细节（补充）

- SSO 多见但非标准要求；临界长度依实现不同。
- 现代实现普遍移除 COW；移动语义可显著降低开销。
- `reserve` 可减少重分配；`shrink_to_fit` 只是提示，可能忽略。

---

## 参考与延伸

- C++ 参考站点：cppreference（字符串相关条目）
- 文本处理：ICU、Boost.Text、utf8cpp
