import React, {useEffect} from "react";
import {BrowserRouter, Route, Routes} from "react-router-dom";
import Navbar from "./components/Navbar";
import Landing from "./pages/Landing";

function App() {

    useEffect(() => {
        document.body.style.backgroundColor = "#EDF2F7";
    }, []);

    return (
        <>
        <Navbar/>
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Landing/>}/>
            </Routes>
        </BrowserRouter>
        </>
    );
}

export default App;
