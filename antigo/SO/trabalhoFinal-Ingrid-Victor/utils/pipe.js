const axios = require("axios").default;
const { Readable } = require("stream");
const { PORT_1, PORT_2, PORT_3 } = require("./variaveis");

const pipe = () => {
  const urls = [
    `http://localhost:${PORT_1}/`,
    `http://localhost:${PORT_2}/`,
    `http://localhost:${PORT_3}/`,
  ];

  const buscarDados = async (url) => {
    try {
      const response = await axios.get(url);
      return response.data;
    } catch (error) {
      console.error("Error fetching data:", error);
      return null;
    }
  };

  const streamLeitura = Readable.from(urls);

  const streamTransformacao = new Readable({
    objectMode: true,
    async read() {
      const url = await streamLeitura.read();
      if (url !== null) {
        const data = await buscarDados(url);
        this.push(data);
      } else {
        this.push(null);
      }
    },
  });

  const resultados = [];
  streamTransformacao.on("data", (data) => {
    resultados.push(data);
  });
  streamTransformacao.on("end", () => {
    console.log("Dados encontrados: ", resultados);
  });
};

module.exports = pipe;
