# sum of two numbers Implementation Report

## Code Implementation
The implementation has been saved to: `code\sum_of_two_numbers_java.java`

## Flow Diagram
The flow diagram has been saved to: `reports\sum_of_two_numbers_output.mmd`

### Program Flow Description
Here's a description of the program's flow:

1. **`main` Method:** The program execution begins within the `main` method.
2. **`sum` Method Call:**  Inside `main`, the `sum` method is called with two string arguments, "10" and "20".
3. **`sum` Method Logic:**
   - **Input Validation:** The `sum` method first checks if either `num1Str` or `num2Str` is `null`. If so, it throws an `IllegalArgumentException` because null inputs are not allowed.
   - **Integer Parsing:** It then attempts to parse the input strings (`num1Str` and `num2Str`) into integers using `Integer.parseInt()`.
   - **Exception Handling:**  If `Integer.parseInt()` encounters a string that cannot be converted to an integer (e.g., "abc"), it throws a `NumberFormatException`. The `try...catch` block catches this exception.
   - **Sum Calculation:** If both parsing operations are successful, the `sum` method calculates the sum of the two integers (`num1` and `num2`) and returns the result.
4. **Exception Handling in `main`:** The `main` method also includes a `try...catch` block to handle any `IllegalArgumentException` that might be thrown by the `sum` method. If an exception is caught, it prints an error message to the standard error stream (`System.err`).
5. **Output:** In the first test case, the program successfully parses the strings "10" and "20" into integers, calculates their sum (30), and prints "The sum is: 30" to the console. In the second test case, the program attempts to parse "10" and "abc," which results in a `NumberFormatException` being thrown. The `catch` block then handles this exception and prints an error message to the console.

