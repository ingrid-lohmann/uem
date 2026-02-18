import { Box, Text, VStack } from '@chakra-ui/react';
import PropTypes from 'prop-types';
import QRCode from 'react-qr-code';


const QRCodeItem = ({ value }) => {
  if (!value) {
    return (
      <Box p={4} borderWidth="1px" borderRadius="md" borderColor="gray.200">
        <Text color="gray.500">Nenhum valor para gerar o QR Code.</Text>
      </Box>
    );
  }

  return (
    <VStack spacing={4} p={4} borderWidth="1px" borderRadius="md" borderColor="gray.200" boxShadow="sm">
      <Box p={2} bg="white" borderRadius="md" display="inline-block">
        <QRCode value={value} />
      </Box>
      <Text fontSize="sm" color="gray.600" isTruncated maxW="100%" as={'b'}>{value}</Text>
    </VStack>
  );
};

QRCodeItem.propTypes = {
  value: PropTypes.string.isRequired,
};

export default QRCodeItem;