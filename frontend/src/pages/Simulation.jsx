import { Heading, Container, Grid, GridItem, Flex, Spacer, Box } from "@chakra-ui/react"
import React from "react";

const Simulation = () => {

    return (
        <>
            <Heading p='5'>This is our beautiful Simulation</Heading>
            <Container maxW='container.2xl'>
                <Flex>
                    <Box w='60%'>
                        <Grid
                            h='600px'
                            templateRows='repeat(2, 1fr)'
                            templateColumns='repeat(5, 1fr)'
                            gap={4}
                            textAlign='center'
                            fontWeight='bold'
                            color='white'
                        >
                            <GridItem rowSpan={2} _hover={{ boxShadow: '2xl' }} colSpan={1} boxShadow='md' rounded='md' bg='#63B3ED'> Tasks</GridItem>
                            <GridItem colSpan={2} _hover={{ boxShadow: '2xl' }} boxShadow='md' rounded='md' bg='#2A4365'>Progress Graph</GridItem>
                            <GridItem colSpan={2} _hover={{ boxShadow: '2xl' }} boxShadow='md' rounded='md' bg='#BEE3F8'>Employees</GridItem>
                            <GridItem colSpan={4} _hover={{ boxShadow: '2xl' }} boxShadow='md' rounded='md' bg='#2B6CB0'>Stress Level</GridItem>
                        </Grid>
                    </Box>
                    <Spacer />
                    <Box
                        p='5'
                        w='38%'
                        boxShadow='md'
                        rounded='md'
                        bg='#D5D8DC'
                        textAlign='center'
                    >
                        <p>
                            <b>Actions</b>
                        </p>
                        <Grid
                            h='500px'
                            templateRows='repeat(10, 1fr)'
                            templateColumns='repeat(3, 1fr)'
                            gap={4}
                            p='5'
                            justify="flex-end"
                        >
                            <GridItem colSpan={3} _hover={{ boxShadow: '2xl' }} boxShadow='md' rounded='md' bg='#EAEDED'> Choice 1 </GridItem>
                            <GridItem colSpan={3} _hover={{ boxShadow: '2xl' }} boxShadow='md' rounded='md' bg='#EAEDED'> Choice 2 </GridItem>
                            <GridItem colSpan={3} _hover={{ boxShadow: '2xl' }} boxShadow='md' rounded='md' bg='#EAEDED'> Choice 3 </GridItem>
                            <GridItem colSpan={3} _hover={{ boxShadow: '2xl' }} boxShadow='md' rounded='md' bg='#EAEDED'> Choice 4 </GridItem>
                            <GridItem colSpan={3} _hover={{ boxShadow: '2xl' }} boxShadow='md' rounded='md' bg='#EAEDED'> Choice 5 </GridItem>
                            <GridItem colSpan={3} _hover={{ boxShadow: '2xl' }} boxShadow='md' rounded='md' bg='#EAEDED'> Choice 6 </GridItem>
                            <GridItem colSpan={3} _hover={{ boxShadow: '2xl' }} boxShadow='md' rounded='md' bg='#EAEDED'> Choice 7 </GridItem>
                            <GridItem colSpan={2} _hover={{ boxShadow: '2xl' }} />
                            <GridItem colSpan={1} _hover={{ boxShadow: '2xl' }} boxShadow='md' rounded='md' bg='#3182CE' color='white' fontWeight='bold'> Next Week </GridItem>
                        </Grid>
                    </Box>
                </Flex >
            </Container >
        </>
    )
}

export default Simulation;