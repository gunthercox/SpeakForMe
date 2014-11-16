from array import array
import pyaudio
import sys
import wave

CHUNK_SIZE = 1024

file = wave.open(sys.argv[1], "rb")

out_file = wave.open(sys.argv[2], "wb")

#pa = pyaudio.PyAudio()

#stream_format = pa.get_format_from_width(file.getsampwidth())
stream_channels = file.getnchannels()
stream_rate = file.getframerate()

out_file.setnchannels(stream_channels)
out_file.setframerate(stream_rate)
out_file.setsampwidth(2)

#out_device = pa.get_default_output_device_info()

'''stream = pa.open(
    format=stream_format,
    channels=stream_channels,
    rate=stream_rate,
    output=True,
    output_device_index=out_device["index"],
)'''

data = file.readframes(CHUNK_SIZE)

all_data = []
raw_data = []

while data != "":
    int_data = array("h", data)

    all_data.append(int_data)
    raw_data.append(data)

    data = file.readframes(CHUNK_SIZE)

# 100000 because there will never be an amplitude that high
all_min = 100000
all_max = 0
all_total = 0

for data in all_data:
    max_data = max(data)

    if max_data < all_min:
        all_min = max_data

    if max_data > all_max:
        all_max = max_data

    all_total += max_data

all_avg = all_total / len(all_data)

#all_avg *= 2

print all_min, all_max, all_avg

start_silence = 0
in_silence = True

words = 0

silence_count = 0

for idx, data in enumerate(all_data):
    max_data = max(data)
    raw = raw_data[idx]

    out_file.writeframes(raw)

    if max_data > all_avg and not start_silence:
        start_silence = idx

    if max_data > all_avg and in_silence:
        if silence_count > 1:
            in_silence = False
            print "Start word", silence_count
            silence_count = 0

    if max_data < all_avg and in_silence:
        silence_count += 1

    if max_data < all_avg and not in_silence:
        in_silence = True
        words += 1
        print "End word"

print start_silence, words

#stream.stop_stream()
#stream.close()

file.close()
out_file.close()