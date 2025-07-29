#include <libavformat/avformat.h>
#include <libavutil/frame.h>

struct enc_encoder {
    AVFrame *aframe;
};

int Test_initialize_codec() {
    struct enc_encoder enc;
    int ret;

    // Initialize network components
    avformat_network_init();

    // Allocate memory for AVFrame
    AVFrame *allocated_frame = av_frame_alloc();
    enc.aframe = allocated_frame;

    // Check if allocation was successful
    if (!enc.aframe) {
        return -1;
    }

    // Clean up
    av_frame_free(&enc.aframe);

    return 0;
}

int main() {
    return Test_initialize_codec();
}