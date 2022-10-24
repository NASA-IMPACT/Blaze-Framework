import './App.css';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import DataTransferProgress from "./pages/DataTransferProgress";
import HealthOfData from "./pages/HealthOfData";
import Layout from "./pages/Layout";
import logo from './images/earthdata-logo.png';
import TransferQueue from "./pages/TransferQueue";
import TechnicalDetails from './pages/TechnicalDetails';


function App() {
  return (
    <html>
      <div className="App">
        <img className='logo' src={logo}></img>
      </div>
      <BrowserRouter>
      <Routes>
          <Route path="/" element={<Layout />}>
          <Route index element={<DataTransferProgress />} />
          <Route path="healthofdata" element={<HealthOfData />} />
          <Route path="technicaldetails" element={<TechnicalDetails />} />
          <Route path="transferqueue" element={<TransferQueue />} />
        </Route>
      </Routes>
    </BrowserRouter>
    </html>
  );
}

export default App;
