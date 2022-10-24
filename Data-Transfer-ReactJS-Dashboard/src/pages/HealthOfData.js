import './HealthOfData.css';
import configData from '../config.json';
const HealthOfData = () => {
    
    return (
      <div className = "HealthOfData">
        <iframe className='totalthroughput' src={configData.HEALTH_OF_DATA.TOTAL_THROUGHPUT} frameborder="0"></iframe>
        <iframe className="memory" src={configData.HEALTH_OF_DATA.MEMORY} frameborder="0"></iframe>
        <iframe className='avgthroughput' src={configData.HEALTH_OF_DATA.AVG_THROUGHPUT} frameborder="0"></iframe>
        <iframe className='individualthroughput' src={configData.HEALTH_OF_DATA.INDIVIDUAL_THROUGHPUT} frameborder="0"></iframe>
      </div>
    )
};

export default HealthOfData;
