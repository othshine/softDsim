import {
    Box,
    Breadcrumb,
    BreadcrumbItem,
    BreadcrumbLink, Button,
    Container,
    Heading,
    Table,
    TableContainer,
    Tbody,
    Td,
    Th,
    Thead,
    Tr,
} from "@chakra-ui/react";
import {HiChevronRight} from "react-icons/hi";
import {useEffect, useState} from "react";
import {useNavigate} from "react-router-dom";

const ScenarioOverview = () => {
    const [scenarios, setScenarios] = useState([]);

    const navigate = useNavigate();

    const fetchScenarios = () => {
        // TODO When API is ready
        setScenarios([...[
            {
                scn_name: "Scenario 1",
                id: "62718607e99ef2798fc61cfa",
                tries: "2",
                best_score: "432"
            },
            {
                scn_name: "Scenario 2",
                id: "62718607301ßf2798fc61cfa",
                tries: "11",
                best_score: "200"
            },
            {
                scn_name: "Scenario 3",
                id: "92018607301ßf2798fc61caa3",
                tries: "1",
                best_score: "99"
            },
        ]])
    };

    const navigateToScenario = (scn_id) => {
        navigate(`${scn_id}`)
    };

    useEffect(() => {
        fetchScenarios();
    }, []);

    return (
        <Box px={10} pt={2}>
            <Breadcrumb spacing='8px' separator={<HiChevronRight color='gray.500'/>}>
                <BreadcrumbItem>
                    <BreadcrumbLink href=''>Scenarios</BreadcrumbLink>
                </BreadcrumbItem>
            </Breadcrumb>
            <Heading>Scenarios</Heading>
            <Box h={5}></Box>
            <Box backgroundColor="white" borderRadius="2xl" minH="60vh">
                <Container maxW='4xl' pt={10}>
                    <TableContainer>
                        <Table variant='simple' size="lg">
                            <Thead>
                                <Tr>
                                    <Th color="gray.400">Scenario Name</Th>
                                    <Th color="gray.400">Tries</Th>
                                    <Th color="gray.400" isNumeric>Best Score</Th>
                                </Tr>
                            </Thead>
                            <Tbody>
                                {scenarios.map((scenario, index) => {
                                    return <Tr key={index}>
                                        <Td fontWeight="500">
                                            <Button variant="link" color="black" onClick={() => {
                                                navigateToScenario(scenario.id)
                                            }}
                                            >{scenario.scn_name}</Button>
                                        </Td>
                                        <Td fontWeight="500">{scenario.tries}</Td>
                                        <Td fontWeight="500" isNumeric>{scenario.best_score}</Td>
                                    </Tr>
                                })}
                            </Tbody>
                        </Table>
                    </TableContainer>
                </Container>
            </Box>
        </Box>
    )
};

export default ScenarioOverview;