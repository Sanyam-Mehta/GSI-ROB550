"""
    NOTE: This is a debugging exercise. The code is intentionally buggy.
    
    For an in-depth understanding of how to debug using Visual Studio Code, please refer to the following link:
    
    https://code.visualstudio.com/docs/editor/debugging
    
    
    Another good resource to understand debugging in Python is:
    https://www.youtube.com/watch?v=7qZBwhSlfOo
    
    Contents to cover:
    
    1. What is debugging?
    2. How to create a launch.json file?
    3. How to set breakpoints?
    4. Step over, step into, step out, continue, restart, and stop debugging.
    5. How to watch variables?
    6. How to use the debug console?
    7. What are conditional breakpoints?
    
    Final comments:
    
     - Adding print statements is a good way to debug, but it is not the best way.
    
     - The best way to debug is to use a debugger.
    
     - Where to add breakpoints is a skill that you will develop over time. A good algorithmic understanding will help you optimize the debugging process.
"""



def print_function(print_string):
    """
        This function prints the input string.
    """
    # A few assertions to check the input
    
    # I am also doing to increase the number of lines of the function for better illustration of the debugging process.
    assert type(print_string) == str, "The input should be a string."
    
    assert len(print_string) > 0, "The input string should not be empty."
    
    assert print_string.isalpha(), "The input string should contain only alphabets."
    
    assert print_string in ["Fizz", "Buzz", "FizzBuzz"], "The input string should be either Fizz, Buzz, or FizzBuzz."
    
    print(print_string)
    

def buggy_fizz_buzz(n):
    """
        Definition of the FizzBuzz problem:
        
        Write a program that prints the numbers from 1 to n. 
        But for multiples of three print “Fizz” instead of the number 
        and for the multiples of five print “Buzz”. 
        For numbers which are multiples of 15 print “FizzBuzz”.
    """
    for i in range(1, n + 1):
        print("i = ", i, " According to the FizzBuzz problem, the output should be: ", fizz_buzz(i))
        if i % 3 == 0:
            print_function("Fizz")
            assert "Fizz" == fizz_buzz(i), "The output should be Fizz."
        elif i % 5 == 0:
            print_function("Buzz")
            assert "Buzz" == fizz_buzz(i), "The output should be Buzz."
        elif i % 15 == 0:
            print_function("FizzBuzz")
            assert "FizzBuzz" == fizz_buzz(i), "The output should be FizzBuzz."
        else:
            print(i)
        print("**********************************************************")
            
def buggy_fizz_buzz_2(n):
    """
        Definition of the FizzBuzz problem:
        
        Write a program that prints the numbers from 1 to n. 
        But for multiples of three print “Fizz” instead of the number 
        and for the multiples of five print “Buzz”. 
        For numbers which are multiples of 15 print “FizzBuzz”.
    """
    for i in range(1, n + 1):
        print("i = ", i, " According to the FizzBuzz problem, the output should be: ", fizz_buzz(i))
        if i % 3 == 0 or i % 5 == 0:
            print_function("FizzBuzz")
            assert "FizzBuzz" == fizz_buzz(i), "The output should be FizzBuzz."
        elif i % 3 == 0:
            print_function("Fizz")
            assert "Fizz" == fizz_buzz(i), "The output should be Fizz."
        elif i % 5 == 0:
            print_function("Buzz")
            assert "Buzz" == fizz_buzz(i), "The output should be Buzz."
        else:
            print(i)
        print("**********************************************************")
        
        
def fizz_buzz(n):
    """
        Definition of the FizzBuzz problem:
        
        Write a program that prints the numbers from 1 to n. 
        But for multiples of three print “Fizz” instead of the number 
        and for the multiples of five print “Buzz”. 
        For numbers which are multiples of 15 print “FizzBuzz”.
    """
    if n % 15 == 0:
        return "FizzBuzz"
    elif n % 3 == 0:
        return "Fizz"
    elif n % 5 == 0:
        return "Buzz"
    else:  
        return n

       
# Test the function
buggy_fizz_buzz(20)