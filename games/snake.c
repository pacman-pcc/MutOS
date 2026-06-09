#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <termios.h>
#include <sys/select.h>
#include <time.h>

#define WIDTH 20
#define HEIGHT 20
#define MAX_TAIL 400

int gameOver;
int x, y, fruitX, fruitY, score;
int tailX[MAX_TAIL], tailY[MAX_TAIL];
int nTail;
enum eDirecton { STOP = 0, LEFT, RIGHT, UP, DOWN };
enum eDirecton dir;
struct termios orig_termios;

void disableRawMode() {
    tcsetattr(STDIN_FILENO, TCSAFLUSH, &orig_termios);
    printf("\033[?25h\033[0m\n");
}

void enableRawMode() {
    tcgetattr(STDIN_FILENO, &orig_termios);
    atexit(disableRawMode);
    struct termios raw = orig_termios;
    raw.c_lflag &= ~(ECHO | ICANON);
    tcsetattr(STDIN_FILENO, TCSAFLUSH, &raw);
    printf("\033[?25l");
}

int kbhit() {
    struct timeval tv = {0L, 0L};
    fd_set fds;
    FD_ZERO(&fds);
    FD_SET(STDIN_FILENO, &fds);
    return select(STDIN_FILENO + 1, &fds, NULL, NULL, &tv);
}

void GenerateFruit() {
    int valid = 0;
    while (!valid) {
        fruitX = rand() % WIDTH;
        fruitY = rand() % HEIGHT;
        valid = 1;

        if (fruitY == y && (fruitX == x || fruitX == x + 1 || fruitX == x + 2)) {
            valid = 0;
            continue;
        }

        for (int i = 0; i < nTail; i++) {
            if (tailX[i] == fruitX && tailY[i] == fruitY) {
                valid = 0;
                break;
            }
        }
    }
}

void Setup() {
    srand(time(NULL));
    gameOver = 0;
    dir = STOP;
    x = WIDTH / 2;
    y = HEIGHT / 2;
    score = 0;
    nTail = 0;
    GenerateFruit();
}

void Draw() {
    printf("\033[H");

    for (int i = 0; i < WIDTH + 4; i++) printf("#");
    printf("\n");

    for (int i = 0; i < HEIGHT; i++) {
        printf("# ");
        for (int j = 0; j < WIDTH; j++) {
            if (i == y && j == x) {
                printf("^-^");
                j += 2;
            } else if (i == fruitY && j == fruitX) {
                printf("$");
            } else {
                int print = 0;
                for (int k = 0; k < nTail; k++) {
                    if (tailX[k] == j && tailY[k] == i) {
                        printf("o");
                        print = 1;
                        break;
                    }
                }
                if (!print) printf(" ");
            }
        }
        printf(" #\n");
    }

    for (int i = 0; i < WIDTH + 4; i++) printf("#");
    printf("\n");
    printf("Score: %d\n", score);
}

void Input() {
    if (kbhit()) {
        char ch;
        if (read(STDIN_FILENO, &ch, 1) > 0) {
            switch (ch) {
                case 'a': if (dir != RIGHT) dir = LEFT; break;
                case 'd': if (dir != LEFT) dir = RIGHT; break;
                case 'w': if (dir != DOWN) dir = UP; break;
                case 's': if (dir != UP) dir = DOWN; break;
                case 'x': gameOver = 1; break;
            }
        }
    }
}

void Logic() {
    if (dir == STOP) return;

    int prevX = tailX[0];
    int prevY = tailY[0];
    int prev2X, prev2Y;
    tailX[0] = x;
    tailY[0] = y;
    for (int i = 1; i < nTail; i++) {
        prev2X = tailX[i];
        prev2Y = tailY[i];
        tailX[i] = prevX;
        tailY[i] = prevY;
        prevX = prev2X;
        prevY = prev2Y;
    }

    switch (dir) {
        case LEFT:  x--; break;
        case RIGHT: x++; break;
        case UP:    y--; break;
        case DOWN:  y++; break;
        default: break;
    }

    if (x >= WIDTH) x = 0; else if (x < 0) x = WIDTH - 1;
    if (y >= HEIGHT) y = 0; else if (y < 0) y = HEIGHT - 1;

    for (int i = 0; i < nTail; i++) {
        if (tailX[i] == x && tailY[i] == y) gameOver = 1;
    }

    if (y == fruitY && (x == fruitX || (dir == RIGHT && (x + 1 == fruitX || x + 2 == fruitX)))) {
        score += 10;
        if (nTail < MAX_TAIL) {
            nTail++;
        }
        GenerateFruit();
    }
}

int main() {
    enableRawMode();
    printf("\033[2J");
    Setup();
    while (!gameOver) {
        Draw();
        Input();
        Logic();
        usleep(100000);
    }
    printf("Game Over! Final Score: %d\n", score);
    return 0;
}
