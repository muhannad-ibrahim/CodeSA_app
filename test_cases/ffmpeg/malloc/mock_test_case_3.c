#include <stdlib.h>
#include <stdio.h>

void test_malloc_3() {
    void* ptr = malloc(1024);
    if (ptr != NULL) {
        printf("Memory allocated successfully\n");
        free(ptr);
        printf("Memory freed successfully\n");
    } else {
        printf("Memory allocation failed\n");
    }
}

int main() {
    test_malloc_3();
    return 0;
}