#include <libavformat/avformat.h>
#include <libavutil/avutil.h>
#include <stdbool.h>

// Define a structure to hold media information
typedef struct {
    AVFormatContext *fmt;
    bool is_local_file;
} mp_media_t;

int Test_seek_to(mp_media_t *m, int64_t pos) {
    // Ensure the media format context is valid
    if (!m || !m->fmt || m->fmt->nb_streams < 1) {
        return -1; // Invalid input
    }

    AVStream *stream = m->fmt->streams[0];
    int64_t seek_pos = pos;
    int seek_flags = 0; // Initialize seek flags, can be set as needed

    // Check if the duration is not available
    bool is_duration_unknown = (m->fmt->duration == AV_NOPTS_VALUE);
    if (!is_duration_unknown) {
        // Rescale the seek position to the stream's time base
        seek_pos = av_rescale_q(seek_pos, AV_TIME_BASE_Q, stream->time_base);

        // Determine the seek target based on the seek flags
        int64_t seek_target =
            (seek_flags == AVSEEK_FLAG_BACKWARD) ? 0 : seek_pos;

        // If the media is a local file, perform the seek
        if (m->is_local_file) {
            if (av_seek_frame(m->fmt, 0, seek_target, seek_flags) < 0) {
                return -1; // Seek failed
            }
        }
    }
    return 0; // Success
}

int main() {
    // Initialize FFmpeg libraries
    av_register_all();
    avformat_network_init();

    // Create and initialize media structure
    mp_media_t media;
    media.fmt = avformat_alloc_context();
    media.is_local_file = true; // Assume it's a local file for this test

    // Open a media file (replace "input.mp4" with an actual file path)
    if (avformat_open_input(&media.fmt, "input.mp4", NULL, NULL) != 0) {
        return -1; // Failed to open file
    }

    // Retrieve stream information
    if (avformat_find_stream_info(media.fmt, NULL) < 0) {
        avformat_close_input(&media.fmt);
        return -1; // Failed to retrieve stream info
    }

    // Test seeking to a position (e.g., 10 seconds)
    int64_t seek_position = 10 * AV_TIME_BASE;
    int result = Test_seek_to(&media, seek_position);

    // Clean up
    avformat_close_input(&media.fmt);
    avformat_network_deinit();

    return result;
}