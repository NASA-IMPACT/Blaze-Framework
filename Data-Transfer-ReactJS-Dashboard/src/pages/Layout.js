import { Outlet, Link} from "react-router-dom";
import './Layout.css';

const Layout = () => {
  return (
    <>
      <ul>
        <li>
          <Link to="/">Data Transfer Progress</Link>
        </li>
        <li>
          <Link to="/healthofdata">Health of Data</Link>
        </li>
        <li>
          <Link to="/technicaldetails">Technical Details</Link>
        </li>
        <li>
          <Link to="/transferqueue">Transfer Queue</Link>
        </li>
      </ul>
      <Outlet />
    </>
  )
};

export default Layout;
