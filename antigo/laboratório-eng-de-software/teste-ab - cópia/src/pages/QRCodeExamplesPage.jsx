import PageLayout from '@/components/PageLayout';
import QRCodeItem from '@/components/QRCodeItem';
import SectionHeader from '@/components/SectionHeader';
import { Box, SimpleGrid, } from '@chakra-ui/react';
import { QrCode } from 'lucide-react';

import { students } from './mock-list';


const QRCodeExamplesPage = () => {

  return (
    <PageLayout>
      <Box paddingBottom={10}>
        <SectionHeader title='Exemplos de QR Codes' icon={QrCode} />

        <SimpleGrid columns={{ base: 1, md: 2, lg: 3, xl: 4 }} spacing={10}>
          {students.map(student => (
            <QRCodeItem value={student.name} key={student.id} />
          ))}
        </SimpleGrid>
      </Box>
    </PageLayout>
  );
}

export default QRCodeExamplesPage;
