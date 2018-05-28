#ifndef UTIL_H
#define UTIL_H

#include <string>
#include <vector>
#include <sstream>

namespace utl {

template<typename Out>
void split(const std::string &s, char delim, Out result) {
    std::stringstream ss(s);
    std::string item;
    while (std::getline(ss, item, delim)) {
        *(result++) = item;
    }
}

std::vector<std::string> split(const std::string &s, char delim) {
    std::vector<std::string> elems;
    split(s, delim, std::back_inserter(elems));
    return elems;
}

template<typename T>
int index(std::vector<T> vec, const T &to_find) {
	std::ptrdiff_t pos = std::find(vec.begin(), vec.end(), to_find) - vec.begin();
	return pos;
}

std::string replace(const std::string& str, const std::string& from, const std::string& to) {
    
    std::string result (str);
    size_t start_pos = str.find(from);
    
    if (start_pos == std::string::npos) {
        return result;
    }
    
    result.replace(start_pos, from.length(), to);
    
    return result;

}

} // namespace utl

#endif // UTIL_H