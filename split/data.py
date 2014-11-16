
def saveSegment(file_name, raw, raw_data, start, end):
    import wave

    #raw = wave.open('inputFile.wav','r')
    frameRate = raw.getframerate()
    nChannels = raw.getnchannels()
    sampWidth = raw.getsampwidth()

    chunk_data = raw_data[start:end+1]

    chunkAudio = wave.open(file_name, "w")
    chunkAudio.setnchannels(nChannels)
    chunkAudio.setsampwidth(sampWidth)
    chunkAudio.setframerate(frameRate)

    for chunk in chunk_data:
        chunkAudio.writeframes(chunk)

    chunkAudio.close()
