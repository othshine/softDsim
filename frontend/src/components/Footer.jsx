import { Flex, HStack, Button } from "@chakra-ui/react"
import React from "react";

const Footer = () => {

    return (
        <>
            <Flex>
                <HStack
                    w="100%"
                    justifyContent="center"
                    gap={14}
                    p={4}
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