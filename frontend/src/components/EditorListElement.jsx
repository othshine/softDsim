import {Box, HStack, Icon, Text} from "@chakra-ui/react";
import {MdDragIndicator} from "react-icons/md";

// TODO Implement ConditionalWrapper Component to resolve code duplication
const EditorListElement = (props) => {

    return (
            props.isSelected ?
                <Box border="1px solid black" p="4px">
                <HStack w="200px" h="50px"
                        justifyContent="space-around" onMouseDown={props.onClick}
                        elementid={props.id}
                        backgroundColor={props.backgroundColor}
                >
                    <Text>{props.title}</Text>
                    <Box {...props.handleProps}>
                        <Icon as={MdDragIndicator}
                              fontSize={20}/>
                    </Box>
                </HStack>
                </Box>
                :
                <Box p="5px">
                <HStack w="200px" h="50px"
                        justifyContent="space-around" onMouseDown={props.onClick}
                        elementid={props.id}
                        backgroundColor={props.backgroundColor}
                >
                    <Text>{props.title}</Text>
                    <Box {...props.handleProps}>
                        <Icon as={MdDragIndicator}
                              fontSize={20}/>
                    </Box>
                </HStack>
                </Box>
    )
};

export default EditorListElement;