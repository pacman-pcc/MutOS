#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MEM_SIZE 30000
#define CALL_STACK_SIZE 1024

typedef struct {
    int start_pos;
    int is_defined;
} Function;

unsigned char memory[MEM_SIZE] = {0};
int ptr = 0;

Function functions[26];
int call_stack[CALL_STACK_SIZE];
int call_stack_ptr = 0;

void pre_parse_functions(const char *code) {
    int i = 0;
    while (code[i] != '\0') {
        if (code[i] == 'f' && code[i+1] >= 'a' && code[i+1] <= 'z' && code[i+2] == '(' && code[i+3] == ')' && code[i+4] == '{') {
            int func_idx = code[i+1] - 'a';
            functions[func_idx].start_pos = i + 5;
            functions[func_idx].is_defined = 1;

            i += 5;
            int braces = 1;
            while (braces > 0 && code[i] != '\0') {
                if (code[i] == '{') braces++;
                if (code[i] == '}') braces--;
                i++;
            }
        } else {
            i++;
        }
    }
}

void execute_mbf(const char *code) {
    int ip = 0;
    int loop_braces = 0;

    pre_parse_functions(code);

    while (code[ip] != '\0') {
        char cmd = code[ip];

        if (cmd == 'f' && code[ip+1] >= 'a' && code[ip+1] <= 'z' && code[ip+2] == '(' && code[ip+3] == ')' && code[ip+4] == '{') {
            ip += 5;
            int braces = 1;
            while (braces > 0 && code[ip] != '\0') {
                if (code[ip] == '{') braces++;
                if (code[ip] == '}') braces--;
                ip++;
            }
            continue;
        }

        if (cmd == 'f' && code[ip+1] >= 'a' && code[ip+1] <= 'z' && code[ip+2] == '(' && code[ip+3] == ')') {
            int func_idx = code[ip+1] - 'a';
            if (functions[func_idx].is_defined) {
                if (call_stack_ptr == CALL_STACK_SIZE) {
                    fprintf(stderr, "MBF Error: Call stack overflow!\n");
                    exit(1);
                }
                call_stack[call_stack_ptr++] = ip + 4;
                ip = functions[func_idx].start_pos;
                continue;
            } else {
                fprintf(stderr, "MBF Runtime Error: Function f%c() is not defined!\n", code[ip+1]);
                exit(1);
            }
        }

        switch (cmd) {
            case '>': ptr = (ptr + 1) % MEM_SIZE; break;
            case '<': ptr = (ptr - 1 + MEM_SIZE) % MEM_SIZE; break;
            case '+': memory[ptr]++; break;
            case '-': memory[ptr]--; break;
            case '.': putchar(memory[ptr]); fflush(stdout); break;
            case ',': memory[ptr] = getchar(); break;

            case '[':
                if (memory[ptr] == 0) {
                    loop_braces = 1;
                    while (loop_braces > 0) {
                        ip++;
                        if (code[ip] == '\0') { fprintf(stderr, "MBF Error: Unmatched '['\n"); exit(1); }
                        if (code[ip] == '[') loop_braces++;
                        if (code[ip] == ']') loop_braces--;
                    }
                }
                break;
            case ']':
                if (memory[ptr] != 0) {
                    loop_braces = 1;
                    while (loop_braces > 0) {
                        ip--;
                        if (ip < 0) { fprintf(stderr, "MBF Error: Unmatched ']'\n"); exit(1); }
                        if (code[ip] == ']') loop_braces++;
                        if (code[ip] == '[') loop_braces--;
                    }
                }
                break;

            case '}':
                if (call_stack_ptr > 0) {
                    ip = call_stack[--call_stack_ptr];
                    continue;
                }
                break;

            case '#':
                printf("%d", memory[ptr]);
                fflush(stdout);
                break;
            case '?':
                putchar('\n');
                fflush(stdout);
                break;
            case '!':
                exit(0);
        }
        ip++;
    }
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <file.mbf>\n", argv[0]);
        return 1;
    }

    FILE *file = fopen(argv[1], "r");
    if (!file) {
        fprintf(stderr, "Error: Could not open file %s\n", argv[1]);
        return 1;
    }

    fseek(file, 0, SEEK_END);
    long file_size = ftell(file);
    fseek(file, 0, SEEK_SET);

    char *code = malloc(file_size + 1);
    if (!code) {
        fprintf(stderr, "Error: Memory allocation failed\n");
        fclose(file);
        return 1;
    }

    size_t read_size = fread(code, 1, file_size, file);
    code[read_size] = '\0';
    fclose(file);

    execute_mbf(code);

    free(code);
    return 0;
}
