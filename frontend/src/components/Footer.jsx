import { Flex, HStack, Button, Text } from "@chakra-ui/react"
import React from "react";

const Footer = () => {

    return (
        <>
            <Flex justify="center">
                <HStack
                    w="45%"
                    justifyContent="start"
                    align="center"
                    gap={1}
                    p={5}
                >
                    <Text textalign="center" textColor="gray.500" fontWeight="bold">
                        © 2022 Simplify
                    </Text>
                </HStack>
                <HStack
                    w="45%"
                    justifyContent="end"
                    gap={10}
                    p={5}
                >
                    <Button variant='link'>
                        Imprint
                    </Button>
                    <Button variant='link'>
                        GDPR
                    </Button>
                </HStack>
            </Flex>
        </>
    )
}

export default Footer;