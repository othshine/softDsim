import {
    Box,
    Breadcrumb,
    BreadcrumbItem,
    BreadcrumbLink,
    Button,
    Container,
    Heading,
    Modal,
    ModalBody,
    ModalCloseButton,
    ModalContent,
    ModalFooter,
    ModalHeader,
    ModalOverlay,
    Text,
    useDisclosure
} from "@chakra-ui/react";
import {HiChevronRight} from "react-icons/hi";
import {useEffect, useState} from "react";
import {Link, useLocation} from "react-router-dom";

const SimulationAlternative = () => {
    const [userScenario, setUserScenario] = useState({});

    const location = useLocation();

    const { isOpen, onOpen, onClose } = useDisclosure();

    const fetchUserScenario = () => {
        const userScenarioMock = {
            scn_name: "Scenario 1"
        }
        setUserScenario(userScenarioMock)
    };

    const scenarioPath = () => {
        const url = location.pathname;
        const newUrl = url.slice(0, url.lastIndexOf("/"));
        return newUrl;
    }

    useEffect(() => {
        fetchUserScenario();
        onOpen();
    }, [onOpen]);

    return (
        <>
            <Modal isOpen={isOpen} onClose={onClose} isCentered>
                <ModalOverlay/>
                <ModalContent>
                    <ModalHeader>Modal Title</ModalHeader>
                    <ModalCloseButton/>
                    <ModalBody>
                        <Text>Scenario Description Here</Text>
                    </ModalBody>

                    <ModalFooter>
                        <Button colorScheme='blue' mr={3} onClick={onClose}>
                            Start
                        </Button>
                    </ModalFooter>
                </ModalContent>
            </Modal>


            {/* TODO create 60 / 40 split layout*/}
            <Box px={10} pt={2}>
                <Breadcrumb spacing='8px' separator={<HiChevronRight color='gray.500'/>}>
                    <BreadcrumbItem>
                        <BreadcrumbLink as={Link} to={scenarioPath()}>Scenarios</BreadcrumbLink>
                    </BreadcrumbItem>
                    <BreadcrumbItem>
                        <BreadcrumbLink href=''>{userScenario.scn_name}</BreadcrumbLink>
                    </BreadcrumbItem>
                </Breadcrumb>
                <Heading>{userScenario.scn_name}</Heading>
                <Box h={5}></Box>
                <Box backgroundColor="white" borderRadius="2xl" minH="60vh">
                    <Container maxW='4xl' pt={10}>
                    </Container>
                </Box>
            </Box>
        </>
    )
};
export default SimulationAlternative;