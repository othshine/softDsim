import {Box, Heading, ListItem, UnorderedList} from "@chakra-ui/react";
import {Draggable, Droppable} from "react-beautiful-dnd";
import EditorBasicComponent from "./EditorBasicComponent";

const ComponentListDroppable = (props) => {

    return (
        <Draggable draggableId={props.id} index={props.index}>
            {(provided) => (

                <Box
                    {...provided.draggableProps}
                    ref={provided.innerRef}
                >
                    <Heading {...provided.dragHandleProps}>Test</Heading>
                    <Droppable droppableId="actionContainer"
                               type="action" // TODO make dynamically or set up correct type
                    >
                        {(provided, snapshot) => (
                            <UnorderedList listStyleType="none"
                                           m={0}
                                           // p={40}
                                           transition="background-color 0.2s ease"
                                           minH="200px"
                                           minW="200px"
                                           {...provided.droppableProps}
                                           ref={provided.innerRef}
                                           backgroundColor={snapshot.isDraggingOver ? "gray.200" : ""}
                                           display="flex"
                                           flexDir="column"
                                // justifyContent={editorList.length ? "flex-start" : "center"}
                                           alignItems="center"
                                           borderRadius="2xl">
                                {
                                    <Draggable key={"1111"} draggableId={"1111"} index={1} action="hello">
                                        {(provided, snapshot) => (
                                            <ListItem
                                                mb={3}
                                                {...provided.draggableProps}
                                                ref={provided.innerRef}
                                            >
                                                <EditorBasicComponent
                                                    backgroundColor={snapshot.isDragging ? "blue.200" : "red.200"}
                                                    elementid={"1111"}
                                                    // onClick={((e) => handleSelect(e))}
                                                    id={"1111"}
                                                    title={"dragable"}
                                                    handleProps={provided.dragHandleProps}
                                                    // isSelected={selectedItem === "1111"}
                                                />

                                            </ListItem>
                                        )}
                                    </Draggable>
                                }
                            </UnorderedList>
                        )

                        }
                    </Droppable>
                </Box>
            )}
        </Draggable>

    )
};

export default ComponentListDroppable;