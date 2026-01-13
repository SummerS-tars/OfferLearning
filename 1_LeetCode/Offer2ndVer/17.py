class Solution:
    def countNumbers(self, cnt: int) -> list[str]:
        """生成从 1 到 10^cnt - 1 的所有数字（字符串形式），不包含前导零。"""

        def buildNumber(num: list[str], pos: int, res: list[str]) -> None:
            # 递归到叶子：把 num 去掉前导零后加入结果（若全零则跳过）
            if pos == cnt:
                i = 0
                while i < cnt and num[i] == '0':
                    i += 1
                if i == cnt:
                    return  # 全零，不加入结果
                res.append(''.join(num[i:]))
                return

            # 按位填充 0..9
            for d in range(10):
                num[pos] = str(d)
                buildNumber(num, pos + 1, res)

        # 初始化并回溯生成
        num: list[str] = ['0'] * cnt
        res: list[str] = []
        buildNumber(num, 0, res)
        return res

def main():
    s = Solution()
    print(s.countNumbers(3))

if __name__ == "__main__":
    main()