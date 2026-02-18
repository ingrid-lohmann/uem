# INGRID LOHMANN
# RA 117698

import struct
import sys
import os

HEADER_SIZE = 4
RECORD_SIZE_FIELD = 2
MIN_UNUSED_SPACE = 10


def readHeader(file):
    file.seek(0)
    header = file.read(HEADER_SIZE)
    return struct.unpack('I', header)[0]


def writeHeader(file, value):
    file.seek(0)
    file.write(struct.pack('I', value))


def readRecord(file):
    sizeData = file.read(RECORD_SIZE_FIELD)
    if not sizeData or len(sizeData) < RECORD_SIZE_FIELD:
        return None, None
    recordSize = struct.unpack('H', sizeData)[0]
    recordData = file.read(recordSize)
    return recordSize, recordData


def writeRecord(file, recordData):
    recordSize = len(recordData)
    file.write(struct.pack('H', recordSize))
    file.write(recordData)


def searchById(file, searchId):
    file.seek(HEADER_SIZE)
    searchIdEncoded = searchId.encode('utf-8')
    while True:
        pos = file.tell()
        recordSize, recordData = readRecord(file)
        if not recordData:
            return None, None
        try:
            if recordData[:len(searchIdEncoded)] == searchIdEncoded:
                return pos, recordData
        except UnicodeDecodeError:
            pass
    return None, None


def insertGame(file, gameData):
    header = readHeader(file)
    gameDataEncoded = gameData.encode('utf-8')
    gameSize = len(gameDataEncoded)

    if header != 0:
        led = header
        prevLED = None
        while led != -1:
            file.seek(led)
            sizeData = file.read(4)
            nextLedData = file.read(4)
            if len(sizeData) < 4 or len(nextLedData) < 4:
                break
            size = struct.unpack('I', sizeData)[0]
            nextLED = struct.unpack('I', nextLedData)[0]
            if size >= gameSize + RECORD_SIZE_FIELD:
                if prevLED is None:
                    writeHeader(file, nextLED)
                else:
                    file.seek(prevLED + 4)
                    file.write(struct.pack('I', nextLED))
                file.seek(led)
                writeRecord(file, gameDataEncoded)
                remainingSpace = size - gameSize - RECORD_SIZE_FIELD
                if remainingSpace > MIN_UNUSED_SPACE:
                    file.write(struct.pack('I', remainingSpace))
                    file.write(struct.pack('I', nextLED))
                return (
                    f"{gameSize} bytes\nTamanho do espaço reutilizado: {size} bytes (sobra {remainingSpace} bytes)\n"
                    f"Local: offset = {led} bytes (0x{led:x})")
            prevLED = led
            led = nextLED
        file.seek(0, 2)
        pos = file.tell()
        writeRecord(file, gameDataEncoded)
        return f"{gameSize} bytes\nLocal: fim do arquivo"
    else:
        file.seek(0, 2)
        pos = file.tell()
        writeRecord(file, gameDataEncoded)
        return f"{gameSize} bytes\nLocal: fim do arquivo"


def removeGame(file, id):
    pos, recordData = searchById(file, id)
    if not recordData:
        return False, None
    file.seek(pos)
    size = struct.unpack('H', file.read(2))[0]
    header = readHeader(file)
    file.seek(pos)
    file.write(struct.pack('I', header))
    file.write(struct.pack('I', size))
    writeHeader(file, pos)
    return True, f"Registro removido! ({size} bytes) Local: offset = {pos} bytes (0x{pos:x})"


def printLED(file):
    header = readHeader(file)
    if header == 0:
        print("LED -> [offset: -1] Total: 0 espacos disponiveis")
        return
    led = header
    totalSpaces = 0
    print("LED -> ", end="")
    while led != -1:
        print(f"[offset: {led}] \n", end="")
        sizeData = file.read(4)
        nextLedData = file.read(4)
        if len(sizeData) < 4 or len(nextLedData) < 4:
            break

    print(f"\n\n[offset: -1] Total: {totalSpaces} espacos disponiveis")


def executeOperations(dataFile, operationsFile):
    with open(dataFile, 'r+b') as file:
        if os.path.getsize(dataFile) == 0:
            writeHeader(file, 0)
        with open(operationsFile, 'r') as operations:
            for line in operations:
                operation = line.strip().split()
                if operation[0] == 'b':
                    searchId = operation[1]
                    _, result = searchById(file, searchId)
                    if result:
                        print(
                            f'Busca pelo registro de chave "{searchId}" {result.decode("utf-8")}'
                        )
                    else:
                        print(f'Erro: registro não encontrado!')
                elif operation[0] == 'i':
                    gameData = ' '.join(operation[1:])
                    result = insertGame(file, gameData)
                    print(
                        f'Inserção do registro de chave "{operation[1].split("|")[0]}" {result}'
                    )
                elif operation[0] == 'r':
                    remove_id = operation[1]
                    success, result = removeGame(file, remove_id)
                    if success:
                        print(
                            f'Remoção do registro de chave "{remove_id}"\n{result}'
                        )
                    else:
                        print(f'Erro: registro não encontrado!')


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Use: python main.py -e <arq_operações> para ler o arquivo de operações\n"
        )
        print("ou\n")
        print("python main.py -p para imprimir a LED \n")
    elif sys.argv[1] == '-e':
        executeOperations('dados.dat', sys.argv[2])
    elif sys.argv[1] == '-p':
        with open('dados.dat', 'r+b') as file:
            printLED(file)
