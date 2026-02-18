import { Button, Checkbox, Text, useToast, Box, Tbody, Tr, Td, Table, Stack } from '@chakra-ui/react';
import { LayoutList } from 'lucide-react';
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

import { students } from './mock-list';

import PageLayout from '@/components/PageLayout';
import SectionHeader from '@/components/SectionHeader';


const StudentListPage = () => {
  const toast = useToast();
  const navigate = useNavigate();

  const saveStorage = () => {
    // eslint-disable-next-line no-undef
    const saved = sessionStorage.getItem('checkedItems');
    return saved ? JSON.parse(saved) : {};
  }

  const [checkedItems, setCheckedItems] = useState(saveStorage);

  useEffect(() => {
    // eslint-disable-next-line no-undef
    sessionStorage.setItem('checkedItems', JSON.stringify(checkedItems));
  }, [checkedItems]);

  const handleCheckboxChange = (name) => {
    setCheckedItems(prev => ({
      ...prev,
      [name]: !prev[name],
    }));
  }

  const handleSubmit = () => {
    const presentScouts = Object.entries(checkedItems)
      .filter(([_, checked]) => checked)
      .map(([name]) => name);

    toast({
      title: presentScouts.length ? 'Presença registrada' : 'Ops!',
      description: presentScouts.length
        ? `Presentes: ${presentScouts.join(', ')}`
        : 'Nenhum escoteiro selecionado',
      status: presentScouts.length ? 'success' : 'error',
      duration: 4000,
      isClosable: true,
    });

    navigate('/feedback', { state: { students: presentScouts } });
  }

  const handleReset = () => {
    setCheckedItems({});
    // eslint-disable-next-line no-undef
    sessionStorage.removeItem('checkedItems');

    toast({
      title: 'Lista limpa',
      description: 'Todos os registros foram removidos.',
      status: 'info',
      duration: 3000,
      isClosable: true,
    });
  }

  const renderCheckBox = (item) => {
    return (
      <Checkbox
        colorScheme='teal'
        key={item.id}
        isChecked={!!checkedItems[item.name]}
        onChange={() => handleCheckboxChange(item.name)}
      >
        <Text fontSize="lg" as={'b'}>{item.name}</Text>
      </Checkbox>
    )
  }

  const renderTable = () => {
    return (
      <Table variant='striped' colorScheme={'gray'}>
        <Tbody>
          {students.map((student, index) => (
            <Tr key={index}>
              <Td>
                {renderCheckBox(student)}
              </Td>
            </Tr>
          ))}
        </Tbody>
      </Table>
    )
  }

  return (
    <PageLayout>
      <Box paddingBottom={10}>
        <SectionHeader title='Lista de Presença dos Escoteiros' icon={LayoutList} />

        {renderTable()}

        <Stack spacing='6' mt={8} direction={{ base: 'column', md: 'row' }} >
          <Button colorScheme="teal" onClick={handleSubmit}>
            Confirmar presenças
          </Button>

          <Button colorScheme="red" variant='outline' onClick={handleReset}>
            Limpar seleção
          </Button>
        </Stack>

      </Box>
    </PageLayout>
  );
}

export default StudentListPage;
