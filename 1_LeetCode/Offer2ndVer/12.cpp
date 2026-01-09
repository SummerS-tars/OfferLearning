#include <iostream>
#include <vector>
#include <unordered_map>
#include <algorithm>
#include <stack>
#include <string>
using namespace std;

#define PII pair<int,int>
// first为行，second为列

class Solution {
public:
    bool wordPuzzle(vector<vector<char>>& grid, string target) {
        if (target.empty()) return true; // 空串直接成立
        for(auto line = grid.begin(); line!=grid.end(); ++line) {
            for(auto ch = line->begin(); ch != line->end(); ++ch) {
                if(*ch != target[0]) continue;
                auto start = make_pair(line - grid.begin(), ch - line->begin());
                if(findPath(grid, target, start))
                    return true;
            }
        }
        return false;
    }

private:
    // x为列，y为行，取右和下为正方向
    // 方向数组，上、右、下、左（对应0,1,2,3）
    vector<int> dx{0, 1, 0, -1};
    vector<int> dy{-1, 0, 1, 0};

    // 用显式栈（带方向索引）模拟递归 DFS
    bool findPath(vector<vector<char>>& grid, string target, PII start) {
        int R = (int)grid.size();
        int C = R ? (int)grid[0].size() : 0;
        if (R == 0 || C == 0) return false;

        struct Frame { int r, c, idx, nextDir; };
        vector<vector<char>> visited(R, vector<char>(C, 0));
        stack<Frame> st;

        // 起点已匹配 target[0]
        st.push({start.first, start.second, 0, 0});
        visited[start.first][start.second] = 1;

        while (!st.empty()) {
            Frame &cur = st.top();

            if (cur.idx == (int)target.size() - 1) {
                return true; // 完整匹配
            }

            if (cur.nextDir >= 4) {
                // 回溯：撤销访问并弹出
                visited[cur.r][cur.c] = 0;
                st.pop();
                continue;
            }

            int dir = cur.nextDir++;
            int nr = cur.r + dy[dir];
            int nc = cur.c + dx[dir];
            int nextIdx = cur.idx + 1;

            if (nr >= 0 && nr < R && nc >= 0 && nc < C &&
                !visited[nr][nc] && grid[nr][nc] == target[nextIdx]) {
                visited[nr][nc] = 1;
                st.push({nr, nc, nextIdx, 0});
            }
        }
        return false;
    }

    bool validDirection(vector<vector<char>>& grid, char nextChar, vector<vector<int>>& visited, PII current, int direction) {
        int R = (int)grid.size();
        int C = R ? (int)grid[0].size() : 0;
        int nr = current.first + dy[direction];
        int nc = current.second + dx[direction];
        return nr >= 0 && nr < R && nc >= 0 && nc < C &&
               !visited[nr][nc] && grid[nr][nc] == nextChar;
    }
};