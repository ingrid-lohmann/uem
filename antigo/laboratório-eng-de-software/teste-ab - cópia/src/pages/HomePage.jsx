import PageLayout from '@/components/PageLayout';
import { Box, Heading, Text, Stack, HStack, Highlight, Button, Divider } from '@chakra-ui/react';
import { LayoutList, ScanQrCode } from 'lucide-react';

const highlightStyle = { px: '1', py: '1', rounded: 'full', bg: 'teal.100' }

const HomePage = () => {

  const textWithHighlight = (text, words) => {
    return (
      <Text fontSize="md">
        <Highlight
          query={words}
          styles={highlightStyle}
        >
          {text}
        </Highlight>
      </Text>
    );
  }

  const highlightWord = (word) => {
    return (
      <Highlight query={word} styles={highlightStyle}>
        {word}
      </Highlight>
    );
  }

  const renderDescription = () => {
    return (
      <>
        <Text fontSize="lg" color="gray.700">
          Estamos empolgados em testar e melhorar a forma como o registro de presença dos{' '}
          {highlightWord('escoteiros')}
          ! Para isso, estamos fazendo um pequeno experimento.
        </Text>

        <Text fontSize="lg">
          Imagine que estamos experimentando duas maneiras diferentes de fazer a chamada, para ver qual delas é a mais
          {highlightWord('prática e rápida')}
          para todos. Isso é o que chamamos de
          {highlightWord('Teste A/B')}
          ! É como comparar dois caminhos para ver qual nos leva mais rápido ao destino.
        </Text>
      </>
    )
  }

  const renderTestA = () => {
    const text = 'Aqui, os monitores usarão a câmera do celular para escanear um QR Code que cada escoteiro terá. Após ler os QR Codes, clique no botão de confirmar presenças.'
    return (
      <>
        <HStack>
          <ScanQrCode size={28} color="#319795" />
          <Heading size='lg'>
            Chamada por QR Code
          </Heading>
        </HStack>
        {textWithHighlight(text, 'escanear um QR Code')}
        <Text>
          Ah, e para você testar à vontade, temos uma {' '}
          <Button colorScheme='teal' variant='link'>
            página com exemplos de QR Codes
          </Button>
          {' '} que você pode usar!
        </Text>
      </>
    )
  }

  const renderHint = () => {
    return (
      <Text>
        Dica: Você pode abrir essa página de exemplos no seu computador e usar o celular para fazer a leitura, assim fica bem prático!
      </Text>
    )
  }

  const renderFormLink = () => {
    const formLink = 'https://forms.gle/h3iK3nsHXhn5sVVXA';
    return (
      <Text fontSize="md">
        Ao final do teste, por favor, {' '}
        <Button as='a' colorScheme='teal' variant='link' rel="noopener noreferrer" target="_blank" href={formLink}>
          preencha nosso formulário de feedback
        </Button>
        {' '}
        para nos ajudar a aprimorar sua experiência. Sua opinião é muito importante!
      </Text>
    )
  }

  const renderTestB = () => {
    const text = 'Nesta opção, o responsável pela turma terá uma lista digital com todos os nomes dos escoteiros e poderá marcar a presença de cada um manualmente, com um simples toque. Após selecionar os nomes, clique no botão de confirmar presenças';
    return (
      <>
        <HStack>
          <LayoutList size={28} color="#319795" />
          <Heading size='lg'>
            Chamada por Lista
          </Heading>
        </HStack>
        {textWithHighlight(text, 'lista digital com todos os nomes')}
      </>

    )
  }

  const renderImportantInfo = () => {
    const text = 'Nosso objetivo é que a chamada de presença seja sempre rápida, sem erros e fácil de usar.'
    const queryWords = ['rápida', 'sem erros', 'fácil de usar']
    return (
      <>
        <Text fontSize="md">
          Para que o seu feedback seja o mais útil e real possível, pedimos que você realize tanto a chamada por QR Code quanto a chamada por lista
          {highlightWord('diretamente no seu celular.')}
          É que, na vida real, o registro de presença é feito com um aparelho portátil e a câmera do celular é essencial para a opção de QR Code. Assim, sua experiência será a mais próxima da realidade!
        </Text>

        {renderFormLink()}

        {textWithHighlight(text, queryWords)}

        <Text>
          A sua experiência ao testar estas duas opções será essencial para nos ajudar a decidir qual delas se encaixa melhor nas atividades escoteiras.
        </Text>
      </>
    )
  }

  const renderContent = () => {
    return (
    <Box maxW="3xl" mx="auto" py={8} p={4}>
      <Stack spacing={6}>
        <Heading size="xl" textAlign="center" mb={4}>
          Bem-vindo(a) ao Nosso Projeto de Presença!
        </Heading>

        {renderDescription()}

        <Text fontSize="md">
          Neste teste, vamos analisar duas opções de registro:
        </Text>

        <Stack pl={4} spacing={2} borderLeft="4px solid" borderColor="teal.300" py={2} bg="gray.50" borderRadius="md">
          {renderTestA()}
          {renderHint()}
          <Divider />
          {renderTestB()}
        </Stack>

        <Text fontSize="lg" mt={4} fontWeight="bold" color="teal.600">
          Importante: Faça o Teste Pelo Celular!
        </Text>

        {renderImportantInfo()}

        <Text fontSize="md" fontWeight="bold" textAlign="center" mt={6}>
          Contamos com a sua participação para construir a melhor ferramenta! 😊
        </Text>
      </Stack>
    </Box>
  );
  }

  return (
    <PageLayout>
      {renderContent()}
    </PageLayout>
  )
}

export default HomePage;