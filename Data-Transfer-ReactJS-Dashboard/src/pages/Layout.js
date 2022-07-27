import { Outlet, Link} from "react-router-dom";
import './Layout.css';

const Layout = () => {
  return (
    <>
      <br></br>
      <br></br>
      <br></br>
      <br></br>
        <ul>
          <li>
            <Link to="/">Data Transfer Progress</Link>
          </li>
          <li>
            <Link to="/healofdata">Health of Data</Link>
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