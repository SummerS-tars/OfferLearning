from typing import List

class Solution:
    def spiralArray(self, array: List[List[int]]) -> List[int]:
        if not array or not array[0]:
            return []

        rowNum, colNum = len(array), len(array[0])

        visited = [[0] * colNum for _ in range(rowNum)]
        res = []
        r, c = 0, 0

        while c < colNum and not visited[r][c]:
            while c+1 < colNum and not visited[r][c+1]: # 未超出未访问区域边界
                res.append(array[r][c])
                visited[r][c] = 1
                c = c + 1
            
            while r+1 < rowNum and not visited[r+1][c]:
                res.append(array[r][c])
                visited[r][c] = 1
                r = r + 1
            
            while c-1 >= 0 and not visited[r][c-1]:
                res.append(array[r][c])
                visited[r][c] = 1
                c = c - 1
            
            while r-1 >= 0 and not visited[r-1][c]:
                res.append(array[r][c])
                visited[r][c] = 1
                r = r - 1
            
            res.append(array[r][c])
            visited[r][c] = 1
            c = c + 1 # 试图移入到内环
        
        return res

def main():
    sol = Solution()
    array = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9,10,11,12],
        [13,14,15,16]
    ]
    print(sol.spiralArray(array))  # Expected output: [1,2,3,4,8,12,16,15,14,13,9,5,6,7,11,10]

if __name__ == "__main__":
    main()
