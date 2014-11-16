
def saveSegment(word_name, raw, raw_data, start, end):
    import wave

    #raw = wave.open('inputFile.wav','r')
    frameRate = raw.getframerate()
    nChannels = raw.getnchannels()
    sampWidth = raw.getsampwidth()

    output_file = "temp/" + word_name + ".wav"

    chunk_data = raw_data[start:end+1]

    chunkAudio = wave.open(output_file, "w")
    chunkAudio.setnchannels(nChannels)
    chunkAudio.setsampwidth(sampWidth)
    chunkAudio.setframerate(frameRate)

    for chunk in chunk_data:
        chunkAudio.writeframes(chunk)

    chunkAudio.close()
