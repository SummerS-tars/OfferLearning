#include <iostream>
#include <vector>
#include <unordered_map>
#include <algorithm>
#include <stack>
#include <string>
using namespace std;
class Solution {
public:
    bool wordPuzzle(vector<vector<char>>& grid, string target) {
        if(grid.empty()) return false;
        raws = grid.size();
        cols = grid[0].size();
        for(int r = 0; r < raws; ++r) {
            for(int c = 0; c < cols; ++c) {
                if(findPath(grid, target, r, c, 0)) return true;
            }
        }
        
        return false;
    }

private:
    int raws;
    int cols;

    bool findPath(vector<vector<char>>& grid, string target, int r, int c, int idx) {
        if(r < 0 || r >= raws || c < 0 || c >= cols || !grid[r][c] || grid[r][c] != target[idx]) return false;
        if(idx == target.size() - 1) return true;
        grid[r][c] = '\0';
        idx++;
        bool isPath = findPath(grid, target, r-1, c, idx) || findPath(grid, target, r, c+1, idx) ||
                    findPath(grid, target, r+1, c, idx) || findPath(grid, target, r, c-1, idx);
        grid[r][c] = target[idx-1];
        return isPath;
    }
};