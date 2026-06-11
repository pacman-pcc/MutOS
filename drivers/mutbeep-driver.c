#include <stdio.h>
#include <string.h>
#include <math.h>
#include <unistd.h>

void play_tone(double frequency, double duration) {
	FILE *aplay = popen("aplay -q -r 8000 -f U8", "w");
	if (!aplay) return;

	int sample_rate = 8000;
	int total_samples = (int)(sample_rate * duration);

	for (int i = 0; i < total_samples; i++) {
		double time = (double)i / sample_rate;
		double sine = sin(2.0 * M_PI * frequency * time);
		unsigned char sample = (unsigned char)((sine + 1.0) * 127.5);
		fputc(sample, aplay);
	}
	pclose(aplay);
}

int main(int argc, char *argv[]) {
	if (argc < 2) return 0;

	if (strcmp(argv[1], "boot") == 0) {
		play_tone(800.0, 0.15);
	}
	else if (strcmp(argv[1], "error") == 0) {
		play_tone(400.0, 0.1);
		usleep(50000);
		play_tone(400.0, 0.1);
	}
	return 0;
}
