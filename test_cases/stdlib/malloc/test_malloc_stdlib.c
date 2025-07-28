#include <stdlib.h>
#include <stdio.h>
#include <assert.h>

/**
 * Test case for malloc function
 * 
 * This test case demonstrates basic memory allocation using malloc
 * and proper error handling.
 */

int test_malloc_basic_allocation() {
    // Test basic memory allocation
    void* ptr = malloc(100);
    if (ptr == NULL) {
        fprintf(stderr, "malloc failed to allocate memory\n");
        return 1;
    }
    
    // Verify the pointer is not null
    assert(ptr != NULL);
    
    // Test writing to allocated memory
    char* char_ptr = (char*)ptr;
    for (int i = 0; i < 100; i++) {
        char_ptr[i] = 'A' + (i % 26);
    }
    
    // Test reading from allocated memory
    for (int i = 0; i < 100; i++) {
        assert(char_ptr[i] == 'A' + (i % 26));
    }
    
    // Free the allocated memory
    free(ptr);
    
    printf("Basic malloc test passed\n");
    return 0;
}

int test_malloc_zero_size() {
    // Test malloc with zero size
    void* ptr = malloc(0);
    // malloc(0) may return NULL or a valid pointer
    // We just need to ensure we don't crash
    if (ptr != NULL) {
        free(ptr);
    }
    
    printf("Zero size malloc test passed\n");
    return 0;
}

int test_malloc_large_allocation() {
    // Test large memory allocation
    size_t large_size = 1024 * 1024; // 1MB
    void* ptr = malloc(large_size);
    
    if (ptr == NULL) {
        fprintf(stderr, "malloc failed to allocate large memory block\n");
        return 1;
    }
    
    assert(ptr != NULL);
    
    // Test writing to large allocated memory
    char* char_ptr = (char*)ptr;
    for (size_t i = 0; i < large_size; i += 1024) {
        char_ptr[i] = 'X';
    }
    
    free(ptr);
    
    printf("Large malloc test passed\n");
    return 0;
}

int main() {
    int result = 0;
    
    result += test_malloc_basic_allocation();
    result += test_malloc_zero_size();
    result += test_malloc_large_allocation();
    
    if (result == 0) {
        printf("All malloc tests passed!\n");
    } else {
        printf("Some malloc tests failed!\n");
    }
    
    return result;
} 