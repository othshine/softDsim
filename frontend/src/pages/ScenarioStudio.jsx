import { Heading, Container,  Flex,  Box, Button, Breadcrumb,BreadcrumbItem,
    BreadcrumbLink,Input,HStack, StackDivider,ButtonGroup,Modal,
    ModalOverlay,
    ModalContent,
    ModalHeader,
    ModalFooter,
    ModalBody,
    ModalCloseButton,useDisclosure,useToast, } from "@chakra-ui/react"
import React from "react";
import {HiChevronRight} from "react-icons/hi";

const ScenarioStudio = () => {
    const [value, setValue] = React.useState('1');
    const { isOpen, onOpen, onClose } = useDisclosure();
    const toast = useToast();
    
  

    return (
        <Flex px={10} pt={2} flexDir="column" flexGrow={1}>
            <Breadcrumb spacing='8px' separator={<HiChevronRight color='gray.500'/>}>
                <BreadcrumbItem>
                    <BreadcrumbLink href=''>Scenario Studio</BreadcrumbLink>
                </BreadcrumbItem>
            </Breadcrumb>
            <Heading>Scenario Studio</Heading>
            <Box  h={5}></Box>
            <Box backgroundColor="white" borderRadius="2xl" minH="60vh" >
            <Container maxW='container.4xl' pt={10}>
            <Box backgroundColor="white"  minH="60vh" >
                
            <Heading as='h4' size='md' pb='2'>Basic Informations</Heading>
            <hr></hr>
            <HStack divider={<StackDivider borderColor='gray.200' />} spacing={4} align='stretch'>
  <Box p='5'>
  <Input placeholder='Set Method'/>
  </Box>
  <Box p='5'>
  <Input placeholder='Set Budget'/>
  </Box>
  <Box p='5'>
  <Input placeholder='Set Duration'/>
  </Box>
  <Box p='5'>
  <Input placeholder='Set Goal'/>
  </Box>
  <Box p='5'>
  <Input placeholder='Description'/>
  </Box>
</HStack>
<Heading as='h4' size='md' pb='2'>Scenario Details</Heading>
            <hr></hr>
            <HStack divider={<StackDivider borderColor='gray.200' />} spacing={4} align='stretch'>
  
  <Box p='5'>
  <Input placeholder='Set Name'/>
  </Box>
  <Box p='5'>
  <Input placeholder='Senior (Development)'/>
  </Box>
  <Box p='5'>
  <Input placeholder='Senior (Management)'/>
  </Box>
  <Box p='5'>
  <Input placeholder='Senior (UI/UX)'/>
  </Box>
  <Box p='5'>
  <Input placeholder='Additional'/>
  </Box>
</HStack>
<Heading as='h4' size='md' pb='2'>Employees</Heading>
            <hr></hr>
            <HStack divider={<StackDivider borderColor='gray.200' />} spacing={4} align='stretch'>
            <Box p='5'>
  <Input placeholder='Java Developer'/>
  </Box>
  <Box p='5'>
  <Input placeholder='Frontend Developer'/>
  </Box>
  <Box p='5'>
  <Input placeholder='Backend Developer'/>
  </Box>
  <Box p='5'>
  <Input placeholder='Fullstack'/>
  </Box>
  <Box p='5'>
  <Input placeholder='DevOps'/>
  </Box>

            </HStack>
            <Heading as='h4' size='md' pb='2'>Additional</Heading>
            <hr></hr>
            <HStack divider={<StackDivider borderColor='gray.200' />} spacing={4} align='stretch'>
            <Box p='5'>
  <Input placeholder='...'/>
  </Box>
  <Box p='5'>
  <Input placeholder='...'/>
  </Box>
  <Box p='5'>
  <Input placeholder='...'/>
  </Box>
  <Box p='5'>
  <Input placeholder='...'/>
  </Box>
  <Box p='5'>
  <Input placeholder='...'/>
  </Box>

            </HStack>
            <Heading as='h4' size='md' pb='2'>Build</Heading>
            <hr></hr>
            <HStack divider={<StackDivider borderColor='gray.200' />} spacing={4} align='stretch'>
            <ButtonGroup variant='outline' spacing='6'p='5'>
  
  <Button colorScheme='blue'
      onClick={() =>
        toast({
          title: 'Scenario stored.',
          description: "We've stored the new scenario in the database.",
          status: 'success',
          duration: 9000,
          isClosable: true,
        })
      }
    >
      Build Scenario
    </Button>
  <Button colorScheme='red'>Clear Form</Button>
  <Button onClick={onOpen}>Help</Button>

      <Modal isOpen={isOpen} onClose={onClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>How to set a proper scenario</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
          Lorem ipsum dolor sit amet, consetetur sadipscing elitr, 
          sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. 
          At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. 
          Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, 
          sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, 
          no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, 
          sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. 
          Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.
            
          </ModalBody>

          <ModalFooter>
            <Button colorScheme='blue' mr={3} onClick={onClose}>
              Close
            </Button>
            
          </ModalFooter>
        </ModalContent>
      </Modal>
  
</ButtonGroup>
  

            </HStack>
            
            </Box>
            
      

            </Container >
            </Box>
        </Flex>
    )
}

export default ScenarioStudio;
