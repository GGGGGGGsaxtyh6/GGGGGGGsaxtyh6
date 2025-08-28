var prompts = {
  python: `# take in the number
n = input()

# calculate answer


# print answer
print(n)
`,

  c: `// take in the number
#include <stdio.h>

int main() {
    int n;

    // calculate answer


    // print answer
    printf("%d", n);

    return 0;
}
`,

  cpp: `// take in the number
#include <iostream>
using namespace std;

int main() {
    int n;

    // calculate answer


    // print answer
    cout << n;

    return 0;
}
`,

  rust: `// take in the number
use std::io;

fn main() {
    let mut n = String::new();

    // calculate answer


    // print answer
    println!("{}", n);
}
`
};
