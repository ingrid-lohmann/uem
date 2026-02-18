const express = require("express");

const normalize = require("../utils/normalize");
const { database2 } = require("../utils/database");
const { PORT_2, STATUS_NOT_FOUND } = require("../utils/variaveis");

const app = express();

app.use(express.json());

app.get("/", (req, res) => {
  res.json(database2);
});

app.get("/buscar/:key", async (req, res) => {
  let foundData = null;

  try {
    const query = req.params.key;
    const foundData = database2.filter(
      (item) =>
        normalize(item.titulo).includes(normalize(query)) ||
        normalize(item.autor).includes(normalize(query))
    );
    if (foundData) {
      res.json(foundData);
      return;
    }
  } catch (error) {
    console.error("Erro ao buscar dados no servidor:", error);
  }

  if (!foundData) {
    res.status(STATUS_NOT_FOUND).json({ message: "Dado não encontrado" });
  }
});

app.listen(PORT_2, () => {
  console.log(`Servidor 2 em execução na porta ${PORT_2}`);
});
