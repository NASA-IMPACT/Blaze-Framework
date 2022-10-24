import './TechnicalDetails.css'
import configData from '../config.json'
const TechnicalDetails = () => {
    return (
      <div className = "TechnicalDetails">
        <iframe className="uptime" src={configData.TECHNICAL_DETAILS.UP_TIME} frameborder="0"></iframe>
        <iframe className="load" src={configData.TECHNICAL_DETAILS.LOAD} frameborder="0"></iframe>      
    </div>
    )
};
  
export default TechnicalDetails;
