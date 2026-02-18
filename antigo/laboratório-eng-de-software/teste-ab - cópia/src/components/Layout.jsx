import { Box, Flex, HStack, IconButton, useDisclosure, Stack, Button } from '@chakra-ui/react';
import { X, Menu } from 'lucide-react';
import { useCallback } from 'react';
import { Link, Outlet } from 'react-router-dom';

const FORM_LINK = "https://forms.gle/h3iK3nsHXhn5sVVXA";

const Links = [
  { name: 'Sobre', to: '/' },
  { name: 'Ler QR Code', to: '/qr-code-reader' },
  { name: 'Exemplos de QR Code', to: '/qr-code-exemples' },
  { name: 'Lista de presença', to: '/lista-alunos' },
  { name: 'Feedback do Teste', to: FORM_LINK, isExternal: true }
];

const Layout = () => {
  const { isOpen, onOpen, onClose } = useDisclosure();

  const handleLinkClick = useCallback(() => {
    // eslint-disable-next-line no-undef
    sessionStorage.removeItem('checkedItems');
    onClose();
  }, [onClose])

  const renderExternalButtonLink = (link) => {
    return (
      <Button
        key={link.to}
        as="a"
        href={link.to}
        target="_blank"
        rel="noopener noreferrer"
        w="full"
        variant="ghost"
        colorScheme='white'
        onClick={handleLinkClick}
      >
        {link.name}
      </Button>
    )
  }

  const renderLink = (link) => {
    if (link.isExternal) return renderExternalButtonLink(link)
    return (
      <Link key={link.to} to={link.to}>
        <Button w="full" variant="ghost" colorScheme='white' onClick={handleLinkClick}>
          {link.name}
        </Button>
      </Link>
    )
  }


  const renderLinks = () => {
    return (
      Links.map(link => {
        return renderLink(link);
      })
    )
  }

  const renderOpenMenu = () => {
    if (!isOpen) return null;

    return (
      <Box pb={4} display={{ md: 'none' }}>
        <Stack as="nav" spacing={4}>
          {Links.map(link => (
            <Link key={link.to} to={link.to}>
              <Button w="full" variant="ghost" onClick={handleLinkClick} colorScheme='white'>
                {link.name}
              </Button>
            </Link>
          ))}
        </Stack>
      </Box>
    )
  }

  return (
    <>
      <Box bg='teal' color='white' px={4} boxShadow="sm" position="sticky" top={0} zIndex={10}>
        <Flex h={16} alignItems="center" justifyContent="space-between">
          <IconButton
            size="md"
            variant='link'
            colorScheme='white'
            icon={isOpen ? <X /> : <Menu />}
            aria-label="Abrir menu"
            display={{ md: 'none' }}
            onClick={isOpen ? onClose : onOpen}
          />
          <HStack spacing={8} alignItems="center">
            <Box fontWeight="bold">Teste A/B</Box>
            <HStack as="nav" spacing={4} display={{ base: 'none', md: 'flex' }}>
              {renderLinks()}
            </HStack>
          </HStack>
        </Flex>

        {renderOpenMenu()}
      </Box>

      <Box p={4}>
        <Outlet />
      </Box>
    </>
  );
}

export default Layout;
