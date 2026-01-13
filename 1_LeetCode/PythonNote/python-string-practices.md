# Python 字符串处理实践速查

适合日常开发、刷题与脚本快速查用。示例默认 Python 3.11，若需兼容更低版本会特别说明。

## 基础与概念

- 字符串类型是不可变对象：所有修改操作都会返回新字符串。
- 文本与二进制：
  - str（文本，Unicode） ↔ bytes（字节）
  - `b = s.encode('utf-8')`，`s = b.decode('utf-8')`
- 原始字符串（正则/Windows 路径常用）：`r"C:\\path\\to"`
- 多行字符串：三引号 `"""..."""`；去公共缩进可用 `textwrap.dedent`。

## 创建与格式化输出

- f-strings（推荐）：
  ```python
  name = 'Alice'; score = 95.123
  f"{name}: {score:.2f}"            # 'Alice: 95.12'
  f"hex: {255:#x}"                  # 'hex: 0xff'
  f"{1000000:,}"                    # '1,000,000'
  ```
- format：`"{:.1%}".format(0.1234)` → '12.3%'
- % 格式化（老式，不推荐新代码使用）：`"%04d" % 7` → '0007'
- 日期格式化：
  ```python
  from datetime import datetime
  dt = datetime(2026, 1, 13, 9, 30)
  dt.strftime('%Y-%m-%d %H:%M')     # '2026-01-13 09:30'
  ```

## 索引、切片与遍历

- 索引/切片：`s[i]`，`s[a:b]`，`s[a:b:c]`；负索引从末尾计；切片创建新字符串。
- 常见片段：
  ```python
  s[::-1]            # 反转
  s[:n]              # 前 n 个字符
  s[-n:]             # 后 n 个字符
  s.replace('\n', '')  # 去换行（注意返回新串）
  ```

## 连接与拼接（性能建议）

- 少量拼接可用 `+` 或 f-strings。
- 循环大量拼接：优选 `''.join(parts)` 或 `io.StringIO`。
  ```python
  parts = []
  for i in range(10000):
      parts.append(str(i))
  s = ''.join(parts)
  ```
- 路径拼接优先 `pathlib`：
  ```python
  from pathlib import Path
  p = Path('base') / 'dir' / 'file.txt'
  ```

## 拆分与合并

- `split()`：按空白（任意空白，连续空白合并），`split(' ')`：仅空格且保留空字符串。
  ```python
  'a  b\t c'.split()      # ['a', 'b', 'c']
  'a  b'.split(' ')        # ['a', '', 'b']
  ```
- 限制分割次数：`s.split(sep, maxsplit)`；右向分割 `rsplit`。
- 行分割：`splitlines(keepends=False)`。
- 三段切分：`partition(sep)` / `rpartition(sep)` → `(head, sep, tail)`。
- 合并：`sep.join(list_of_str)`。

## 去除与填充

- 去空白：`strip()` / `lstrip()` / `rstrip()`（可传字符集）。

    ```python
    '  abc  '.strip()        # 'abc'
    'xxabcx'.strip('x')      # 'abc'
    ```

- 去前导零：`s.lstrip('0') or '0'`（全零兼容）。
- 对齐与填充：`ljust` / `rjust` / `center` / `zfill`。

    ```python
    '7'.zfill(4)             # '0007'
    'abc'.rjust(6, '.')      # '...abc'
    ```

## 查找与判断

- 包含：`substr in s`；计数：`s.count(substr)`。
- 位置：`s.find(substr)`（-1 不存在），`s.index(substr)`（不存在抛异常）。
- 前后缀：`s.startswith(prefix)` / `s.endswith(suffix)`，支持元组：

    ```python
    s.startswith(('http://', 'https://'))
    ```

- 大小写无关比较：`s.casefold()` 比 `lower()` 更适合国际文本。
- 类别判断：`isdigit()` / `isdecimal()` / `isnumeric()`（见“Unicode 与规范化”）。

## 替换与清洗

- 简单替换：`s.replace(old, new, count=-1)`。
- 多字符映射/删除：`str.translate` + `str.maketrans`：

    ```python
    table = str.maketrans({'-': ' ', '_': ' '})
    'a-b_c'.translate(table)          # 'a b c'

    delete = str.maketrans('', '', '.,!?')
    'Hi, you!'.translate(delete)      # 'Hi you'
    ```

- 正则替换（参见下一节）：`re.sub(pattern, repl, s)`。

## 正则表达式（re）

- 常用入口：
  
    ```python
    import re
    pat = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
    pat.findall('2026-01-13, 2026/01/13')   # ['2026-01-13']
    ```

- 查找与分组：

    ```python
    m = re.search(r"(?P<user>[\w.-]+)@(?P<host>[\w.-]+)", 'a.b@example.com')
    m.group('user'), m.group('host')
    ```

- 多分隔符分割：`re.split(r"[,;\s]+", s)`。
- 标志位：`re.I`（忽略大小写）、`re.M`（多行 ^$）、`re.S`（点匹配换行）。
- 原始字符串写法 `r"..."` 可避免反斜杠转义困扰。

## Unicode 与规范化

- 同一“视觉字符”可能有多种编码；正规化减少歧义：

    ```python
    import unicodedata as ud
    s_norm = ud.normalize('NFC', s)   # 或 NFKC 做兼容性折叠
    ```

- 去音标（示例）：

    ```python
    import unicodedata as ud
    def remove_accents(s: str) -> str:
        nfkd = ud.normalize('NFKD', s)
        return ''.join(ch for ch in nfkd if ud.category(ch) != 'Mn')
    ```

- 数字判断差异：
    - `isdecimal()` 最严格（十进制数字）
    - `isdigit()` 覆盖上标等（如 '²'）
    - `isnumeric()` 最宽（含罗马数字等）

## 文本换行、缩进与宽度

- 包装与缩短：

    ```python
    import textwrap as tw
    tw.fill(s, width=80)
    tw.shorten(s, width=32, placeholder='…')
    ```

- 去公共缩进：

    ```python
    from textwrap import dedent
    print(dedent("""
        def f():
            return 42
    """))
    ```

## 读写文件与编码

```python
from pathlib import Path
p = Path('file.txt')
text = p.read_text(encoding='utf-8')
# 写入时确保编码与换行
p.write_text(text, encoding='utf-8', newline='\n')
```

- 若遇到 `\ufeff`（BOM），可在读取后 `lstrip('\ufeff')`。
- JSON：

    ```python
    import json
    s = json.dumps(obj, ensure_ascii=False)   # 保留中文
    obj = json.loads(s)
    ```

## 常见任务代码片段（可直接复制）

- 统计词频：

    ```python
    import re
    from collections import Counter
    words = re.findall(r"\w+", s.lower())
    freq = Counter(words).most_common(10)
    ```

- 仅保留字母数字与空格：

    ```python
    import re
    clean = re.sub(r"[^\w\s]", "", s)
    ```

- 移除重复空白：

    ```python
    import re
    collapsed = re.sub(r"\s+", " ", s).strip()
    ```

- 快速提取数字：

  ```python
  import re
  nums = [int(x) for x in re.findall(r"-?\d+", s)]
  ```

- 简易 slug（URL 片段）：

    ```python
    import re
    slug = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip('-')
    ```

- 多行合并为一行：

    ```python
    one_line = ' '.join(s.splitlines())
    ```

## 类型提示与最佳实践

- 列表类型：`list[str]`（Py3.9+），老版本用 `from typing import List` → `List[str]`。
- 元组类型：`tuple[str, ...]`（变长），`tuple[int, str]`（定长）
- 可迭代/序列：`Iterable[str]` / `Sequence[str]`
- Union：`str | int`（Py3.10+），老版本 `Union[str, int]`
- 不要写 `[str]` 作为类型；那是列表字面量，非类型表达式。

## 常见坑与对策

- `''.join(iterable)` 的“主体”在左侧字符串上，不是 `iterable.join(sep)`。
- `str.replace`、`strip` 等都返回新字符串，原串不变。
- `split()` 与 `split(' ')` 行为不同（是否合并空白）。
- 处理文件需明确 `encoding='utf-8'`，跨平台换行建议 `newline='\n'`。
- Windows 路径用原始字符串或 `pathlib`，避免反斜杠转义。
- 正则请使用原始字符串 `r"..."`；频繁使用的模式先 `re.compile`。
- 切片对“用户感知字符”（如 emoji+变体）可能截断组合字符，精确按“字素簇”分割需更高级库（如 `regex` 第三方包的 `\X`）。

## 性能建议（简）

- 循环内避免频繁 `s += part`，用收集后 `''.join(parts)`。
- 正则多次复用时 `re.compile`。
- 避免无意义的中间大字符串拷贝（链式替换时可合并步骤或用 `translate`）。
- 大文本构造可用 `io.StringIO` 作为缓冲。
