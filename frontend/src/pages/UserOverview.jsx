import {
    AlertDialog,
    AlertDialogBody,
    AlertDialogContent,
    AlertDialogFooter,
    AlertDialogHeader,
    AlertDialogOverlay,
    Box,
    Breadcrumb,
    BreadcrumbItem,
    BreadcrumbLink,
    Button,
    Container,
    Flex,
    Heading,
    IconButton,
    Table,
    TableContainer,
    Tbody,
    Td,
    Th,
    Thead,
    Tr,
    useDisclosure,
    useToast
} from "@chakra-ui/react";
import {HiChevronRight, HiOutlineCheck, HiOutlineTrash} from "react-icons/hi";
import {useEffect, useRef, useState} from "react";
import getCookie from "../utils/utils";

const UserOverview = () => {
    const [users, setUsers] = useState([]);
    const [userToDelete, setUserToDelete] = useState("");

    const toast = useToast()

    const {isOpen, onOpen, onClose} = useDisclosure()
    const cancelRef = useRef();

    const fetchUsers = async () => {
        const res = await fetch('http://localhost:8000/api/user', {
            method: 'GET',
            credentials: 'include',
        })
        const fetchedUsers = await res.json();
        setUsers(fetchedUsers)
    };

    const navigateToUser = () => {

    };

    const deleteUser = async (username) => {
        try {
            const res = await fetch(`http://localhost:8000/api/user/${username}`, {
                method: 'DELETE',
                credentials: 'include',
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                }
            })
            await res.json();
            fetchUsers();
            toast({
                title: `${username} has been deleted`,
                status: 'success',
                duration: 5000,
            });
        } catch (e) {
            toast({
                title: `Could not delete ${username}`,
                status: 'error',
                duration: 5000,
            });
            console.log(e);
        }

    };

    useEffect(() => {
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
                                    <Th color="gray.400">Superadmin</Th>
                                    <Th color="gray.400">Admin</Th>
                                    <Th color="gray.400">Actions</Th>
                                </Tr>
                            </Thead>
                            <Tbody>
                                {users.map((user, index) => {
                                    return <Tr key={index}>
                                        <Td fontWeight="500">
                                            <Button variant="link" color="black" onClick={() => {
                                                navigateToUser(user.id)

                                            }}>{`${user.username[0].toUpperCase() + user.username.slice(1)}`}</Button>
                                        </Td>
                                        <Td fontWeight="500">{user.is_superuser ? <HiOutlineCheck/> : ""}</Td>
                                        <Td fontWeight="500">{user.is_staff ? <HiOutlineCheck/> : ""}</Td>
                                        <Td fontWeight="500">
                                            <IconButton
                                                variant='ghost'
                                                colorScheme='black'
                                                aria-label='Call Sage'
                                                fontSize='20px'
                                                icon={<HiOutlineTrash/>}
                                                onClick={() => {
                                                    onOpen()
                                                    setUserToDelete(user.username)
                                                }
                                                }
                                            />
                                        </Td>
                                    </Tr>
                                })}
                            </Tbody>
                        </Table>
                    </TableContainer>
                </Container>
            </Box>

            {/*Delete user alert pop up*/}
            <AlertDialog
                isOpen={isOpen}
                leastDestructiveRef={cancelRef}
                onClose={onClose}
                isCentered
                motionPreset='slideInBottom'
            >
                <AlertDialogOverlay>
                    <AlertDialogContent>
                        <AlertDialogHeader fontSize='lg' fontWeight='bold'>
                            Delete user {userToDelete}
                        </AlertDialogHeader>

                        <AlertDialogBody>
                            Are you sure? You can't undo this action afterwards.
                        </AlertDialogBody>

                        <AlertDialogFooter>
                            <Button ref={cancelRef} onClick={onClose}>
                                Cancel
                            </Button>
                            <Button colorScheme='red' onClick={() => {
                                deleteUser(userToDelete)
                                onClose()
                            }} ml={3}>
                                Delete
                            </Button>
                        </AlertDialogFooter>
                    </AlertDialogContent>
                </AlertDialogOverlay>
            </AlertDialog>
        </Flex>
    )
};

export default UserOverview;