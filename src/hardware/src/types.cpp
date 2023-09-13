#ifndef TYPES_H
#define TYPES_H

#include <string>
#include <initializer_list>
#include <map>

#include <stdint.h>
#define func auto
#define var decltype(auto)


namespace types {
    using None = void;

    using i8 = int8_t;
    using u8 = uint8_t;

    using i16 = int16_t;
    using u16 = uint16_t;

    using i32 = int32_t;
    using u32 = uint32_t;

    using i64 = int64_t;
    using u64 = uint64_t;

    using Str = std::string;

    template<typename T>
    using IList = std::initializer_list<T>;

    template<typename K, typename V>
    using Map = std::map<K, V>;
}

#endif