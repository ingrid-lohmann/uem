const axios = require("axios").default;

const { PORT_1, PORT_2, PORT_3 } = require("./variaveis");

const fifo = () => {
  const links = [
    `http://localhost:${PORT_1}/`,
    `http://localhost:${PORT_2}/`,
    `http://localhost:${PORT_3}/`,
  ];

  let serverData = [];

  links.forEach(async (link, index) => {
    const resposta = await axios.get(link);
    serverData.push(...resposta.data);
    if (index == 2) {
      console.log(JSON.stringify(serverData));
    }
  });
};

module.exports = fifo;
