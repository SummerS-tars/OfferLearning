class Solution:
    def trainingPlan(self, actions: list[int]) -> list[int]:
        l, r = 0, len(actions) - 1
        while l < r:
            while l < r and actions[l] % 2 != 0: # 让l停在r最左侧的偶数上
                l = l + 1
            while l < r and actions[r] % 2 != 1: # 让r停在l最右侧的奇数上
                r = r - 1
            if l < r:
                actions[l], actions[r] = actions[r], actions[l]
        return actions

def main():
    s = Solution()
    print(s.trainingPlan([1,2,3,4]))

if __name__ == "__main__":
    main()
