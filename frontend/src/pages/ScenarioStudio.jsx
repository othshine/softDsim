import {
    Box,
    Breadcrumb,
    BreadcrumbItem,
    BreadcrumbLink,
    Flex,
    Heading,
    HStack,
    Icon, ListItem,
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
import {MdDragIndicator} from "react-icons/md";
import { v4 as uuidv4 } from 'uuid';
import styled from "@emotion/styled";

const Clone = styled.li`
  background-color: chartreuse;
  width: 200px;
  height: 50px;
    + li {
        display: none !important;
      background-color: blueviolet;
    }
`;

const ScenarioStudio = () => {
    const finalDataList = [
        {
            id: uuidv4(),
            name: "Dropdown"
        },
        {
            id: uuidv4(),
            name: "Buttons"
        },
        {
            id: uuidv4(),
            name: "Radio Buttons"
        },
    ]

    const finalComponentList = [
        {
            id: uuidv4(),
            name: "Dropdown"
        },
        {
            id: uuidv4(),
            name: "Buttons"
        },
        {
            id: uuidv4(),
            name: "Radio Buttons"
        },
    ]

    const [editorList, updateEditorList] = useState(finalDataList);
    const [componentList, updateComponentList] = useState(finalComponentList);

    useEffect(() => {
        console.log(componentList)
    })

    const handleOnDragEnd = (result) => {
        // handle moving outside droppables
        if(!result.destination) return;

        // moving in the editor list
        if(result.source.droppableId === "editor" && result.destination.droppableId === "editor") {
            const items = Array.from(editorList);
            const [reorderedItem] = items.splice(result.source.index, 1);
            items.splice(result.destination.index, 0, reorderedItem);

            updateEditorList(items);
            // moving from component list to editor list
        } else if (result.source.droppableId === "componentList" && result.destination.droppableId === "editor") {
            const componentListItems = Array.from(componentList);
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
                            {/*<VStack color="gray.200">*/}
                            {/*    <Icon as={RiDragDropLine} w={20} h={20} mb={6}/>*/}
                            {/*    <Heading size="lg" pointerEvents="none">Drag a component here</Heading>*/}
                            {/*    <Text pointerEvents="none" fontSize="xl" mt="20px">(Create a scenario by drag and dropping different components)</Text>*/}
                            {/*</VStack>*/}
                            <Droppable droppableId="editor">
                                {(provided, snapshot) => (
                                    <UnorderedList listStyleType="none"
                                                   p={4}
                                                   border="1px solid"
                                                   transition="background-color 0.2s ease"
                                                   minH={80}
                                                   {...provided.droppableProps}
                                                   ref={provided.innerRef}
                                                   backgroundColor={snapshot.isDraggingOver ? "gray.200" : ""}>
                                        {
                                            editorList.map(({id, name}, index) => {
                                                    return (
                                                        <Draggable key={id} draggableId={id} index={index}>
                                                            {(provided, snapshot) => (
                                                                <ListItem
                                                                    mb={3}
                                                                    backgroundColor={snapshot.isDragging ? "blue.200" : "red.200"}
                                                                    {...provided.draggableProps}
                                                                    ref={provided.innerRef}
                                                                >
                                                                    <HStack w="200px" h="50px" justifyContent="space-around">
                                                                        <Text>{name}</Text>
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
                                        }
                                        {provided.placeholder}
                                    </UnorderedList>
                                )}
                            </Droppable>

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
                                            <Droppable droppableId="componentList" isDropDisabled={true}>
                                                {(provided, snapshot) => (
                                                    <UnorderedList
                                                        listStyleType="none"
                                                        // h={200}
                                                        //{...provided.droppableProps}
                                                        ref={provided.innerRef}
                                                        // isDraggingOver={snapshot.isDraggingOver}
                                                    >
                                                        {finalComponentList.map(({id, name}, index) => {
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
                                                                                >
                                                                                    <VStack w="200px" h="50px" backgroundColor="red.200">
                                                                                        <Text>{name}</Text>
                                                                                    </VStack>
                                                                                </ListItem>
                                                                                {snapshot.isDragging &&
                                                                                    <Clone>
                                                                                        {name}
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

                                            {/*<Droppable droppableId="ITEMS" isDropDisabled={true}>*/}
                                            {/*    {(provided, snapshot) => (*/}
                                            {/*        <Kiosk*/}
                                            {/*            ref={provided.innerRef}*/}
                                            {/*            isDraggingOver={snapshot.isDraggingOver}>*/}
                                            {/*            {finalComponentList.map((item, index) => (*/}
                                            {/*                <Draggable*/}
                                            {/*                    key={item.id}*/}
                                            {/*                    draggableId={item.id}*/}
                                            {/*                    index={index}>*/}
                                            {/*                    {(provided, snapshot) => (*/}
                                            {/*                        <Fragment>*/}
                                            {/*                            <Item*/}
                                            {/*                                ref={provided.innerRef}*/}
                                            {/*                                {...provided.draggableProps}*/}
                                            {/*                                {...provided.dragHandleProps}*/}
                                            {/*                                isDragging={snapshot.isDragging}*/}
                                            {/*                                style={*/}
                                            {/*                                    provided.draggableProps*/}
                                            {/*                                        .style*/}
                                            {/*                                }>*/}
                                            {/*                                {item.name}*/}
                                            {/*                            </Item>*/}
                                            {/*                            {snapshot.isDragging && (*/}
                                            {/*                                <Clone>{item.name}</Clone>*/}
                                            {/*                            )}*/}
                                            {/*                        </Fragment>*/}
                                            {/*                    )}*/}
                                            {/*                </Draggable>*/}
                                            {/*            ))}*/}
                                            {/*        </Kiosk>*/}
                                            {/*    )}*/}
                                            {/*</Droppable>*/}
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