const express = require("express");

const normalize = require("../utils/normalize");
const { database3 } = require("../utils/database");
const { PORT_3, STATUS_NOT_FOUND } = require("../utils/variaveis");

const app = express();

app.use(express.json());

app.get("/", (req, res) => {
  res.json(database3);
});

app.get("/buscar/:key", async (req, res) => {
  let foundData = null;

  try {
    const query = req.params.key;
    const foundData = database3.filter(
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

app.listen(PORT_3, () => {
  console.log(`Servidor 3 em execução na porta ${PORT_3}`);
});
