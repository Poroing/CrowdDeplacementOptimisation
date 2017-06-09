#:/bin/bash
cat rapport.tex | egrep '^[^%\]' | egrep -o '([[:space:]]|^)[^[:space:]{}()$]+' | wc
