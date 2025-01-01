#include <iostream>
#include <string>
#include <cassert>

/*
    NOTE: This is a debugging exercise. The code is intentionally buggy.
    
    For an in-depth understanding of how to debug using Visual Studio Code, please refer to the following link:
    
    https://code.visualstudio.com/docs/cpp/cpp-debug

    Another good resource to understand debugging in C++ is:
    https://www.youtube.com/watch?v=0ebzPwixrJA

    g++ -g debug_c.cpp -o debug_c.o
    
    Contents to cover:
    
    1. What is debugging?
    2. How to create a launch.json file?
    3. How to set breakpoints?
    4. Step over, step into, step out, continue, restart, and stop debugging.
    5. How to watch variables?
    6. How to use the debug console?
    7. What are conditional breakpoints?
    
    Final comments:
    
     - Adding cout statements is a good way to debug, but it is not the best way.
    
     - The best way to debug is to use a debugger.
    
     - Where to add breakpoints is a skill that you will develop over time. A good algorithmic understanding will help you optimize the debugging process.
*/

void print_function(const std::string& print_string) {
    // A few assertions to check the input
    
    // Increasing the number of lines for better illustration of the debugging process.
    assert(!print_string.empty() && "The input string should not be empty.");
    
    assert(print_string.find_first_not_of("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ") == std::string::npos && "The input string should contain only alphabets.");
    
    assert(print_string == "Fizz" || print_string == "Buzz" || print_string == "FizzBuzz" && "The input string should be either Fizz, Buzz, or FizzBuzz.");
    
    std::cout << print_string << std::endl;
}

std::string fizz_buzz(int n) {
    if (n % 15 == 0) {
        return "FizzBuzz";
    } else if (n % 3 == 0) {
        return "Fizz";
    } else if (n % 5 == 0) {
        return "Buzz";
    } else {
        return std::to_string(n);
    }
}

void buggy_fizz_buzz(int n) {
    for (int i = 1; i <= n; ++i) {
        std::cout << "i = " << i << " According to the FizzBuzz problem, the output should be: " << fizz_buzz(i) << std::endl;
        if (i % 3 == 0) {
            print_function("Fizz");
            assert("Fizz" == fizz_buzz(i) && "The output should be Fizz.");
        } else if (i % 5 == 0) {
            print_function("Buzz");
            assert("Buzz" == fizz_buzz(i) && "The output should be Buzz.");
        } else if (i % 15 == 0) {
            print_function("FizzBuzz");
            assert("FizzBuzz" == fizz_buzz(i) && "The output should be FizzBuzz.");
        } else {
            std::cout << i << std::endl;
        }
        std::cout << "**********************************************************" << std::endl;
    }
}

void buggy_fizz_buzz_2(int n) {
    for (int i = 1; i <= n; ++i) {
        std::cout << "i = " << i << " According to the FizzBuzz problem, the output should be: " << fizz_buzz(i) << std::endl;
        if (i % 3 == 0 || i % 5 == 0) {
            print_function("FizzBuzz");
            assert("FizzBuzz" == fizz_buzz(i) && "The output should be FizzBuzz.");
        } else if (i % 3 == 0) {
            print_function("Fizz");
            assert("Fizz" == fizz_buzz(i) && "The output should be Fizz.");
        } else if (i % 5 == 0) {
            print_function("Buzz");
            assert("Buzz" == fizz_buzz(i) && "The output should be Buzz.");
        } else {
            std::cout << i << std::endl;
        }
        std::cout << "**********************************************************" << std::endl;
    }
}

int main() {
    buggy_fizz_buzz(20);
    return 0;
}
