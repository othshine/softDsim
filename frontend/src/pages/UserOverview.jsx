import {
    Box,
    Breadcrumb,
    BreadcrumbItem,
    BreadcrumbLink,
    Button,
    Container, Flex,
    Heading,
    IconButton,
    Table,
    TableContainer,
    Tbody,
    Td,
    Th,
    Thead,
    Tr
} from "@chakra-ui/react";
import {HiChevronRight, HiOutlineTrash} from "react-icons/hi";
import {useEffect, useState} from "react";
import client from "../axiosConfig";

const UserOverview = () => {
    const [users, setUsers] = useState([]);

    const fetchUsers = async () => {
        const res  = await client.get("/csrf-cookie");
        console.log(res)
        setUsers([
            {
                id: 1,
                firstName: "Itachi",
                lastName: "Uchiha",
                email: "itachi.uchiha@stud.fra-uas.de"
            },
            {
                id: 2,
                firstName: "Neji",
                lastName: "Hyuga",
                email: "neji.hyuga@stud.fra-uas.de"
            },
            {
                id: 3,
                firstName: "Rock",
                lastName: "Lee",
                email: "rock.lee@stud.fra-uas.de"
            },
        ])
    };

    const navigateToUser = () => {

    };

    const fetchUserss = async () => {
        const config = {
            headers: {
                "X-CSRFToken": "sC6HnD76p1j3otcbDqB453OCCEnU6SXK2regwwJsX8Tx0U3hpbXSdRmUj1vC94SC",
                "Access-Control-Allow-Origin": "http://localhost:8000",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Methods": "*"
            },
            withCredentials: true
        }

        const res = await client.get("/user", config);
        console.log(res)
    }

    useEffect( () => {
        fetchUsers();
    }, []);

    return (
        <Flex px={10} pt={2} flexDir="column" flexGrow={1}>
            <Breadcrumb spacing='8px' separator={<HiChevronRight color='gray.500'/>}>
                <BreadcrumbItem>
                    <BreadcrumbLink href=''>Users</BreadcrumbLink>
                </BreadcrumbItem>
            </Breadcrumb>
            <Heading>Users</Heading>
            <Box h={5}></Box>
            <Box backgroundColor="white" borderRadius="2xl" minH="60vh">
                <Container maxW='4xl' pt={10}>
                    <TableContainer>
                        <Table variant='simple' size="lg">
                            <Thead>
                                <Tr>
                                    <Th color="gray.400">User Name</Th>
                                    <Th color="gray.400">Email</Th>
                                    <Th color="gray.400" >Actions</Th>
                                </Tr>
                            </Thead>
                            <Tbody>
                                {users.map((user, index) => {
                                    return <Tr key={index}>
                                        <Td fontWeight="500">
                                            <Button variant="link" color="black" onClick={() => {
                                                navigateToUser(user.id)
                                                fetchUserss()

                                            }}>{`${user.firstName} ${user.lastName}`}</Button>
                                        </Td>
                                        <Td fontWeight="500">{user.email}</Td>
                                        <Td fontWeight="500">
                                            <IconButton
                                                variant='ghost'
                                                colorScheme='black'
                                                aria-label='Call Sage'
                                                fontSize='20px'
                                                icon={<HiOutlineTrash />}
                                            />
                                        </Td>
                                    </Tr>
                                })}
                            </Tbody>
                        </Table>
                    </TableContainer>
                </Container>
            </Box>
        </Flex>
    )
};

export default UserOverview;