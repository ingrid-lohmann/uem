import { Alert, AlertDescription, AlertTitle } from '@chakra-ui/react'
import { AlertCircleIcon } from 'lucide-react'

const AlertInfo = () => {
  return (
    <Alert status="info" flexDirection="column" alignItems="center" justifyContent="center" textAlign="center" borderRadius="md" p={4} width='md'>
      <AlertCircleIcon size={40} mr={0} />
      <AlertTitle mt={4} mb={1} fontSize="lg">Atenção!</AlertTitle>
      <AlertDescription maxWidth="sm">
        Por favor, acesse esta página usando um celular para registrar a presença.
      </AlertDescription>
    </Alert>
  )
}

export default AlertInfo