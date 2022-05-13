import {
    Box,
    Breadcrumb,
    BreadcrumbItem,
    BreadcrumbLink,
    Flex,
    Heading,
    HStack,
    Icon,
    Tab,
    TabList,
    TabPanel,
    TabPanels,
    Tabs,
    Text,
    VStack
} from "@chakra-ui/react";
import {HiChevronRight} from "react-icons/hi";
import {RiDragDropLine} from "react-icons/ri";

const ScenarioStudio = () => {
    return (
        <Flex px={10} pt={2} flexDir="column" flexGrow={1}>
            <Breadcrumb spacing='8px' separator={<HiChevronRight color='gray.500'/>}>
                <BreadcrumbItem>
                    <BreadcrumbLink href=''>Scenarios Studio</BreadcrumbLink>
                </BreadcrumbItem>
            </Breadcrumb>
            <Heading>Scenario Studio</Heading>
            <Box h={5}></Box>
            <Box backgroundColor="#EDF2F7" borderRadius="2xl" minH="70vh">
                <HStack w="full" h="full" overflow="hidden" pt={2} spacing={5}>

                    {/*Editor*/}
                    <Flex w="full" h="full" justifyContent="center" alignItems="center" backgroundColor="white"
                          borderRadius="2xl">
                        <VStack color="gray.200">
                            <Icon as={RiDragDropLine} w={20} h={20} mb={6}/>
                            <Heading size="lg" pointerEvents="none">Drag a component here</Heading>
                            <Text pointerEvents="none" fontSize="xl" mt="20px">(Create a scenario by drag and dropping different components)</Text>
                        </VStack>
                    </Flex>


                    {/*Right Panel*/}
                    <Box minW={80} h="full" backgroundColor="white" borderRadius="2xl">
                        <Tabs defaultIndex={1}>
                            <TabList>
                                <Tab fontWeight="bold" color="gray.400">Inspector</Tab>
                                <Tab fontWeight="bold" color="gray.400">Components</Tab>
                            </TabList>

                            <TabPanels>
                                <TabPanel>
                                    <p>one!</p>
                                </TabPanel>
                                <TabPanel>
                                    <VStack alignItems="flex-start" pt={3}>
                                        <Text color="gray.400" fontWeight="bold">All Components</Text>
                                        <Box h={40} w="full" backgroundColor="blue.500">
                                        </Box>
                                    </VStack>
                                </TabPanel>
                            </TabPanels>
                        </Tabs>
                    </Box>
                </HStack>
            </Box>
        </Flex>
    )
};

export default ScenarioStudio