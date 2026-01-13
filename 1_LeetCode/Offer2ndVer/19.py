class Solution:
    def articleMatch(self, s: str, p: str) -> bool:
        if len(s) == 0 and len(p) == 0:
            return True
        elif len(s) != 0 and len(p) == 0:
            return False
        elif len(s) == 0 and len(p) != 0: # 调整边界条件，处理s已经为空，而p中有若干个 * 统配符的情况
            if len(p) >= 2 and p[1] == '*':
                return self.articleMatch(s, p[2::])# 匹配0个字符尝试
            else:
                return False

        hasAst: bool = False # 标识是否第二个为通配符 *
        if len(p) >=2 and p[1] == '*':
            hasAst = True

        charPatch: bool = False
        if not hasAst: # 先处理非 * 通配符情况
            if p[0] == '.':
                charPatch = True
            elif s[0] == p[0]:
                charPatch = True
            
            if charPatch:
                return self.articleMatch(s[1::], p[1::])
            else:
                return False
        
        else: # 处理带 * 统配符情况
            if self.articleMatch(s, p[2::]): # 匹配0个字符尝试
                return True
            chToPatch = p[0]
            for i, ch in enumerate(s): # 依次增加通配符 * 匹配字符串长度直至有字串匹配成功或者全都失败
                if ch == chToPatch or chToPatch == '.':
                    charPatch = self.articleMatch(s[i+1::], p[2::])
                    if charPatch:
                        return True # 存在子串成功匹配
                else:
                    return False # 通配符匹配结束，但字串匹配失败

        return False # 全部尝试失败
                
def main():
    s = "aab"
    p = "c*a*b"
    solution = Solution()
    result = solution.articleMatch(s, p)
    print(result)

    s1 = "mississippi"
    p1 = "mis*is*p*."
    # p1 = "mis*is*ip*."
    result1 = solution.articleMatch(s1, p1)
    print(result1)

    s2 = "a"
    p2 = "ab*"
    result2 = solution.articleMatch(s2, p2)
    print(result2)

if __name__ == "__main__":
    main()
