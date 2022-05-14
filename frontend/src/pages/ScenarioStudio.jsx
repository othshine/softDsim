import {
    Box,
    Breadcrumb,
    BreadcrumbItem,
    BreadcrumbLink,
    Flex,
    Heading,
    HStack,
    Icon, Image, ListItem,
    Tab,
    TabList,
    TabPanel,
    TabPanels,
    Tabs,
    Text, UnorderedList,
    VStack
} from "@chakra-ui/react";
import {HiChevronRight} from "react-icons/hi";
import {RiDragDropLine} from "react-icons/ri";
import {DragDropContext, Draggable, Droppable} from "react-beautiful-dnd";
import {Fragment, useEffect, useState} from "react";
import {MdDragIndicator, MdOutlineAttractions, MdOutlineInfo, MdRule, MdTimeline} from "react-icons/md";
import {v4 as uuidv4} from 'uuid';
import styled from "@emotion/styled";
import {BsLightningCharge, BsLightningChargeFill} from "react-icons/bs";
import ComponentListElement from "../components/ComponentListElement";

const Clone = styled(ListItem)`
  margin-bottom: 12px;
  + li {
    display: none !important;
    background-color: blueviolet;
  }
`;

const ScenarioStudio = () => {

    const finalComponentList = [
        {
            id: uuidv4(),
            title: "Simulation Base Information",
            content: "Define the basisc stats for a new simulation.",
            icon: MdOutlineInfo,
        },
        {
            id: uuidv4(),
            title: "Simulation Fragment",
            content: "Control the simulation by defining fragments.",
            icon: MdTimeline,
        },
        {
            id: uuidv4(),
            title: "Action",
            content: "Trigger actions like teamevents or training sessions.",
            icon: BsLightningCharge,
        },
        {
            id: uuidv4(),
            title: "Decisions",
            content: "Create questions which need to be answered.",
            icon: MdRule,
        },
        {
            id: uuidv4(),
            title: "Event",
            content: "Add events which can occur during the simulation like the illness of an employee.",
            icon: MdOutlineAttractions,
        },
    ]

    const [editorList, updateEditorList] = useState([]);

    const handleOnDragEnd = (result) => {
        // handle moving outside droppables
        if (!result.destination) return;

        // moving in the editor list
        if (result.source.droppableId === "editor" && result.destination.droppableId === "editor") {
            const items = Array.from(editorList);
            const [reorderedItem] = items.splice(result.source.index, 1);
            items.splice(result.destination.index, 0, reorderedItem);

            updateEditorList(items);
            // moving from component list to editor list
        } else if (result.source.droppableId === "componentList" && result.destination.droppableId === "editor") {
            const componentListItems = Array.from(finalComponentList);
            const [movedItem] = componentListItems.splice(result.source.index, 1);

            const editorListItems = Array.from(editorList);
            let movedItemCopy = {...movedItem};
            movedItemCopy.id = uuidv4();
            editorListItems.splice(result.destination.index, 0, movedItemCopy);
            updateEditorList(editorListItems);
        }
    };

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
                    <DragDropContext onDragEnd={handleOnDragEnd}>
                        {/*Editor*/}
                        <Flex w="full" h="full" justifyContent="center" alignItems="center" backgroundColor="white"
                              borderRadius="2xl">
                            <Droppable droppableId="editor">
                                {(provided, snapshot) => (
                                    <UnorderedList listStyleType="none"
                                                   m={0}
                                                   p={40}
                                                   transition="background-color 0.2s ease"
                                                   minH="90%"
                                                   minW="90%"
                                                   {...provided.droppableProps}
                                                   ref={provided.innerRef}
                                                   backgroundColor={snapshot.isDraggingOver ? "gray.200" : ""}
                                                   display="flex"
                                                   flexDir="column"
                                                   justifyContent={editorList.length ? "flex-start" : "center"}
                                                   alignItems="center"
                                                   borderRadius="2xl">
                                        {
                                            editorList.length ?
                                                editorList.map(({id, title}, index) => {
                                                        return (
                                                            <Draggable key={id} draggableId={id} index={index}>
                                                                {(provided, snapshot) => (
                                                                    <ListItem
                                                                        mb={3}
                                                                        backgroundColor={snapshot.isDragging ? "blue.200" : "red.200"}
                                                                        {...provided.draggableProps}
                                                                        ref={provided.innerRef}
                                                                    >
                                                                        <HStack w="200px" h="50px"
                                                                                justifyContent="space-around">
                                                                            <Text>{title}</Text>
                                                                            <Box {...provided.dragHandleProps}>
                                                                                <Icon as={MdDragIndicator}
                                                                                      fontSize={20}/>
                                                                            </Box>
                                                                        </HStack>
                                                                    </ListItem>
                                                                )}
                                                            </Draggable>
                                                        )
                                                    }
                                                )
                                                :
                                                <VStack color="gray.200">
                                                    <Icon as={RiDragDropLine} w={20} h={20} mb={6}/>
                                                    <Heading size="lg" pointerEvents="none">Drag a component
                                                        here</Heading>
                                                    <Text pointerEvents="none" fontSize="xl" mt="20px">(Create a complex
                                                        scenario by drag and dropping different components)</Text>
                                                </VStack>
                                        }
                                        }
                                        {provided.placeholder}
                                    </UnorderedList>
                                )}
                            </Droppable>

                        </Flex>


                        {/*Right Panel*/}
                        <Box h="full" backgroundColor="white" borderRadius="2xl">
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
                                            <Droppable droppableId="componentList" isDropDisabled={true}>
                                                {(provided) => (
                                                    <UnorderedList
                                                        listStyleType="none"
                                                        ref={provided.innerRef}
                                                    >
                                                        {finalComponentList.map(({id, title, content, icon}, index) => {
                                                                return (
                                                                    <Draggable
                                                                        key={id}
                                                                        draggableId={id}
                                                                        index={index}>
                                                                        {(provided, snapshot) => (
                                                                            <Fragment>
                                                                                <ListItem
                                                                                    ref={provided.innerRef}
                                                                                    {...provided.draggableProps}
                                                                                    {...provided.dragHandleProps}
                                                                                    mb={3}
                                                                                >
                                                                                    <ComponentListElement title={title} content={content} icon={icon}/>
                                                                                </ListItem>
                                                                                {snapshot.isDragging &&
                                                                                    <Clone>
                                                                                        <ComponentListElement title={title} content={content} icon={icon}/>
                                                                                    </Clone>}
                                                                            </Fragment>
                                                                        )}
                                                                    </Draggable>
                                                                )
                                                            }
                                                        )
                                                        }
                                                        {provided.placeholder}
                                                    </UnorderedList>
                                                )}
                                            </Droppable>
                                        </VStack>
                                    </TabPanel>
                                </TabPanels>
                            </Tabs>
                        </Box>
                    </DragDropContext>
                </HStack>
            </Box>
        </Flex>
    )
};

export default ScenarioStudio