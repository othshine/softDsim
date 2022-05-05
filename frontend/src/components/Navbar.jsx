import {
    Avatar,
    Button,
    Flex,
    HStack,
    IconButton,
    Image,
    Menu,
    MenuButton,
    MenuDivider,
    MenuGroup,
    MenuItem,
    MenuList,
    Text
} from "@chakra-ui/react"
import Logo from "../images/modern-logo.png"
import {HiMoon, HiOutlineLogout} from "react-icons/hi";
import {useEffect, useRef} from "react";

const Navbar = () => {
    const menuButton = useRef();

    // Workaround to center text in avatar
    useEffect(() => {
        menuButton.current.firstElementChild.style.width = "100%"
    }, [])

    return (
        <Flex
            w="full"
            px={16}
            py={4}
            borderBottom="1px solid #E2E8F0"
        >
            <Image src={Logo} alt="logo" w={14} objectFit="contain"/>
            <HStack
                w="100%"
                justifyContent="center"
                gap={14}
            >
                <Button variant='link'>
                    Scenarios
                </Button>
                <Button variant='link'>
                    Simulation Studio
                </Button>
                <Button variant='link'>
                    User Management
                </Button>
                <Button variant='link'>
                    Help
                </Button>

            </HStack>
            <HStack
                justifyContent="flex-end"
            >
                <HStack borderRadius="full" backgroundColor="white" p={3} boxShadow='xl'>
                    <Text whiteSpace="nowrap">👋 Hey, Oshigaki Kisame</Text>
                    <IconButton
                        variant='ghost'
                        aria-label='Call Sage'
                        fontSize='20px'
                        icon={<HiMoon/>}
                        size="xs"
                    />
                    <Menu>
                        <MenuButton ref={menuButton} as={Avatar} name='Oshigaki Kisame' size="sm" cursor="pointer">
                        </MenuButton>
                        <MenuList>
                            <MenuGroup title='Profile'>
                                <MenuItem>My Account</MenuItem>
                                <MenuItem icon={<HiOutlineLogout/>} color="red">Logout </MenuItem>
                            </MenuGroup>
                            <MenuDivider/>
                            <MenuGroup title='Profile'>
                                <MenuItem>My Account</MenuItem>
                                <MenuItem icon={<HiOutlineLogout/>} color="red">Logout </MenuItem>
                            </MenuGroup>
                        </MenuList>
                    </Menu>
                </HStack>

            </HStack>
        </Flex>
    )
}

export default Navbar;