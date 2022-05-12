import { Heading, Container, Grid, GridItem, Flex, Spacer, Box } from "@chakra-ui/react"
import React from "react";

const Simulation = () => {

    return (
        <Flex flexDir="column" flexGrow={1}>
            <Heading p='5'>This is our beautiful Simulation</Heading>
            <Container maxW='container.2xl'>
                <Flex>
                    <Box w='60%'>
                        <Grid
                            h='100%'
                            templateRows='repeat(2, 1fr)'
                            templateColumns='repeat(5, 1fr)'
                            gap={4}
                            textAlign='center'
                            fontWeight='bold'
                            color='white'
                        >
                            <GridItem rowSpan={2} _hover={{ boxShadow: '2xl' }} colSpan={1} boxShadow='md' rounded='md' bg='blue.300'> Tasks</GridItem>
                            <GridItem colSpan={2} _hover={{ boxShadow: '2xl' }} boxShadow='md' rounded='md' bg='blue.800'>Progress Graph</GridItem>
                            <GridItem colSpan={2} _hover={{ boxShadow: '2xl' }} boxShadow='md' rounded='md' bg='blue.100'>Employees</GridItem>
                            <GridItem colSpan={4} _hover={{ boxShadow: '2xl' }} boxShadow='md' rounded='md' bg='blue.700'>Stress Level</GridItem>
                        </Grid>
                    </Box>
                    <Spacer />
                    <Box
                        p='5'
                        w='38%'
                        boxShadow='md'
                        rounded='md'
                        bg='gray.400'
                        textAlign='center'
                    >
                        <p>
                            <b>Actions</b>
                        </p>
                        <Grid

                            templateRows='repeat(10, 1fr)'
                            templateColumns='repeat(3, 1fr)'
                            gap={4}
                            p='5'
                            justify="flex-end"
                        >
                            <GridItem colSpan={3} _hover={{ boxShadow: '2xl' }} boxShadow='md' rounded='md' bg='gray.100'> Choice 1 </GridItem>
                            <GridItem colSpan={3} _hover={{ boxShadow: '2xl' }} boxShadow='md' rounded='md' bg='gray.100'> Choice 2 </GridItem>
                            <GridItem colSpan={3} _hover={{ boxShadow: '2xl' }} boxShadow='md' rounded='md' bg='gray.100'> Choice 3 </GridItem>
                            <GridItem colSpan={3} _hover={{ boxShadow: '2xl' }} boxShadow='md' rounded='md' bg='gray.100'> Choice 4 </GridItem>
                            <GridItem colSpan={3} _hover={{ boxShadow: '2xl' }} boxShadow='md' rounded='md' bg='gray.100'> Choice 5 </GridItem>
                            <GridItem colSpan={3} _hover={{ boxShadow: '2xl' }} boxShadow='md' rounded='md' bg='gray.100'> Choice 6 </GridItem>
                            <GridItem colSpan={3} _hover={{ boxShadow: '2xl' }} boxShadow='md' rounded='md' bg='gray.100'> Choice 7 </GridItem>
                            <GridItem colSpan={2} />
                            <GridItem colSpan={1} _hover={{ boxShadow: '2xl' }} boxShadow='md' rounded='md' bg='blue.500' color='white' fontWeight='bold'> Next Week </GridItem>
                        </Grid>
                    </Box>
                </Flex >
            </Container >
        </Flex>
    )
}

export default Simulation;