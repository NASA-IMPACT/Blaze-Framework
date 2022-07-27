import './App.css';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./pages/Layout";
import DataTransferProgress from "./pages/DataTransferProgress";
import HealthOfData from "./pages/HealthOfData";
import TransferQueue from "./pages/TransferQueue";
import TechnicalDetails from './pages/TechnicalDetails';
import logo from './images/earthdata-logo.png';

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
          <Route path="healofdata" element={<HealthOfData />} />
          <Route path="technicaldetails" element={<TechnicalDetails />} />
          <Route path="transferqueue" element={<TransferQueue />} />
        </Route>
      </Routes>
    </BrowserRouter>
    </html>
  );
}

export default App;
