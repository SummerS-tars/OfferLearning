"""
正则匹配（支持 '.' 与 '*'）的动态规划解法（底层迭代 DP）

问题定义：
- 给定文本 s 与模式 p，判断 p 是否能匹配 s。
- 规则：
  - '.' 可以匹配任意单个字符
  - '*' 作用于它前面的字符（或 '.'），表示该字符可以重复出现 0 次或多次

本实现采用“自底向上”的 DP：
- 定义状态 dp[i][j]：表示 s[i:] 与 p[j:] 能否匹配（布尔值）
- 目标答案：dp[0][0]
- 边界：dp[n][m] = True（空串匹配空模式）
- 转移：
  - 设 first = (i < n) and (p[j] == s[i] or p[j] == '.')
  - 若 j+1 < m 且 p[j+1] == '*':
      dp[i][j] = dp[i][j+2]                   # 使用 0 次该字符
               or (first and dp[i+1][j])      # 使用 ≥1 次该字符（消耗 s 的一个字符，保持 p 不动）
  - 否则（普通字符或 '.'）：
      dp[i][j] = first and dp[i+1][j+1]

复杂度分析：
- 时间：O(n * m) —— 每个 (i, j) 状态只计算一次，转移常数级
- 空间：O(n * m) —— DP 表大小为 (n+1) x (m+1)

与递归回溯相比：
- 递归在最坏情况下（尤其是含有多个 '*'）会指数级爆炸；
- DP 把重叠子问题合并成表格计算，显著降低到 O(nm)。
"""

from typing import List


class Solution:
    def articleMatch(self, s: str, p: str) -> bool:
        """迭代 DP 实现正则匹配（支持 '.' 与 '*'），返回是否匹配。

        参数:
        - s: 待匹配文本
        - p: 模式字符串

        返回:
        - bool: 是否匹配

        说明:
        - 不使用字符串切片参与状态（避免隐性线性拷贝开销），仅使用索引。
        - 采用 (n+1) x (m+1) 的布尔 DP 表，按 i 从 n 到 0，j 从 m-1 到 0 反向填充。
        """
        n, m = len(s), len(p)
        # dp[i][j] 表示 s[i:] 与 p[j:] 是否匹配
        dp: List[List[bool]] = [[False] * (m + 1) for _ in range(n + 1)]

        # 边界：空串匹配空模式
        dp[n][m] = True

        # 反向填表：i 从 n 到 0，j 从 m-1 到 0
        # 注意：当 i == n 时，s[i] 越界，first 为 False，仅可能用 0 次 '*' 来匹配剩余模式
        for i in range(n, -1, -1):
            for j in range(m - 1, -1, -1):
                # 当前位是否匹配（只有 i < n 时才可能匹配一个字符）
                first = (i < n) and (p[j] == s[i] or p[j] == '.')

                # 看下一位是否是 '*'
                if j + 1 < m and p[j + 1] == '*':
                    # 两种可能：
                    # 1) 使用 0 次该字符：跳过 p[j] 和 '*', 即 j+2
                    # 2) 使用 ≥1 次该字符：若 first 为 True，消耗 s 的一个字符（i+1），模式保持在 j（因为还可以继续重复）
                    dp[i][j] = dp[i][j + 2] or (first and dp[i + 1][j])
                else:
                    # 普通字符或 '.'：必须当前匹配，且 i、j 都前进一位
                    dp[i][j] = first and dp[i + 1][j + 1]

        return dp[0][0]


def main():
    sol = Solution()

    # 用例 1：LeetCode 经典示例
    s = "aab"
    p = "c*a*b"  # True：c* 可匹配 0 次，a* 匹配 "aa"，b 匹配 "b"
    print("case1:", sol.articleMatch(s, p))

    # 用例 2：
    s1 = "mississippi"
    p1 = "mis*is*p*."  # False：按规则最终无法覆盖完整 s1
    print("case2:", sol.articleMatch(s1, p1))

    # 用例 3：
    s2 = "a"
    p2 = "ab*"  # True：b* 可匹配 0 次
    print("case3:", sol.articleMatch(s2, p2))

    # 更多自检用例
    cases = [
        ("", ""),                # True：空匹配空
        ("", "a*"),              # True：a* 可以匹配 0 次
        ("", ".*"),              # True：.* 可以匹配 0 次
        ("abc", "abc"),          # True：完全相同
        ("abc", "a.c"),          # True：'.' 匹配一个字符
        ("abbbbc", "ab*c"),      # True：b* 匹配多次 b
        ("abcd", "d*"),          # False：d* 只能匹配末尾，无法覆盖前面的字符
        ("aaa", "a*a"),          # True：a* 可匹配多次，后面再匹配一个 a
        ("aaa", "ab*a*c*a"),     # True：经典例
    ]
    for idx, (ss, pp) in enumerate(cases, start=1):
        print(f"extra{idx}:", sol.articleMatch(ss, pp))


if __name__ == "__main__":
    main()
