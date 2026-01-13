#include <iostream>
#include <vector>
using namespace std;

class Solution {
public:
    int wardrobeFinishing(int m, int n, int cnt) {
        raws = m, cols = n, this->cnt = cnt;
        vector<vector<int>> visited(raws, vector<int>(cols, 0));
        return dfsFindBlock(visited, 0, 0);
    }

private:
    int raws;
    int cols;
    int cnt;

    int dfsFindBlock(vector<vector<int>>& visited, int r, int c) {
        // 边界与约束检查
        if (r < 0 || r >= raws || c < 0 || c >= cols) return 0;
        if (visited[r][c] || digit(r) + digit(c) > cnt) return 0;
        visited[r][c] = 1;
        return 1 + dfsFindBlock(visited, r, c+1) + dfsFindBlock(visited, r+1, c);
    }

    int digit(int num) {
        int result = 0;
        if (num < 0) num = -num;
        while (num) {
            result += num % 10;
            num /= 10;
        }
        return result;
    }
};