import {Text} from "@chakra-ui/react";
import {useEffect} from "react";

const InnerFragmentList = (props) => {
    const actions = props.actions;

    useEffect(() => {
        console.log("##########################", actions)
    }, [])

    return ( <>
        {   actions &&
            props.actions.map((action, index) => {
            // TODO Design action component
            return (<Text key={index}>hello</Text>)
            })}
    </>)
};
export default InnerFragmentList;