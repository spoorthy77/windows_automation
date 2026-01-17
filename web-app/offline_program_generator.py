"""
Offline Program Generator
Generates syntax-correct source code for common programming tasks
Languages: Python, Java, C, C++
100% offline: uses local templates and fuzzy topic matching
"""

from typing import Dict, Optional, Tuple
import os
import ast


# Supported languages and file extensions
LANGUAGE_EXTENSIONS = {
    'python': '.py',
    'java': '.java',
    'c': '.c',
    'cpp': '.cpp'
}


# Canonical topics and synonyms for fuzzy selection
TOPIC_SYNONYMS: Dict[str, Tuple[str, ...]] = {
    'prime_number': (
        'prime', 'prime number', 'is prime', 'primes', 'check prime'
    ),
    'sum_three_numbers': (
        'sum of three numbers', 'add three numbers', 'addition of three numbers',
        'sum three numbers', 'sum 3 numbers', 'add 3 numbers',
        'add three integers', 'sum of three integers', 'addition of three integers'
    ),
    'factorial': (
        'factorial', 'fact', 'n!', 'compute factorial'
    ),
    'fibonacci': (
        'fibonacci', 'fibo', 'fib sequence', 'fibonacci series'
    ),
    'sum_two_numbers': (
        'sum of two numbers', 'add two numbers', 'addition of two numbers',
        'sum two numbers', 'sum 2 numbers', 'add 2 numbers',
        'add two integers', 'sum of two integers', 'addition of two integers'
    ),
    'palindrome': (
        'palindrome', 'is palindrome', 'reverse equals'
    ),
    'reverse_string': (
        'reverse string', 'string reverse', 'rev string'
    ),
    'sum_array': (
        'sum array', 'array sum', 'sum of array', 'sum list'
    ),
    'bubble_sort': (
        'bubble sort', 'sort bubble', 'simple sort'
    ),
    'binary_search': (
        'binary search', 'bsearch', 'search sorted'
    ),
    'gcd': (
        'gcd', 'greatest common divisor', 'hcf', 'highest common factor'
    ),
    'lcm': (
        'lcm', 'least common multiple'
    ),
}


def normalize_language(text: str) -> Optional[str]:
    t = text.lower()
    if 'python' in t or 'py' in t:
        return 'python'
    if 'java' in t:
        return 'java'
    # Handle C++ variants first
    if 'c++' in t or 'cpp' in t or 'c plus plus' in t:
        return 'cpp'
    # Bare 'c' with word boundary
    tokens = [tok.strip() for tok in t.replace('\n', ' ').split(' ')]
    if 'c' in tokens:
        return 'c'
    return None


def fuzzy_topic(text: str) -> Optional[str]:
    from rapidfuzz import fuzz
    t = text.lower()
    best_topic, best_score = None, 0
    for topic, synonyms in TOPIC_SYNONYMS.items():
        for s in synonyms:
            score = fuzz.partial_ratio(t, s)
            if score > best_score:
                best_topic, best_score = topic, score
    # Require a modest confidence to avoid random matches
    return best_topic if best_score >= 60 else None


def py_templates() -> Dict[str, str]:
    return {
        'prime_number': (
            """def is_prime(n: int) -> bool:\n    if n <= 1:\n        return False\n    if n <= 3:\n        return True\n    if n % 2 == 0 or n % 3 == 0:\n        return False\n    i = 5\n    while i * i <= n:\n        if n % i == 0 or n % (i + 2) == 0:\n            return False\n        i += 6\n    return True\n\nif __name__ == '__main__':\n    try:\n        value = int(input('Enter a number: '))\n        print('Prime' if is_prime(value) else 'Not prime')\n    except ValueError:\n        print('Please enter a valid integer.')\n"""
        ),
        'sum_two_numbers': (
            """def sum_two_numbers(a: int, b: int) -> int:\n    return a + b\n\nif __name__ == '__main__':\n    try:\n        a = float(input('Enter first number: '))\n        b = float(input('Enter second number: '))\n        # Print without trailing .0 when inputs are integers\n        s = a + b\n        if s.is_integer():\n            print('Sum:', int(s))\n        else:\n            print('Sum:', s)\n    except ValueError:\n        print('Please enter valid numbers.')\n"""
        ),
        'sum_three_numbers': (
            """def sum_three_numbers(a: float, b: float, c: float) -> float:\n    return a + b + c\n\nif __name__ == '__main__':\n    try:\n        a = float(input('Enter first number: '))\n        b = float(input('Enter second number: '))\n        c = float(input('Enter third number: '))\n        s = sum_three_numbers(a, b, c)\n        if s.is_integer():\n            print('Sum:', int(s))\n        else:\n            print('Sum:', s)\n    except ValueError:\n        print('Please enter valid numbers.')\n"""
        ),
        'factorial': (
            """def factorial(n: int) -> int:\n    if n < 0:\n        raise ValueError('n must be non-negative')\n    result = 1\n    for i in range(2, n + 1):\n        result *= i\n    return result\n\nif __name__ == '__main__':\n    try:\n        value = int(input('Enter n: '))\n        print('Factorial:', factorial(value))\n    except ValueError as e:\n        print(e)\n"""
        ),
        'fibonacci': (
            """def fibonacci(n: int) -> list:\n    if n <= 0:\n        return []\n    seq = [0, 1]\n    while len(seq) < n:\n        seq.append(seq[-1] + seq[-2])\n    return seq[:n]\n\nif __name__ == '__main__':\n    try:\n        n = int(input('Enter count: '))\n        print(fibonacci(n))\n    except ValueError:\n        print('Please enter a valid integer.')\n"""
        ),
        'palindrome': (
            """def is_palindrome(s: str) -> bool:\n    t = ''.join(ch.lower() for ch in s if ch.isalnum())\n    return t == t[::-1]\n\nif __name__ == '__main__':\n    s = input('Enter text: ')\n    print('Palindrome' if is_palindrome(s) else 'Not palindrome')\n"""
        ),
        'reverse_string': (
            """def reverse_string(s: str) -> str:\n    return s[::-1]\n\nif __name__ == '__main__':\n    s = input('Enter text: ')\n    print(reverse_string(s))\n"""
        ),
        'sum_array': (
            """def sum_array(nums):\n    return sum(nums)\n\nif __name__ == '__main__':\n    try:\n        raw = input('Enter integers space-separated: ')\n        nums = [int(x) for x in raw.split()]\n        print('Sum:', sum_array(nums))\n    except ValueError:\n        print('Please enter valid integers.')\n"""
        ),
        'bubble_sort': (
            """def bubble_sort(arr):\n    n = len(arr)\n    for i in range(n):\n        for j in range(0, n - i - 1):\n            if arr[j] > arr[j + 1]:\n                arr[j], arr[j + 1] = arr[j + 1], arr[j]\n    return arr\n\nif __name__ == '__main__':\n    try:\n        raw = input('Enter integers space-separated: ')\n        nums = [int(x) for x in raw.split()]\n        print('Sorted:', bubble_sort(nums))\n    except ValueError:\n        print('Please enter valid integers.')\n"""
        ),
        'binary_search': (
            """def binary_search(arr, target):\n    left, right = 0, len(arr) - 1\n    while left <= right:\n        mid = (left + right) // 2\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1\n    return -1\n\nif __name__ == '__main__':\n    try:\n        raw = input('Enter sorted integers space-separated: ')\n        arr = [int(x) for x in raw.split()]\n        t = int(input('Enter target: '))\n        idx = binary_search(arr, t)\n        print('Found at index' if idx != -1 else 'Not found', idx)\n    except ValueError:\n        print('Please enter valid integers.')\n"""
        ),
        'gcd': (
            """def gcd(a: int, b: int) -> int:\n    while b:\n        a, b = b, a % b\n    return abs(a)\n\nif __name__ == '__main__':\n    try:\n        a = int(input('Enter a: '))\n        b = int(input('Enter b: '))\n        print('GCD:', gcd(a, b))\n    except ValueError:\n        print('Please enter valid integers.')\n"""
        ),
        'lcm': (
            """def gcd(a: int, b: int) -> int:\n    while b:\n        a, b = b, a % b\n    return abs(a)\n\ndef lcm(a: int, b: int) -> int:\n    return abs(a * b) // gcd(a, b) if a and b else 0\n\nif __name__ == '__main__':\n    try:\n        a = int(input('Enter a: '))\n        b = int(input('Enter b: '))\n        print('LCM:', lcm(a, b))\n    except ValueError:\n        print('Please enter valid integers.')\n"""
        ),
    }


def java_templates() -> Dict[str, str]:
    return {
        'PrimeNumber': (
            """public class PrimeNumber {\n    public static boolean isPrime(int n) {\n        if (n <= 1) return false;\n        if (n <= 3) return true;\n        if (n % 2 == 0 || n % 3 == 0) return false;\n        for (int i = 5; i * i <= n; i += 6) {\n            if (n % i == 0 || n % (i + 2) == 0) return false;\n        }\n        return true;\n    }\n    public static void main(String[] args) throws java.io.IOException {\n        java.io.BufferedReader br = new java.io.BufferedReader(new java.io.InputStreamReader(System.in));\n        System.out.print("Enter a number: ");\n        int n = Integer.parseInt(br.readLine());\n        System.out.println(isPrime(n) ? "Prime" : "Not prime");\n    }\n}\n"""
        ),
        'SumTwoNumbers': (
            """public class SumTwoNumbers {\n    public static void main(String[] args) throws java.io.IOException {\n        java.io.BufferedReader br = new java.io.BufferedReader(new java.io.InputStreamReader(System.in));\n        System.out.print("Enter first number: ");\n        double a = Double.parseDouble(br.readLine());\n        System.out.print("Enter second number: ");\n        double b = Double.parseDouble(br.readLine());\n        System.out.println("Sum: " + (a + b));\n    }\n}\n"""
        ),
        'SumThreeNumbers': (
            """public class SumThreeNumbers {\n    public static void main(String[] args) throws java.io.IOException {\n        java.io.BufferedReader br = new java.io.BufferedReader(new java.io.InputStreamReader(System.in));\n        System.out.print("Enter first number: ");\n        double a = Double.parseDouble(br.readLine());\n        System.out.print("Enter second number: ");\n        double b = Double.parseDouble(br.readLine());\n        System.out.print("Enter third number: ");\n        double c = Double.parseDouble(br.readLine());\n        System.out.println("Sum: " + (a + b + c));\n    }\n}\n"""
        ),
        'Factorial': (
            """public class Factorial {\n    public static long factorial(int n) {\n        if (n < 0) throw new IllegalArgumentException("n must be non-negative");\n        long result = 1;\n        for (int i = 2; i <= n; i++) result *= i;\n        return result;\n    }\n    public static void main(String[] args) throws java.io.IOException {\n        java.io.BufferedReader br = new java.io.BufferedReader(new java.io.InputStreamReader(System.in));\n        System.out.print("Enter n: ");\n        int n = Integer.parseInt(br.readLine());\n        System.out.println("Factorial: " + factorial(n));\n    }\n}\n"""
        ),
        'Fibonacci': (
            """public class Fibonacci {\n    public static int[] fibonacci(int n) {\n        if (n <= 0) return new int[0];\n        int[] seq = new int[Math.max(n, 2)];\n        seq[0] = 0; seq[1] = 1;\n        for (int i = 2; i < n; i++) seq[i] = seq[i-1] + seq[i-2];\n        int[] res = new int[n];\n        System.arraycopy(seq, 0, res, 0, n);\n        return res;\n    }\n    public static void main(String[] args) throws java.io.IOException {\n        java.io.BufferedReader br = new java.io.BufferedReader(new java.io.InputStreamReader(System.in));\n        System.out.print("Enter count: ");\n        int n = Integer.parseInt(br.readLine());\n        int[] arr = fibonacci(n);\n        for (int v : arr) System.out.print(v + " ");\n        System.out.println();\n    }\n}\n"""
        ),
        'Palindrome': (
            """public class Palindrome {\n    public static boolean isPalindrome(String s) {\n        String t = s.replaceAll("[^A-Za-z0-9]", "").toLowerCase();\n        return new StringBuilder(t).reverse().toString().equals(t);\n    }\n    public static void main(String[] args) throws java.io.IOException {\n        java.io.BufferedReader br = new java.io.BufferedReader(new java.io.InputStreamReader(System.in));\n        System.out.print("Enter text: ");\n        String s = br.readLine();\n        System.out.println(isPalindrome(s) ? "Palindrome" : "Not palindrome");\n    }\n}\n"""
        ),
        'ReverseString': (
            """public class ReverseString {\n    public static String reverse(String s) {\n        return new StringBuilder(s).reverse().toString();\n    }\n    public static void main(String[] args) throws java.io.IOException {\n        java.io.BufferedReader br = new java.io.BufferedReader(new java.io.InputStreamReader(System.in));\n        System.out.print("Enter text: ");\n        String s = br.readLine();\n        System.out.println(reverse(s));\n    }\n}\n"""
        ),
        'BubbleSort': (
            """public class BubbleSort {\n    public static void bubbleSort(int[] arr) {\n        int n = arr.length;\n        for (int i = 0; i < n; i++) {\n            for (int j = 0; j < n - i - 1; j++) {\n                if (arr[j] > arr[j + 1]) {\n                    int tmp = arr[j];\n                    arr[j] = arr[j + 1];\n                    arr[j + 1] = tmp;\n                }\n            }\n        }\n    }\n    public static void main(String[] args) throws java.io.IOException {\n        java.io.BufferedReader br = new java.io.BufferedReader(new java.io.InputStreamReader(System.in));\n        System.out.print("Enter integers space-separated: ");\n        String[] parts = br.readLine().trim().split("\\\\s+");\n        int[] arr = new int[parts.length];\n        for (int i = 0; i < parts.length; i++) arr[i] = Integer.parseInt(parts[i]);\n        bubbleSort(arr);\n        for (int v : arr) System.out.print(v + " ");\n        System.out.println();\n    }\n}\n"""
        ),
    }


def c_templates() -> Dict[str, str]:
    return {
        'prime_number': (
            """#include <stdio.h>\n#include <stdbool.h>\n\nbool is_prime(int n) {\n    if (n <= 1) return false;\n    if (n <= 3) return true;\n    if (n % 2 == 0 || n % 3 == 0) return false;\n    for (int i = 5; i * i <= n; i += 6) {\n        if (n % i == 0 || n % (i + 2) == 0) return false;\n    }\n    return true;\n}\n\nint main(void) {\n    int n;\n    printf("Enter a number: ");\n    if (scanf("%d", &n) != 1) return 0;\n    printf(is_prime(n) ? "Prime\n" : "Not prime\n");\n    return 0;\n}\n"""
        ),
        'sum_two_numbers': (
            """#include <stdio.h>\n\nint main(void) {\n    double a, b;\n    printf("Enter first number: ");\n    if (scanf("%lf", &a) != 1) return 0;\n    printf("Enter second number: ");\n    if (scanf("%lf", &b) != 1) return 0;\n    printf("Sum: %.2f\\n", a + b);\n    return 0;\n}\n"""
        ),
        'sum_three_numbers': (
            """#include <stdio.h>\n\nint main(void) {\n    double a, b, c;\n    printf("Enter three numbers: ");\n    if (scanf("%lf %lf %lf", &a, &b, &c) != 3) return 0;\n    printf("Sum: %.2f\\n", a + b + c);\n    return 0;\n}\n"""
        ),
        'factorial': (
            """#include <stdio.h>\n\nunsigned long long factorial(int n) {\n    if (n < 0) return 0;\n    unsigned long long res = 1;\n    for (int i = 2; i <= n; ++i) res *= i;\n    return res;\n}\n\nint main(void) {\n    int n;\n    printf("Enter n: ");\n    if (scanf("%d", &n) != 1) return 0;\n    printf("Factorial: %llu\n", factorial(n));\n    return 0;\n}\n"""
        ),
    }


def cpp_templates() -> Dict[str, str]:
    return {
        'prime_number': (
            """#include <iostream>\n#include <cmath>\nusing namespace std;\n\nbool isPrime(int n) {\n    if (n <= 1) return false;\n    if (n <= 3) return true;\n    if (n % 2 == 0 || n % 3 == 0) return false;\n    for (int i = 5; i * i <= n; i += 6) {\n        if (n % i == 0 || n % (i + 2) == 0) return false;\n    }\n    return true;\n}\n\nint main() {\n    int n;\n    cout << "Enter a number: ";\n    if (!(cin >> n)) return 0;\n    cout << (isPrime(n) ? "Prime" : "Not prime") << endl;\n    return 0;\n}\n"""
        ),
        'sum_two_numbers': (
            """#include <iostream>\nusing namespace std;\n\nint main() {\n    double a, b;\n    cout << "Enter first number: ";\n    if (!(cin >> a)) return 0;\n    cout << "Enter second number: ";\n    if (!(cin >> b)) return 0;\n    cout << "Sum: " << (a + b) << endl;\n    return 0;\n}\n"""
        ),
        'sum_three_numbers': (
            """#include <iostream>\nusing namespace std;\n\nint main() {\n    double a, b, c;\n    cout << "Enter first number: ";\n    if (!(cin >> a)) return 0;\n    cout << "Enter second number: ";\n    if (!(cin >> b)) return 0;\n    cout << "Enter third number: ";\n    if (!(cin >> c)) return 0;\n    cout << "Sum: " << (a + b + c) << endl;\n    return 0;\n}\n"""
        ),
        'factorial': (
            """#include <iostream>\nusing namespace std;\n\nunsigned long long factorial(int n) {\n    if (n < 0) return 0;\n    unsigned long long res = 1;\n    for (int i = 2; i <= n; ++i) res *= i;\n    return res;\n}\n\nint main() {\n    int n;\n    cout << "Enter n: ";\n    if (!(cin >> n)) return 0;\n    cout << "Factorial: " << factorial(n) << endl;\n    return 0;\n}\n"""
        ),
        'bubble_sort': (
            """#include <iostream>\n#include <vector>\nusing namespace std;\n\nvoid bubbleSort(vector<int>& arr) {\n    int n = (int)arr.size();\n    for (int i = 0; i < n; ++i) {\n        for (int j = 0; j < n - i - 1; ++j) {\n            if (arr[j] > arr[j + 1]) {\n                int tmp = arr[j];\n                arr[j] = arr[j + 1];\n                arr[j + 1] = tmp;\n            }\n        }\n    }\n}\n\nint main() {\n    cout << "Enter integers space-separated: ";\n    vector<int> arr;\n    int x;\n    while (cin >> x) arr.push_back(x);\n    bubbleSort(arr);\n    for (int v : arr) cout << v << ' ';\n    cout << endl;\n    return 0;\n}\n"""
        ),
    }


def select_template(language: str, topic: str) -> Optional[Tuple[str, str]]:
    """Return (file_stem, code) for language/topic or None."""
    language = language.lower()
    topic = topic.lower()
    if language == 'python':
        templates = py_templates()
        code = templates.get(topic)
        if code:
            stem = {
                'prime_number': 'prime_number',
                'sum_three_numbers': 'sum_three_numbers',
                'sum_two_numbers': 'sum_two_numbers',
                'factorial': 'factorial',
                'fibonacci': 'fibonacci',
                'palindrome': 'palindrome',
                'reverse_string': 'reverse_string',
                'sum_array': 'sum_array',
                'bubble_sort': 'bubble_sort',
                'binary_search': 'binary_search',
                'gcd': 'gcd',
                'lcm': 'lcm',
            }.get(topic, topic)
            return stem, code
    elif language == 'java':
        templates = java_templates()
        # Map topic to class name
        topic_to_class = {
            'prime_number': 'PrimeNumber',
            'sum_two_numbers': 'SumTwoNumbers',
            'sum_three_numbers': 'SumThreeNumbers',
            'factorial': 'Factorial',
            'fibonacci': 'Fibonacci',
            'palindrome': 'Palindrome',
            'reverse_string': 'ReverseString',
            'bubble_sort': 'BubbleSort',
        }
        class_name = topic_to_class.get(topic)
        if class_name and class_name in templates:
            return class_name, templates[class_name]
    elif language == 'c':
        templates = c_templates()
        code = templates.get(topic)
        if code:
            stem = topic
            return stem, code
    elif language == 'cpp':
        templates = cpp_templates()
        code = templates.get(topic)
        if code:
            stem = topic
            return stem, code
    return None


def ensure_python_syntax(code: str) -> Optional[str]:
    """Return error message if invalid, else None."""
    try:
        ast.parse(code)
        return None
    except SyntaxError as e:
        return f"Python syntax error: {e}"


def save_program(base_dir: str, file_stem: str, language: str, code: str) -> str:
    ext = LANGUAGE_EXTENSIONS[language]
    file_name = f"{file_stem}{ext}"
    os.makedirs(base_dir, exist_ok=True)
    full_path = os.path.join(base_dir, file_name)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(code)
    return full_path


def generate_program(user_text: str, language: Optional[str], topic: Optional[str], base_dir: str) -> Dict:
    """Generate code + save file. Returns dict with result info."""
    # Infer language/topic if missing
    lang = language or normalize_language(user_text) or 'python'
    top = topic or fuzzy_topic(user_text)

    if not top:
        return {
            'ok': False,
            'message': (
                "❌ Could not detect the program topic.\n"
                "Try specifying: prime, factorial, fibonacci, palindrome, reverse string, sum array, bubble sort, binary search, gcd, lcm."
            )
        }

    selection = select_template(lang, top)
    if not selection:
        return {
            'ok': False,
            'message': f"❌ Templates for '{lang}' and topic '{top}' are not available."
        }

    stem, code = selection

    # Quick syntax check for Python
    if lang == 'python':
        err = ensure_python_syntax(code)
        if err:
            return {'ok': False, 'message': f"❌ {err}"}

    path = save_program(base_dir, stem, lang, code)

    # Compose display message
    header = (
        f"✅ Program generated successfully!\n"
        f"• Language: {lang.capitalize()}\n"
        f"• Topic: {top.replace('_', ' ').title()}\n"
        f"• Saved Path: {path}\n\n"
        f"📄 Source Code:\n"
        + "=" * 50 + "\n"
    )
    return {
        'ok': True,
        'message': header + code
    }
