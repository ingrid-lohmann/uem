import { Box, Text } from '@chakra-ui/react';
import { useMemo } from 'react';

const footerMessages = [
  'Feito com café, código e carinho — equipe <undefined />',
  'Feito por humanos (e alguns commits de madrugada) — equipe <undefined />',
  'Feito na base do improviso e da paixão — equipe <undefined />',
  'Feito por gente que testa em produção — equipe <undefined />',
  'Feito com ❤️ e alguns bugs — equipe <undefined />',
  'Feito por quem ama código… e sofre com ele — equipe <undefined />',
  'Feito com <div>, emoção e push forçado — equipe <undefined />',
  'Feito com bugs, mas com orgulho — equipe <undefined />',
  'Feito com a coragem de quem não leu a doc — equipe <undefined />',
  'Feito por devs que não sabem nomear variáveis — equipe <undefined />',
];

const Footer = () => {
  const randomMessage = useMemo(() => {
    const index = Math.floor(Math.random() * footerMessages.length);
    return footerMessages[index];
  }, []);

  return (
    <Box as="footer" mb={2} textAlign="center" color="gray.600" fontSize="sm">
      <Text fontSize='xs'>
        {randomMessage}
      </Text>
    </Box>
  );
};

export default Footer