import {Heading, Accordion,
    AccordionItem,
    AccordionButton,
    AccordionPanel,
    AccordionIcon,
    Box, 
    Breadcrumb,
    BreadcrumbItem,
    BreadcrumbLink,Container,
    TableContainer,

} from "@chakra-ui/react"
import React from "react";
import {HiChevronRight} from "react-icons/hi";

const Help = () => {

    return (
        <>
            <Box px={20} pt={2}>
            <Breadcrumb spacing='8px' separator={<HiChevronRight color='gray.500'/>}>
                <BreadcrumbItem>
                    <BreadcrumbLink href=''>Help</BreadcrumbLink>
                </BreadcrumbItem>
            </Breadcrumb>
            <Heading>Help and FAQ</Heading>
            <Box  h={5}></Box>
            <Box backgroundColor="white" borderRadius="2xl" minH="60vh">
                <Container maxW='4xl' pt={10}>
                    <TableContainer>
                        <Accordion defaultIndex={[0]} allowMultiple='true' allowToggle='true'>
  <AccordionItem>
    <h2>
      <AccordionButton _expanded={{bg: 'blue', color: 'white'}}>
        <Box flex='1' textAlign='left'>
          Einleitung
        </Box >
        <AccordionIcon />
      </AccordionButton>
    </h2>
    <AccordionPanel pb={4}>
    
      Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
      tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim
      veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea
      commodo consequat.
      
    </AccordionPanel>
  </AccordionItem>

  <AccordionItem>
    <h2>
      <AccordionButton _expanded={{bg: 'blue', color: 'white'}}>
        <Box flex='1' textAlign='left'>
          Registrierung/Login
        </Box>
        <AccordionIcon />
      </AccordionButton>
    </h2>
    <AccordionPanel pb={4}>
      Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
      tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim
      veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea
      commodo consequat.
    </AccordionPanel>
  </AccordionItem>

  <AccordionItem>
    <h2>
      <AccordionButton _expanded={{bg: 'blue', color: 'white'}}>
        <Box flex='1' textAlign='left'>
          Szenarios
        </Box>
        <AccordionIcon />
      </AccordionButton>
    </h2>
    <AccordionPanel pb={4}>
      Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
      tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim
      veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea
      commodo consequat.
    </AccordionPanel>
  </AccordionItem>

  <AccordionItem>
    <h2>
      <AccordionButton _expanded={{bg: 'blue', color: 'white'}}>
        <Box flex='1' textAlign='left'>
          Szenario Studio
        </Box>
        <AccordionIcon />
      </AccordionButton>
    </h2>
    <AccordionPanel pb={4}>
      Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
      tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim
      veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea
      commodo consequat.
    </AccordionPanel>
  </AccordionItem>
  <AccordionItem>
    <h2>
      <AccordionButton _expanded={{bg: 'blue', color: 'white'}}>
        <Box flex='1' textAlign='left'>
          Profil
        </Box>
        <AccordionIcon />
      </AccordionButton>
    </h2>
    <AccordionPanel pb={4}>
      Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
      tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim
      veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea
      commodo consequat.
    </AccordionPanel>
  </AccordionItem>
  <AccordionItem>
    <h2>
      <AccordionButton _expanded={{bg: 'blue', color: 'white'}}>
        <Box flex='1' textAlign='left'>
          Sonstiges
        </Box>
        <AccordionIcon />
      </AccordionButton>
    </h2>
    <AccordionPanel pb={4}>
      Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
      tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim
      veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea
      commodo consequat.
    </AccordionPanel>
    
  </AccordionItem>
  
  
</Accordion>
                    </TableContainer>
                </Container>
            </Box>
        </Box>
        </>
    )
}

export default Help;