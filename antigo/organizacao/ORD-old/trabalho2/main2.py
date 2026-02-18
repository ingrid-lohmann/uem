import re
import os
import struct


class BTreeNode:
    def __init__(self, order, is_leaf=True):
        self.is_leaf = is_leaf
        self.keys = []
        self.children = []
        self.offsets = []  # Lista de byte-offsets
        self.order = order

    def insert_non_full(self, key, offset):
        i = len(self.keys) - 1
        if self.is_leaf:
            # Inserção direta no nó folha
            self.keys.append(None)
            self.offsets.append(None)
            while i >= 0 and key < self.keys[i]:
                self.keys[i + 1] = self.keys[i]
                self.offsets[i + 1] = self.offsets[i]
                i -= 1
            self.keys[i + 1] = key
            self.offsets[i + 1] = offset
        else:
            # Inserção no nó interno, descendo a árvore
            while i >= 0 and key < self.keys[i]:
                i -= 1
            i += 1
            if len(self.children[i].keys) == 2 * self.order - 1:
                self.split_child(i)
                if key > self.keys[i]:
                    i += 1
            self.children[i].insert_non_full(key, offset)

    def split_child(self, i):
        order = self.order
        new_node = BTreeNode(order, self.children[i].is_leaf)
        y = self.children[i]
        self.children.insert(i + 1, new_node)
        self.keys.insert(i, y.keys[order - 1])
        new_node.keys = y.keys[order:(2 * order - 1)]
        new_node.offsets = y.offsets[order:(2 * order - 1)]
        y.keys = y.keys[0:(order - 1)]
        y.offsets = y.offsets[0:(order - 1)]
        if not y.is_leaf:
            new_node.children = y.children[order:(2 * order)]
            y.children = y.children[0:order]


class BTree:
    def __init__(self, order):
        self.root = BTreeNode(order)
        self.order = order

    def insert(self, key, offset):
        root = self.root
        if len(root.keys) == 2 * self.order - 1:
            new_node = BTreeNode(self.order, False)
            new_node.children.append(self.root)
            new_node.split_child(0)
            self.root = new_node
            self.root.children[0].insert_non_full(key, offset)
        else:
            self.root.insert_non_full(key, offset)

    def search(self, node, key):
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        if i < len(node.keys) and key == node.keys[i]:
            return node.offsets[i]
        if node.is_leaf:
            return None
        else:
            return self.search(node.children[i], key)

    def save_to_file(self, filename):
        with open(filename, "wb") as file:
            self._save_node_to_file(file, self.root)

    def _save_node_to_file(self, file, node):
        # Serialização de um nó em formato binário (ajuste conforme necessário)
        file.write(struct.pack('i', len(node.keys)))  # Número de chaves
        for key, offset in zip(node.keys, node.offsets):
            file.write(struct.pack('i', key))
            file.write(struct.pack('i', offset))
        if not node.is_leaf:
            file.write(struct.pack('i', len(node.children)))
            for child in node.children:
                self._save_node_to_file(file, child)

    def load_from_file(self, filename):
        with open(filename, "rb") as file:
            self.root = self._load_node_from_file(file)

    def _load_node_from_file(self, file):
        try:
            num_keys = struct.unpack('i', file.read(4))[0]
            node = BTreeNode(self.order)
            node.keys = [struct.unpack('i', file.read(4))[0]
                         for _ in range(num_keys)]
            node.offsets = [struct.unpack('i', file.read(4))[0]
                            for _ in range(num_keys)]
            if num_keys > 0:
                num_children = struct.unpack('i', file.read(4))[0]
                if num_children > 0:
                    node.is_leaf = False
                    node.children = [self._load_node_from_file(
                        file) for _ in range(num_children)]
            return node
        except struct.error as e:
            print(f"Erro ao desempacotar dados: {e}")
            return None


def create_index(btree_filename, games_filename, btree):
    try:
        with open(games_filename, "rb") as games_file:
            num_records = int.from_bytes(games_file.read(4), byteorder='big')
            print(f"Número de registros no arquivo: {num_records}")

            for i in range(num_records):
                byte_offset = games_file.tell()

                # Tenta ler o próximo registro (exemplo: 100 bytes por registro)
                record = games_file.read(100)

                # Verifica se o registro lido é menor do que o esperado (indicando fim de arquivo)
                if not record or len(record) < 100:
                    print(
                        f"Registro vazio ou malformado no offset {byte_offset}. Ignorando...")
                    break  # Sair do loop se chegar ao final do arquivo ou encontrar um registro inválido

                # Extrai o game ID do registro
                game_id = extract_game_id(record)

                if game_id is not None:
                    btree.insert(game_id, byte_offset)
                else:
                    print(
                        f"Registro ignorado no offset {byte_offset} devido a erro de extração.")

        # Salvando a árvore-B no arquivo
        with open(btree_filename, "wb") as btree_file:
            btree.save_to_file(btree_file)

        print("Índice criado com sucesso!")

    except Exception as e:
        print(f"Erro ao criar o índice: {e}")


def execute_operations(btree_filename, games_filename, operations_filename):
    try:
        # Carregar a árvore-B do arquivo
        btree = BTree(order=4)
        btree.load_from_file(btree_filename)

        with open(operations_filename, "r") as operations_file:
            for line in operations_file:
                operation = line.strip().split("|")
                if len(operation) < 2:
                    continue

                op_type = operation[0].strip().lower()
                game_id = int(operation[1].strip())

                if op_type == "b":
                    offset = btree.search(btree.root, game_id)
                    if offset is not None:
                        with open(games_filename, "rb") as games_file:
                            games_file.seek(offset)
                            record = games_file.read(100)
                            print(
                                f"Registro encontrado para ID {game_id}: {record.decode('utf-8').strip()}")
                    else:
                        print(f"Registro com ID {game_id} não encontrado")

                elif op_type == "i" and len(operation) == 6:
                    # Checar se o jogo já existe
                    if btree.search(btree.root, game_id) is not None:
                        print(f"Erro: chave '{game_id}' já existente!")
                    else:
                        # Inserir novo registro no final do arquivo games.dat
                        with open(games_filename, "ab") as games_file:
                            offset = games_file.tell()
                            new_record = f"{game_id}|{operation[2]}|{operation[3]}|{operation[4]}|{operation[5]}|"
                            games_file.write(
                                new_record.ljust(100).encode('utf-8'))

                        # Inserir a nova chave e offset na árvore-B
                        btree.insert(game_id, offset)
                        btree.save_to_file(btree_filename)
                        print(
                            f"Registro inserido para ID {game_id} no offset {offset}")

    except Exception as e:
        print("Erro ao executar operações:", str(e))


def extract_game_id(record):
    try:
        # Decodifica o registro para uma string legível
        record_str = record.decode('utf-8').strip()

        # Usa expressão regular para encontrar o primeiro número válido no registro
        match = re.search(r'\d+', record_str)
        if match:
            return int(match.group())  # Retorna o número como inteiro
        else:
            raise ValueError(
                f"Não foi encontrado nenhum ID válido no registro: {record_str}")

    except (ValueError, IndexError) as e:
        print(
            f"Erro ao extrair o game ID do registro: {record}. Detalhes do erro: {e}")
        return None  # Retorna None ou lança um erro dependendo de como você quer tratar isso


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:  # Apenas 2 argumentos são necessários para '-c', '-p', ou '-e'
        print("Uso: programa -c|-e|-p <arquivo>")
        sys.exit(1)

    option = sys.argv[1]
    ORDEM = 4  # Defina a ordem da árvore-B como constante
    btree_filename = "btree.dat"
    games_filename = "games.dat"

    if option == "-c":
        # Não precisa de mais argumentos, apenas cria o índice
        if os.path.exists(btree_filename):
            os.remove(btree_filename)  # Remove o arquivo se já existir
        create_index(btree_filename, games_filename, BTree(order=ORDEM))
    elif option == "-e":
        if len(sys.argv) < 3:  # Para '-e', requer o arquivo de operações
            print("Uso: programa -e <arquivo_operacoes>")
            sys.exit(1)
        operations_filename = sys.argv[2]
        execute_operations(btree_filename, games_filename, operations_filename)
    elif option == "-p":
        # Para '-p', apenas imprime a árvore-B (não requer argumento adicional)
        btree = BTree(order=ORDEM)
        btree.load_from_file(btree_filename)
        print_btree(btree.root)
    else:
        print("Opção inválida")
