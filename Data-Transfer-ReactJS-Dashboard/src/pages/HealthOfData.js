import './HealthOfData.css';
const HealthOfData = () => {
    
    return (
      <div className = "HealthOfData">
    
        <iframe className='totalthroughput' src="http://ec2-35-88-36-61.us-west-2.compute.amazonaws.com:3000/d-solo/vUMFoZrnk/hls-data-transfer-metrics?orgId=1&refresh=5s&panelId=24"frameborder="0"></iframe>
        <iframe className="memory" src="http://ec2-35-88-36-61.us-west-2.compute.amazonaws.com:3000/d-solo/vUMFoZrnk/hls-data-transfer-metrics?orgId=1&refresh=5s&panelId=10"frameborder="0"></iframe>
        <iframe className='avgthroughput' src="http://ec2-35-88-36-61.us-west-2.compute.amazonaws.com:3000/d-solo/vUMFoZrnk/hls-data-transfer-metrics?orgId=1&refresh=5s&panelId=14" frameborder="0"></iframe>
      </div>
    )
};
  
  export default HealthOfData;