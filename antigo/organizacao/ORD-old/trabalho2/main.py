import os
import struct

# Ingrid Lohmann RA: 117698
# Favor usar o arquivo op.txt, pois tive que alterar a estrutura
# para que funcionasse


class BTreeNode:
    def __init__(self, order, is_leaf=True):
        self.is_leaf = is_leaf
        self.keys = []
        self.children = []
        self.offsets = []
        self.order = order

    def insert_non_full(self, key, offset):
        i = len(self.keys) - 1
        if self.is_leaf:
            self.keys.append(None)
            self.offsets.append(None)
            while i >= 0 and key < self.keys[i]:
                self.keys[i + 1] = self.keys[i]
                self.offsets[i + 1] = self.offsets[i]
                i -= 1
            self.keys[i + 1] = key
            self.offsets[i + 1] = offset
        else:
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

    def print_tree(self, node=None, level=0, page_number=0, is_root=True):
        if node is None:
            node = self.root

        print(f"Página {page_number}")
        print(f"Chaves: {' | '.join(map(str, node.keys))}")
        print(f"Offsets: {' | '.join(map(str, node.offsets))}")

        if not node.is_leaf:
            children_pages = [
                child_page for child_page in range(len(node.children))]
            print(f"Filhas: {' | '.join(map(str, children_pages))}")
        else:
            print(f"Filhas: {' | '.join(['-1'] * self.order)}")

        if is_root:
            print("-" * 20 + " Raiz " + "-" * 20)

        if not node.is_leaf:
            for i, child in enumerate(node.children):
                self.print_tree(
                    node.children[i], level + 1, page_number + i + 1, is_root=False)

    def _save_node_to_file(self, file, node):
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
        raw_data = file.read(4)
        if len(raw_data) < 4:
            raise ValueError(
                "Erro ao ler o número de chaves: arquivo incompleto.")
        num_keys = struct.unpack('i', raw_data)[0]

        node = BTreeNode(self.order)

        for _ in range(num_keys):
            raw_key = file.read(4)
            raw_offset = file.read(4)
            if len(raw_key) < 4 or len(raw_offset) < 4:
                raise ValueError(
                    "Erro ao ler chave ou offset: arquivo incompleto.")
            key = struct.unpack('i', raw_key)[0]
            offset = struct.unpack('i', raw_offset)[0]
            node.keys.append(key)
            node.offsets.append(offset)

        raw_is_leaf = file.read(4)
        if len(raw_is_leaf) < 4:
            raise ValueError(
                "Erro ao verificar se o nó é folha: arquivo incompleto.")
        is_leaf = struct.unpack('i', raw_is_leaf)[0]
        node.is_leaf = bool(is_leaf)

        if not node.is_leaf:
            raw_num_children = file.read(4)
            if len(raw_num_children) < 4:
                raise ValueError(
                    "Erro ao ler o número de filhos: arquivo incompleto.")
            num_children = struct.unpack('i', raw_num_children)[0]
            for _ in range(num_children):
                child = self._load_node_from_file(file)
                node.children.append(child)

        return node


def create_index(btree_filename, games_filename, btree):
    try:
        with open(games_filename, "rb") as games_file:
            total_records = struct.unpack('i', games_file.read(4))[0]
            offset = 4

            for _ in range(total_records):
                record = games_file.read(100)
                game_id = extract_game_id(record)
                btree.insert(game_id, offset)
                offset += 100

        # Sobrescrever o arquivo btree.dat
        btree.save_to_file(btree_filename)
        print("Árvore-B criada e armazenada com sucesso no arquivo", btree_filename)

    except Exception as e:
        print("Erro ao criar o índice:", str(e))


def extract_game_id(record):
    return int.from_bytes(record[:4], byteorder='big')


def execute_operations(btree_filename, games_filename, operations_filename):
    try:
        btree = BTree(order=4)
        btree.load_from_file(btree_filename)
        with open(operations_filename, "r") as operations_file:
            for line in operations_file:
                original_operation = line.strip().split("|")
                operation = list(filter(None, original_operation))
                if len(operation) < 2:
                    continue

                op_type = operation[0].strip().lower()
                game_id = int(operation[1].strip())
                game_data = operation[1:]
                if op_type == "b":
                    offset = btree.search(btree.root, game_id)
                    if offset is not None:
                        with open(games_filename, "rb") as games_file:
                            games_file.seek(offset)
                            record = games_file.read(100)
                            print(f"Registro encontrado para ID {game_id}: {
                                  record.decode('utf-8').strip()}")
                    else:
                        print(f"Registro com ID {game_id} não encontrado")

                elif op_type == "i" and len(game_data) == 6:
                    if btree.search(btree.root, game_id) is not None:
                        print(f"Erro: chave '{game_id}' já existente!")
                    else:
                        with open(games_filename, "ab") as games_file:
                            offset = games_file.tell()
                            new_record = f"{game_id}|{game_data[2]}|{
                                game_data[3]}|{game_data[4]}|{game_data[5]}|"
                            games_file.write(
                                new_record.ljust(100).encode('utf-8'))

                        btree.insert(game_id, offset)
                        btree.save_to_file(btree_filename)
                        print(f"Registro inserido para ID {
                              game_id} no offset {offset}")

    except Exception as e:
        print("Erro ao executar operações:", str(e))


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Uso: programa -c|-e|-p <arquivo>")
        sys.exit(1)

    option = sys.argv[1]
    ORDEM = 4

    btree = BTree(order=ORDEM)

    if option == "-c":
        btree_filename = "btree.dat"
        games_filename = "games.dat"
        if os.path.exists(btree_filename):
            os.remove(btree_filename)
        create_index(btree_filename, games_filename, btree)
    elif option == "-e":
        btree_filename = "btree.dat"
        games_filename = "games.dat"
        if len(sys.argv) < 3:
            print("Uso: programa -e <arquivo_operacoes>")
            sys.exit(1)
        operations_filename = sys.argv[2]
        execute_operations(btree_filename, games_filename, operations_filename)
        pass
    elif option == "-p":
        btree_filename = "btree.dat"
        btree = BTree(order=ORDEM)
        btree.load_from_file(btree_filename)
        btree.print_tree(btree.root)
        pass
    else:
        print("Opção inválida")
