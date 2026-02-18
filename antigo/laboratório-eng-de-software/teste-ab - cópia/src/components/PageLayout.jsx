import { Box, Flex } from '@chakra-ui/react';
import PropTypes from 'prop-types';

import Footer from './Footer';

const PageLayout = ({ children }) => {
  return (
    <Flex direction="column" minH="100vh">
      <Box flex="1">
        {children}
      </Box>
      <Footer />
    </Flex>
  );
};

PageLayout.propTypes = {
  children: PropTypes.node.isRequired,
};

export default PageLayout;
