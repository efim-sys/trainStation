#ifndef TOOLS_H
#define TOOLS_H

#include "types.cpp"
using namespace types;

#define MLS(...)  #__VA_ARGS__


namespace tools {
    inline func format(Str temp, IList<Str> args_) -> Str {
        var args = args_.begin();
        Str fmt = "";

        u16 size = temp.size();
        u16 index = 0;

        for (u16 ind = 0; ind < size; ind++) {
            char c = temp[ind];
            if (c == '{') {
                fmt += args[(ind++, index++)];
            } else {
                fmt += c;
            }
        }

        return fmt;
    }
}

#endif