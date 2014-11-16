from __future__ import division

from .data import saveSegment

from array import array

import json
import os
import sys
import wave
import subprocess

# Files are stored in directories with the pattern:
# /data/{{ voice_name }}/{{ sound }}/{{ sound }}.wav


phoneme_swap = {
    "IH": "I",
    "UW": "U",
    "Z": "ZZZ"
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

def convert_upload(file_name, sentence, user):
    sentence = sentence.lower().strip().split()
    sentence_index = -1

    CHUNK_SIZE = 256

    file = wave.open(file_name, "rb")

    stream_channels = file.getnchannels()
    stream_rate = file.getframerate()

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

                silence_count = 0

                start_idx = idx

        # Increment the silence count if it is still silent
        if max_data < all_avg and in_silence:
            silence_count += 1

        if max_data < all_avg and not in_silence:

            end_idx = idx
	    if sentence_index ==  len(sentence):
   	      break
            word = sentence[sentence_index]

            phonemes = get_phonemes(word)

            phoneme_sum = get_phoneme_sum(phonemes)

            if len(word) < 5:
                if len(word) == 2:
                    phoneme_sum = 1
                if len(word) == 3:
                    phoneme_sum = 3

            if word.endswith("ing"):
                phoneme_sum -= 2

            if word.endswith("s"):
                phoneme_sum += 2

            if word.startswith("the"):
                phoneme_sum -= 3

            if end_idx - start_idx < phoneme_sum * 7:
                continue

            in_silence = True
            words += 1

            if len(word) < 4:
                continue

            saveSegment(("/tmp/%s.wav" % word), file, raw_data, start_idx, end_idx)
            subprocess.call(["sox", ("/tmp/%s.wav" % word), "%s/uploads/%s/words/%s.wav" % (os.getcwd(), user, word, ), "silence", "1", "0.1", "1%", "reverse", "silence", "1", "0.1", "2.5%", "reverse"])

            word_file = wave.open("uploads/%s/words/%s.wav" % (user, word), "rb")
            data = word_file.readframes(CHUNK_SIZE)
            word_data = []

            while data != "":
                word_data.append(data)
                data = word_file.readframes(CHUNK_SIZE)

            phoneme_sum = get_phoneme_sum(phonemes)

            word_length = len(word_data)

            phoneme_start = 0

	    os.makedirs("uploads/%s/phonemes/%s" % (user, word))

            for phoneme in phonemes:
                ratio = 1 / len(phonemes)
		print phoneme + " --> " + word
                frame_count = int(ratio * word_length)
	   	filepath = "uploads/%s/phonemes/%s/%s" % (user, word, phoneme)
	   	print filepath
                saveSegment(filepath, file, word_data, phoneme_start, phoneme_start + frame_count)
                phoneme_start += frame_count

    file.close()
