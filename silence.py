from split.data import saveSegment

from array import array

import json
import pyaudio
import sys
import wave

# Files are stored in directories with the pattern:
# /data/{{ voice_name }}/{{ sound }}/{{ sound }}.wav


phoneme_swap = {
    "IH": "I",
    "UW": "U"
}

phoneme_dictionary = json.load(open("data/cmu_edited.txt"))

def get_phonemes(word):
    word = word.upper()
    return phoneme_dictionary[word]

def get_phoneme_sum(phonemes):
    total_phoneme = ""

    for phoneme in phonemes:
        if phoneme in phoneme_swap:
            phoneme = phoneme_swap[phoneme]

        total_phoneme += phoneme

    return len(total_phoneme)

sentence = "Create ongoing communication and support your teachers by sending them links to view their observations and evaluations".split()
sentence_index = -1

CHUNK_SIZE = 256

file = wave.open(sys.argv[1], "rb")

out_file = wave.open(sys.argv[2], "wb")

stream_channels = file.getnchannels()
stream_rate = file.getframerate()

out_file.setnchannels(stream_channels)
out_file.setframerate(stream_rate)
out_file.setsampwidth(2)

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

all_avg = all_max * 0.1

print all_min, all_max, all_avg

start_silence = 0
in_silence = True

words = 0

silence_count = 0

for idx, data in enumerate(all_data):
    max_data = max(data)
    raw = raw_data[idx]

    # Remove the beginning silence
    if max_data > all_avg and not start_silence:
        start_silence = idx

        silence_data = all_data[0:idx]
        silence_total = 0

        for data in silence_data:
            silence_total = 0

            for d in data:
                silence_total += abs(d)

            silence_total = silence_total / len(data)        

    if max_data > all_avg and in_silence:
        if silence_count > 1:
            in_silence = False
            sentence_index += 1
            print "Start word", silence_count
            silence_count = 0

            start_idx = idx
            #print ">>>>", start_idx

    # Increment the silence count if it is still silent
    if max_data < all_avg and in_silence:
        silence_count += 1

    if max_data < all_avg and not in_silence:

        end_idx = idx
        word = sentence[sentence_index]

        phonemes = get_phonemes(word)

        phoneme_sum = get_phoneme_sum(phonemes)

        if end_idx - start_idx < phoneme_sum * 7:
            continue

        in_silence = True
        words += 1
        print "End word", word, phoneme_sum * 7


        print ">>>>>>>>>", end_idx, end_idx - start_idx

        smurf_data = raw_data[start_idx:end_idx+1]
        for data in smurf_data:
            out_file.writeframes(data)

        saveSegment("test"+str(idx), file, raw_data, start_idx, end_idx)

print start_silence, words

file.close()
out_file.close()
