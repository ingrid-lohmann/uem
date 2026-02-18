import { HStack, Heading } from '@chakra-ui/react';
import PropTypes from 'prop-types'

const SectionHeader = ({ icon: Icon, title }) => {
  return (
    <HStack mb={6} justifyContent="center">
      {Icon && <Icon size={32} color="#319795" />}
      <Heading as="h1" size="xl">{title}</Heading>
    </HStack>
  );
};

SectionHeader.propTypes = {
  title: PropTypes.string.isRequired,
  icon: PropTypes.elementType.isRequired,
};

export default SectionHeader