import PageLayout from '@/components/PageLayout';
import { Box, Heading, Button, HStack, VStack, Table, Tr, Td, Tbody, Container, Tfoot } from '@chakra-ui/react';
import { ListChecks } from 'lucide-react';
import { useCallback } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

const FeedBackPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const students = location.state?.students || [];

  const today = new Date();

  const formattedDate = today.toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: 'long',
    year: 'numeric'
  });

  const handleNavigate = useCallback(() => {
    // eslint-disable-next-line no-undef
    sessionStorage.removeItem('checkedItems');
    // eslint-disable-next-line no-undef
    sessionStorage.removeItem('scanned');
    navigate('/');
  }, [navigate]);

  const handleGoBack = useCallback(() => {
    navigate(-1);
  }, [navigate]);

  const renderButtons = () => {
    return (
      <VStack>
        <Button colorScheme='teal' mt={6} onClick={handleNavigate} w='full'>
          Finalizar
        </Button>
        <Button colorScheme='teal' variant='ghost' onClick={handleGoBack} w='full'>
          Voltar
        </Button>
      </VStack>
    )
  }

  return (
    <PageLayout>
      <Box p={4}>
        <VStack marginBottom={20}>
          <HStack justifyContent='center'>
            <ListChecks size={32} color="#319795" />
            <Heading as="h1" size="xl">Lista de presença</Heading>
          </HStack>
          <Heading size="xs" color={'gray.500'}>Data: {formattedDate}</Heading>
        </VStack>

        <Container>
          <Table variant='striped' colorScheme='gray'>
            <Tbody>
              {students.map((student, index) => (
                <Tr key={index}>
                  <Td>{student}</Td>
                </Tr>
              ))}
            </Tbody>
            <Tfoot>
              <Tr>
                <Td textAlign="right" fontWeight="bold">Total de alunos: {students.length}</Td>
              </Tr>
            </Tfoot>
          </Table>
          {renderButtons()}
        </Container>
      </Box>
    </PageLayout>
  );
}

export default FeedBackPage;
