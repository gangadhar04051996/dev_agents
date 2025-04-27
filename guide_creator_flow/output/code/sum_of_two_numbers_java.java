```java
/*
 * Filename: sum_of_two_numbers_java.java
 * Description: This Java program calculates the sum of two numbers with input validation and error handling.
 * It validates if the inputs are indeed integers before performing the addition operation.
 * If the inputs are not valid, it throws an IllegalArgumentException with a descriptive message.
 */

public class SumOfTwoNumbers {

    /**
     * Method to calculate the sum of two integers
     *
     * @param num1 The first integer input
     * @param num2 The second integer input
     * @return The sum of num1 and num2
     * @throws IllegalArgumentException if either input is not an integer or if null.
     */
    public static int sum(String num1Str, String num2Str) {
        // Validate inputs are not null
        if (num1Str == null || num2Str == null) {
            throw new IllegalArgumentException("Both inputs cannot be null.");
        }

        try {
            // Attempt to parse the strings into integers
            int num1 = Integer.parseInt(num1Str);
            int num2 = Integer.parseInt(num2Str);

            // Return the sum of the two integers
            return num1 + num2;

        } catch (NumberFormatException e) {
            // If parsing fails, throw an exception indicating invalid input type
            throw new IllegalArgumentException("Both inputs must be valid integers.");
        }
    }

    public static void main(String[] args) {
        try {
            int result = sum("10", "20");
            System.out.println("The sum is: " + result); // Output: The sum is: 30

            // Testing with invalid input
            result = sum("10", "abc"); // This will throw an exception
        } catch (IllegalArgumentException e) {
            System.err.println("Error: " + e.getMessage());
        }
    }
}
```

### Save this code as `sum_of_two_numbers_java.java` and compile/run it using a Java compiler to see its functionality. This implementation follows Java conventions, includes comprehensive input validation and error handling, and optimizes for performance by leveraging built-in type safety and exception handling mechanisms.