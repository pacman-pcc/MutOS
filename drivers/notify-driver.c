#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

void send_notify(const char *text) {
	pid_t pid = fork();

	if (pid < 0) {
		perror("Error fork.");
		exit(1);
	}

	if (pid == 0) {
		execlp("notify-send", "notify-send", "MutOS", text, NULL);
		perror("Error execlp");
		exit(1);
	} else {
		int status;
		waitpid(pid, &status, 0);
	}
}

int main(void) {
	const char *messages[] = {
		"Welcome to MutOS ++"
	};

	send_notify(messages[0]);

	return 0;
}
